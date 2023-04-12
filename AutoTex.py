import os
import bpy

from bpy.props import (EnumProperty, StringProperty, BoolProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)

bl_info = {
    "name": "NodeMaster",
    "description": "Streamlines texture loading and node creation",
    "author": "BlackBladeDesign",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "Shader Editor > Options Panel > AutoTex",
    "category": "Shader"}

class AutoTexProperties(bpy.types.PropertyGroup):
    
    gltf_Node : bpy.props.BoolProperty(
        name="Add glTF Node",
        description="Create a GLB/GLTF Output node, connect AO or ORM red channel to it for Ambient Occlusion",
        default=False
    )
    texCoord : bpy.props.BoolProperty(
        name="Add Texture Coord",
        description="Add Texture Coordinate node with mapping",
        default=False
    )
    displacement : bpy.props.BoolProperty(
        name="Add Displacement",
        description="Add a Displacement node, connect to material output",
        default=False
    )
    image_file_type: bpy.props.EnumProperty(
        name="Image File Type",
        description="Select the image file type",
        items=(
            (".jpg", "JPEG", ""),
            (".png", "PNG", ""),
            (".bmp", "BMP", ""),
            (".tga", "Targa", "")
        ),
        default=".jpg"
    )
    
    apply_to: bpy.props.EnumProperty(
        name="Apply To",
        description="Select the option to apply to",
        items=(
            ("SELECTED", "Selected", ""),
            ("ALL_ATTACHED", "All Attached", ""),
            ("ALL_VISIBLE", "All Visible", ""),
        ),
        default="SELECTED"
    )
    node_structure: bpy.props.EnumProperty(
        name="Node Structure",
        description="Select the node structure",
        items=(
            ("ORM_GLB", "ORM - GLB", ""),
            ("BLENDER_BSDF", "Blender (BSDF)", ""),
            #("PBR_METALLIC_ROUGHNESS", "PBR (Metallic Roughness)", ""),
            #("DOCUMENT_CHANNELS_NORMAL_AO_NO_ALPHA", "Document Channels + Normal + AO (No Alpha)", ""),
            #("DOCUMENT_CHANNELS_NORMAL_AO_WITH_ALPHA", "Document Channels + Normal + AO (With Alpha)", ""),
        ),
        default="ORM_GLB"
    )
        # Add two new StringProperty properties for texture names
    normal_map: bpy.props.StringProperty(
        name="Normal Map",
        default="_Normal"
    )
    base_color: bpy.props.StringProperty(
        name="Base Color",
        default="_Color"
    )
    texturePath: bpy.props.StringProperty(
        name="Path",
        default = "/Textures"
    )

        

class AutoTexPanel(bpy.types.Panel):
    """Creates a new tab in the shader editor options panel"""
    bl_label = "AutoTex"
    bl_idname = "NODE_PT_autotex"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "AutoTex"

    def draw(self, context):
        layout = self.layout
        row = layout.column()
        row.label(text="Set your path, load textures & nodes")
        row.operator("node.autoload", text="Load / Reload")
        row.operator("node.loadfrompath", text="Set Texture Path")
        row.label(text="")
        row.prop(context.scene.auto_tex_props, "texturePath", text="Texture Path")
        row.label(text="_______________________________________________________________")
        row.label(text="Material Settings:")
       
        row.prop(context.scene.auto_tex_props, "gltf_Node", text="GLTF/GLB Output")
        row.prop(context.scene.auto_tex_props, "displacement", text="Displacment")
        row.label(text="")
        row.prop(context.scene.auto_tex_props, "apply_to", text=" Apply To")
        row.prop(context.scene.auto_tex_props, "image_file_type", text=" File Type")
        row.prop(context.scene.auto_tex_props, "node_structure", text=" Node Structure") 
        

        row.label(text="_______________________________________________________________")
        row.label(text="Texture suffixes:")
        row.prop(context.scene.auto_tex_props, "normal_map", text="- Normal Map")
        row.prop(context.scene.auto_tex_props, "base_color", text="- Base Color")
        
        

def connectNodes(node_tree, output_socket, input_socket):
    links = node_tree.links
    link = links.new(output_socket, input_socket)
    return link
    
def loadImageTexture(newPath, newNode, colorSpace):
     
     if os.path.exists(newPath):
         newNode.image = bpy.data.images.load(newPath)
         newNode.image.colorspace_settings.name = colorSpace
     else:
         message = "Missing image file for material: {}".format(newPath)
         bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message), title="Error", icon='ERROR')
          
def setNodes(textures_dir, properties):    
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
        obj = bpy.context.active_object
        if obj:
            for material_slot in obj.material_slots:
                mat = material_slot.material
                node_tree = mat.node_tree
                nTreeSetup(node_tree, textures_dir, mat.name, properties)
    else:
        # Get the current active material
        mat = bpy.context.active_object.active_material
        node_tree = mat.node_tree
        material_name = mat.name
        nTreeSetup(node_tree, textures_dir, material_name, properties)
 
def nTreeSetup(node_tree, textures_dir, material_name, properties):
    file_type =properties.image_file_type
    node_structure = properties.node_structure
    nm_Suffix = properties.normal_map if properties.normal_map != "" else "_Normal"
    col_Suffix = properties.base_color if properties.base_color != "" else "_Color"
    
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)
        
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
    principled_node = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    material_output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    principled_node.name = 'Principled BSDF'
    principled_node.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    principled_node.location = (200, 200)
    material_output_node.location = (600, 0)
    connectNodes(node_tree, principled_node.outputs[0], material_output_node.inputs[0])
    
    
    if node_structure == "ORM_GLB":
        # Find the "glTF Settings" node
        # Create Nodes for ORM GLB
        image_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        sep_color_node = node_tree.nodes.new(type='ShaderNodeSeparateColor')
        norm_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
        norm_image_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        basecolor_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        # Set the name of the nodes
        basecolor_node.name = 'Color'
        norm_image_node.name = 'NormalMap'
        sep_color_node.name = 'Separate Color'
        image_node.name = 'ORM'
        # Set spacing
        node_tree.nodes['ORM'].location = (-400, -100)
        node_tree.nodes['Separate Color'].location = (-100, -100)
        node_tree.nodes['Color'].location = (-400, 200)
        node_tree.nodes['NormalMap'].location = (-300, -400)
        node_tree.nodes['Normal Map'].location = (0, -350)
        principled_node.location = (200, 200)
        material_output_node.location = (600, 0)
        # Connect Nodes
        if gltf_settings != None:
           connectNodes(node_tree, sep_color_node.outputs[0], gltf_node.inputs[0])
        connectNodes(node_tree, basecolor_node.outputs[0], principled_node.inputs['Base Color'])
        connectNodes(node_tree, norm_node.outputs[0], principled_node.inputs['Normal'])
        connectNodes(node_tree, norm_image_node.outputs[0], norm_node.inputs['Color'])  
        connectNodes(node_tree, image_node.outputs[0], sep_color_node.inputs[0])
        connectNodes(node_tree, sep_color_node.outputs[2], principled_node.inputs['Metallic'])
        connectNodes(node_tree, sep_color_node.outputs[1], principled_node.inputs['Roughness'])
        
        

        loadImageTexture(os.path.join(textures_dir, material_name + '_ORM' + file_type),image_node, 'Non-Color')
        loadImageTexture(os.path.join(textures_dir, material_name + nm_Suffix + file_type),norm_image_node, 'Non-Color')
        loadImageTexture(os.path.join(textures_dir, material_name + col_Suffix + file_type), basecolor_node, 'sRGB')   
         
    elif node_structure == "BLENDER_BSDF":
        
        norm_file_path = os.path.join(textures_dir, material_name + nm_Suffix + file_type)
        basecolor_file_path = os.path.join(textures_dir, material_name + col_Suffix + file_type)
        metallic_file_path = os.path.join(textures_dir, material_name + '_Metallic' + file_type)
        roughness_file_path = os.path.join(textures_dir, material_name + '_Roughness' + file_type)

        # Create image texture nodes
        normal_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        normal_map_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
        basecolor_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        metallic_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        roughness_node = node_tree.nodes.new(type='ShaderNodeTexImage')
        
        loadImageTexture(norm_file_path, normal_node, 'Non-Color')
        loadImageTexture(metallic_file_path, metallic_node, 'Non-Color')        
        loadImageTexture(roughness_file_path, roughness_node, 'Non-Color')
        loadImageTexture(basecolor_file_path, basecolor_node, 'sRGB')


        connectNodes(node_tree, basecolor_node.outputs['Color'], principled_node.inputs['Base Color'])
        connectNodes(node_tree, metallic_node.outputs['Color'], principled_node.inputs['Metallic'])
        connectNodes(node_tree, roughness_node.outputs['Color'], principled_node.inputs['Roughness'])
        connectNodes(node_tree, normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])
        connectNodes(node_tree, normal_node.outputs['Color'], normal_map_node.inputs['Color'])
        
        basecolor_node.name = 'Color'
        normal_node.name = 'NormalMap'
        normal_map_node.name = 'Normal'
        metallic_node.name = 'Metallic'
        roughness_node.name = 'Roughness'
        
        node_tree.nodes['Metallic'].location = (-400, -100)
        node_tree.nodes['Roughness'].location = (-100, -100)
        node_tree.nodes['Color'].location = (-400, 200)
        node_tree.nodes['NormalMap'].location = (-300, -400)
        node_tree.nodes['Normal'].location = (0, -350)
 
class ShaderAutoLoad(bpy.types.Operator):
    """Auto-load textures for all nodes in the shader"""
    bl_label = "Auto Load"
    bl_idname = "node.autoload"
    
    def execute(self, context):
        blend_dir = os.path.dirname(bpy.data.filepath)
        parent_dir = os.path.dirname(blend_dir)
        texturesFolder = os.path.join(parent_dir, 'Textures')
        setPathFolder = bpy.context.scene.auto_tex_props.texturePath
        
        if setPathFolder and setPathFolder != "/Textures" and os.path.exists(bpy.path.abspath(setPathFolder)):
           setNodes(bpy.context.scene.auto_tex_props.texturePath,bpy.context.scene.auto_tex_props)
        else:
            setNodes(texturesFolder,bpy.context.scene.auto_tex_props)
        
        return {'FINISHED'}
    
class ShaderLoadFromPath(bpy.types.Operator):
    """Load textures from a specified path"""
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
            setNodes(textures_dir, bpy.context.scene.auto_tex_props)

            return {'FINISHED'}
    


def register():
    bpy.utils.register_class(AutoTexProperties)
    bpy.types.Scene.auto_tex_props = bpy.props.PointerProperty(type=AutoTexProperties)
    bpy.utils.register_class(AutoTexPanel)
    bpy.utils.register_class(ShaderAutoLoad)
    bpy.utils.register_class(ShaderLoadFromPath)
    bpy.types.Scene.textures_dir = bpy.props.StringProperty(
        name="Textures Directory",
        subtype='DIR_PATH',
        default='')

def unregister():
    bpy.utils.unregister_class(AutoTexProperties)
    del bpy.types.Scene.auto_tex_props
    bpy.utils.unregister_class(AutoTexPanel)
    bpy.utils.unregister_class(ShaderAutoLoad)
    bpy.utils.unregister_class(ShaderLoadFromPath)

if __name__ == "__main__":
    register()