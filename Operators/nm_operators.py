import bpy
import os
from bpy.types import Operator

# Without a path set, will load/reload from the .blend files parent folder, and then /textures. Eg if .blend exists in /3D Assets/Blend, it'll search in 3D Assets/Textures/.
# Otherwise it will just reload from the path specified.
class AutoLoad(Operator):
    bl_label = "Auto Load"
    bl_idname = "node.autoload"
    
    def execute(self, context):
        blend_dir = os.path.dirname(bpy.data.filepath)
        parent_dir = os.path.dirname(blend_dir)
        texturesFolder = os.path.join(parent_dir, 'Textures')
        setPathFolder = bpy.context.scene.nm_props.texturePath
        
        if setPathFolder and setPathFolder != "/Textures" and os.path.exists(bpy.path.abspath(setPathFolder)):
            applyMaterial(bpy.context.scene.nm_props.texturePath, bpy.context.scene.nm_props)
        else:
            applyMaterial(texturesFolder, bpy.context.scene.nm_props)

        return {'FINISHED'}
#Sets the path to the texture folder and runs automatically to find all the applicable textures.
class LoadFromPath(Operator):
    bl_label = "Load From Path"
    bl_idname = "node.loadfrompath"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if not hasattr(self, 'first_time_run'):
            self.first_time_run = True
        else:
            self.first_time_run = False

        if self.first_time_run:
            # Open the file browser to select a folder
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}

        else:
            # Get the selected folder path
            bpy.context.scene.nm_props.texturePath = os.path.abspath(os.path.dirname(self.filepath))
            textures_dir = bpy.context.scene.nm_props.texturePath
            applyMaterial(textures_dir, bpy.context.scene.nm_props)

            return {'FINISHED'}
    

       
def applyMaterial(textures_dir, properties):    
    apply_to = properties.apply_to
    

    if apply_to == "ALL_VISIBLE":
        # Apply to all visible materials
        for obj in bpy.context.scene.objects:
            if not obj.visible_get():
                continue
            for material_slot in obj.material_slots:
                mat = material_slot.material
                node_tree = mat.node_tree
                nTreeSetup(node_tree, textures_dir, mat.name, properties)
    elif apply_to == "ALL_ATTACHED":
        # Apply to all materials attached to the active object
        if bpy.context.active_object.material_slots:
            obj = bpy.context.active_object
            for material_slot in obj.material_slots:
                mat = material_slot.material
                node_tree = mat.node_tree
                nTreeSetup(node_tree, textures_dir, mat.name, properties)
    else:
# Get the active object
        # Get all objects in the scene
        all_objects = bpy.context.scene.objects

        # Check if there are any objects in the scene
        if len(all_objects) == 0:
            errorGen("No Objects in scene{}".format("."), 'Error', 'FILE_BLANK')   
        else:
            # Get the active object
            obj = bpy.context.active_object
            # Check if there is an active object and if it has an active material
            if  obj == None or obj and obj.active_material == None:
                errorGen("No Material or Object Selected{}".format("."), 'Error', 'FILE_BLANK')              
            else:
                mat = bpy.context.active_object.active_material
                node_tree = mat.node_tree
                material_name = mat.name
                nTreeSetup(node_tree, textures_dir, material_name, properties)
 
#Sets up the node tree based on the structure selected in properties.         
def nTreeSetup(node_tree, textures_dir, material_name, properties):
   
   #Properties
    file_type = properties.image_file_type
    node_structure = properties.node_structure
    nm_Suffix = properties.normal_map if properties.normal_map != "" else "_Normal"
    col_Suffix = properties.base_color if properties.base_color != "" else "_Color"
    
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)

    #Create the GLTF Node if set    
    gltf_settings = None
    if properties.gltf_Node:
       for node in bpy.data.node_groups:
            if node.name == "glTF Material Output":
                gltf_settings = node
                break
       # If the "glTF Settings" node is not found, create it
       if not gltf_settings:
        gltf_settings = bpy.data.node_groups.new(name='glTF Material Output', type='ShaderNodeTree')
       # Add an input called "Occlusion" to the "glTF Settings" node
       if not gltf_settings.inputs.get('Occlusion'):
        input_node = gltf_settings.nodes.new('NodeGroupInput')
        input_node.name = 'Occlusion'
        gltf_settings.inputs.new('NodeSocketVector', 'Occlusion')
       # Add the "glTF Settings" node to the node tree
       gltf_node = node_tree.nodes.new('ShaderNodeGroup')
       gltf_node.node_tree = gltf_settings  
       
    # Create core nodes
    principled_node = createNode(node_tree, 'ShaderNodeBsdfPrincipled', 'Principled BSDF',200, 200)
    material_output_node = createNode(node_tree, 'ShaderNodeOutputMaterial', 'Material Output',600, 0)
    connectNodes(node_tree, principled_node.outputs[0], material_output_node.inputs[0])
    principled_node.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)


    if node_structure == "BLENDER_BSDF":
        met_Suffix = properties.metallic_texture if properties.metallic_texture != "" else "_Metallic"
        roughness_Suffix = properties.roughness_texture if properties.roughness_texture != "" else "_Roughness"
        # Create image texture nodes
        normal_map_node = createNode(node_tree, 'ShaderNodeNormalMap','Normal',0, -350)
        if bpy.context.scene.nm_props.loadImageNodes:
            basecolor_node = createNode(node_tree, 'ShaderNodeTexImage','Color',-400, 200)
            metallic_node = createNode(node_tree, 'ShaderNodeTexImage','Metallic', -400, -100)
            roughness_node = createNode(node_tree, 'ShaderNodeTexImage','Roughness',-100, -100)
            normal_node = createNode(node_tree, 'ShaderNodeTexImage','NormalMap',-300, -400)
            #Load Textures
            normal_node.image = loadImageTexture(textures_dir, material_name, nm_Suffix, file_type, 'Non-Color')
            metallic_node.image = loadImageTexture(textures_dir, material_name, met_Suffix, file_type, 'Non-Color')        
            roughness_node.image = loadImageTexture(textures_dir, material_name, roughness_Suffix, file_type, 'Non-Color')
            basecolor_node.image = loadImageTexture(textures_dir, material_name, col_Suffix, file_type, 'sRGB')
            bpy.ops.node.imgcleaner()
            if gltf_settings:
                ao_node = createNode(node_tree, 'ShaderNodeTexImage','AO',-800,0)
                connectNodes(node_tree, ao_node.outputs['Color'], gltf_node.inputs[0])
                gltf_node.location = (0,50)
        #connect Nodes
            connectNodes(node_tree, normal_node.outputs['Color'], normal_map_node.inputs['Color'])
            connectNodes(node_tree, basecolor_node.outputs['Color'], principled_node.inputs['Base Color'])
            connectNodes(node_tree, metallic_node.outputs['Color'], principled_node.inputs['Metallic'])
            connectNodes(node_tree, roughness_node.outputs['Color'], principled_node.inputs['Roughness'])
        connectNodes(node_tree, normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])
        



    
    if node_structure == "ORM_GLB":
        orm_Suffix = properties.orm_texture if properties.orm_texture != "" else "_ORM"

        # Create Nodes for ORM GLB
        sep_color_node = createNode(node_tree, 'ShaderNodeSeparateColor','Separate Color',-100, -100)
        normal_node = createNode(node_tree, 'ShaderNodeNormalMap','Normal',0, -350)
        if bpy.context.scene.nm_props.loadImageNodes:
            normal_map_node = createNode(node_tree, 'ShaderNodeTexImage','Normal Map',-300, -400)
            orm_node = createNode(node_tree, 'ShaderNodeTexImage','ORM',-400, -100)
            basecolor_node = createNode(node_tree, 'ShaderNodeTexImage','Color', -400, 200)
            #Load images
            orm_node.image = loadImageTexture(textures_dir, material_name, orm_Suffix, file_type, 'Non-Color')
            normal_map_node.image = loadImageTexture(textures_dir, material_name, nm_Suffix, file_type, 'Non-Color')
            basecolor_node.image = loadImageTexture(textures_dir, material_name, col_Suffix, file_type, 'sRGB')
            bpy.ops.node.imgcleaner()
        # Connect Nodes 
            connectNodes(node_tree, orm_node.outputs[0], sep_color_node.inputs[0])
            connectNodes(node_tree, basecolor_node.outputs[0], principled_node.inputs['Base Color'])
            connectNodes(node_tree, normal_map_node.outputs[0], normal_node.inputs[1])
        connectNodes(node_tree, normal_node.outputs[0], principled_node.inputs['Normal'])
        connectNodes(node_tree, sep_color_node.outputs[2], principled_node.inputs['Metallic'])
        connectNodes(node_tree, sep_color_node.outputs[1], principled_node.inputs['Roughness'])
        if gltf_settings:
           connectNodes(node_tree, sep_color_node.outputs[0], gltf_node.inputs[0])

     


 
def createNode(node_tree, node_type, node_name, x, y):
    # Check if node with the given name already exists
    existing_node = None
    for node in node_tree.nodes:
        if node.name == node_name or node.label == node_name:
            existing_node = node
            break
    if existing_node != None:
        errorGen("Found Existing Nodes: {}".format(node_name), 'Error', 'FILE_BLANK')  
        return existing_node
        
    else:
        # Create new node
        new_node = node_tree.nodes.new(node_type)
        new_node.name = node_name
        new_node.label = node_name
        if x is not None and y is not None:
            new_node.location = (x, y)
        return new_node

def loadImageTexture(texDir, material, suffix, filetype, colorSpace):
     if bpy.context.scene.nm_props.loadTextures:
        newPath = os.path.join(texDir, (material + suffix + filetype))
        if os.path.exists(newPath):
            image = bpy.data.images.load(newPath)
            image.colorspace_settings.name = colorSpace
            image.name = material+suffix+filetype
            return image
        else:
            errorGen("Missing Textures: {}".format(newPath), 'Error', 'FILE_BLANK')
     else:
        return
def errorGen (msg, titleVar, iconVar):
         message = msg
         bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message), title=titleVar, icon=iconVar)

def connectNodes(node_tree, output_socket, input_socket):
    links = node_tree.links
    for link in links:
        if link.from_socket == output_socket and link.to_socket == input_socket:
            # Link already exists, return the existing link
            return link
    # Link does not exist, create a new one
    new_link = links.new(output_socket, input_socket)
    return new_link
#add a custom property to objects or materials.   
def addProperty (selection, customProperty, value, applyMat, applyOBJ):
    # get the selected objects
    selection = bpy.context.selected_objects

    # loop through all selected objects
    if applyMat:
        for obj in selection:
            # loop through all materials in the object
            for mat_slot in obj.material_slots:
                mat = mat_slot.material
                # add a custom property named "refractionIOR" with a value of 1.4 to the material
                mat["refractionIOR"] = 1.4
    if applyOBJ: 
            for obj in selection:
                # add a custom property with the specified name and value to the object
                obj[customProperty] = value
