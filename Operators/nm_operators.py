import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty
from ..Props.nm_props import AutoTexProperties
# Without a path set, will load from the .blend files parent folder, and then /textures. Eg if .blend exists in /3D Assets/Blend, it'll search in 3D Assets/Textures/.
# Otherwise it will just reload from the path specified.
class AutoLoad(Operator):
    bl_label = "Auto Load"
    bl_idname = "node.autoload"
    
    def execute(self, context):
        blend_dir = os.path.dirname(bpy.data.filepath)
        parent_dir = os.path.dirname(blend_dir)
        texturesFolder = os.path.join(parent_dir, 'Textures')
        setPathFolder = bpy.context.scene.auto_tex_props.texturePath
        
        if setPathFolder and setPathFolder != "/Textures" and os.path.exists(bpy.path.abspath(setPathFolder)):
            applyMaterial(bpy.context.scene.auto_tex_props.texturePath, bpy.context.scene.auto_tex_props)
        else:
            applyMaterial(texturesFolder, bpy.context.scene.auto_tex_props)

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
            bpy.context.scene.auto_tex_props.texturePath = os.path.abspath(os.path.dirname(self.filepath))
            textures_dir = bpy.context.scene.auto_tex_props.texturePath
            applyMaterial(textures_dir, bpy.context.scene.auto_tex_props)

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
            message = "No Objects in scene".format
            bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message()), title="Error", icon='ERROR')
        else:
            # Get the active object
            obj = bpy.context.active_object
            # Check if there is an active object and if it has an active material
            if  obj == None or obj and obj.active_material == None:
                message = "No Material or Object Selected".format
                bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message()), title="Error", icon='ERROR')
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
       
    # Create nodes
    principled_node = createNode(node_tree, 'ShaderNodeBsdfPrincipled', 'Principled BSDF')
    material_output_node = createNode(node_tree, 'ShaderNodeOutputMaterial', 'Material Output')
    connectNodes(node_tree, principled_node.outputs[0], material_output_node.inputs[0])
    principled_node.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    principled_node.location = (200, 200)
    material_output_node.location = (600, 0)

    if node_structure == "BLENDER_BSDF":
        met_Suffix = properties.metallic_texture if properties.metallic_texture != "" else "_Metallic"
        roughness_Suffix = properties.roughness_texture if properties.roughness_texture != "" else "_Roughness"
        # Create image texture nodes
        normal_node = createNode(node_tree, 'ShaderNodeTexImage','NormalMap')
        normal_map_node = createNode(node_tree, 'ShaderNodeNormalMap','Normal')
        basecolor_node = createNode(node_tree, 'ShaderNodeTexImage','Color')
        metallic_node = createNode(node_tree, 'ShaderNodeTexImage','Metallic')
        roughness_node = createNode(node_tree, 'ShaderNodeTexImage','Roughness')

        #connect Nodes
        connectNodes(node_tree, basecolor_node.outputs['Color'], principled_node.inputs['Base Color'])
        connectNodes(node_tree, metallic_node.outputs['Color'], principled_node.inputs['Metallic'])
        connectNodes(node_tree, roughness_node.outputs['Color'], principled_node.inputs['Roughness'])
        connectNodes(node_tree, normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])
        connectNodes(node_tree, normal_node.outputs['Color'], normal_map_node.inputs['Color'])
        
        #position Nodes
        node_tree.nodes['Metallic'].location = (-400, -100)
        node_tree.nodes['Roughness'].location = (-100, -100)
        node_tree.nodes['Color'].location = (-400, 200)
        node_tree.nodes['NormalMap'].location = (-300, -400)
        node_tree.nodes['Normal'].location = (0, -350)

        #load textures
        norm_file_path = os.path.join(textures_dir, material_name + nm_Suffix + file_type)
        basecolor_file_path = os.path.join(textures_dir, material_name + col_Suffix + file_type)
        metallic_file_path = os.path.join(textures_dir, material_name + met_Suffix + file_type)
        roughness_file_path = os.path.join(textures_dir, material_name + roughness_Suffix + file_type)
        loadImageTexture(norm_file_path, normal_node, 'Non-Color')
        loadImageTexture(metallic_file_path, metallic_node, 'Non-Color')        
        loadImageTexture(roughness_file_path, roughness_node, 'Non-Color')
        loadImageTexture(basecolor_file_path, basecolor_node, 'sRGB')

        if gltf_settings:
            ao_node = createNode(node_tree, 'ShaderNodeTexImage','AO')
            connectNodes(node_tree, ao_node.outputs['Color'], gltf_node.inputs[0])
            node_tree.nodes['AO'].location = (-800, 0)
            gltf_node.location = (0,50)
    
    if node_structure == "ORM_GLB":
        orm_Suffix = properties.orm_texture if properties.orm_texture != "" else "_ORM"
        # Create Nodes for ORM GLB
        orm_node = createNode(node_tree, 'ShaderNodeTexImage','ORM')
        sep_color_node = createNode(node_tree, 'ShaderNodeSeparateColor','Separate Color')
        normal_node = createNode(node_tree, 'ShaderNodeTexImage','NormalMap')
        normal_map_node = node_tree.nodes.new('ShaderNodeNormalMap')
        basecolor_node = createNode(node_tree, 'ShaderNodeTexImage','Color')
        # Connect Nodes
        connectNodes(node_tree, basecolor_node.outputs[0], principled_node.inputs['Base Color'])
        connectNodes(node_tree, normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])
        connectNodes(node_tree, normal_node.outputs['Color'], normal_map_node.inputs['Color'])
        connectNodes(node_tree, orm_node.outputs[0], sep_color_node.inputs[0])
        connectNodes(node_tree, sep_color_node.outputs[2], principled_node.inputs['Metallic'])
        connectNodes(node_tree, sep_color_node.outputs[1], principled_node.inputs['Roughness'])
        if gltf_settings:
           connectNodes(node_tree, sep_color_node.outputs[0], gltf_node.inputs[0])

        # Set spacing
        orm_node.location = (-400, -100)
        sep_color_node.location = (-100, -100)
        basecolor_node.location = (-400, 200)
        normal_node.location = (-300, -400)
        normal_map_node.location = (0, -350)

        #Load images
        loadImageTexture(os.path.join(textures_dir, material_name + orm_Suffix + file_type),orm_node, 'Non-Color')
        loadImageTexture(os.path.join(textures_dir, material_name + nm_Suffix + file_type),normal_node, 'Non-Color')
        loadImageTexture(os.path.join(textures_dir, material_name + col_Suffix + file_type), basecolor_node, 'sRGB')

 
def createNode(node_tree, node_type, node_name):
    # Create a new node of the specified type
    newnode = node_tree.nodes.new(node_type)
    newnode.name = node_name
    return newnode        
 
def loadImageTexture(newPath, newNode, colorSpace):
     
     if os.path.exists(newPath):
         newNode.image = bpy.data.images.load(newPath)
         newNode.image.colorspace_settings.name = colorSpace
     else:
         message = "Missing Textures: {}".format(newPath)
         bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message), title="Error", icon='ERROR')
def connectNodes(node_tree, output_socket, input_socket):
    links = node_tree.links
    link = links.new(output_socket, input_socket)
    return link
    
  