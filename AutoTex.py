import bpy
import os
import bpy

from bpy.props import EnumProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty

bl_info = {
    "name": "AutoTex",
    "description": "Auto loads ORM, Normal map, and basecolor textures and builds a node tree, or load from a specified path",
    "author": "BlackBladeDesign",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "Shader Editor > Options Panel > AutoTex",
    "category": "Shader"}



class AutoTexPanel(bpy.types.Panel):
    """Creates a new tab in the shader editor options panel"""
    bl_label = "AutoTex"
    bl_idname = "NODE_PT_autotex"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "AutoTex"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator("node.autoload", text="Auto Load")
        row.operator("node.loadfrompath", text="Load From Path")
        
        col = layout.column(align=True)
        col.prop(context.scene.auto_tex_props, "apply_to", text="Apply To")
        col.prop(context.scene.auto_tex_props, "image_file_type", text="Image File Type")
        col.prop(context.scene.auto_tex_props, "node_structure", text="Node Structure")


class AutoTexProperties(bpy.types.PropertyGroup):
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
        ("PBR_METALLIC_ROUGHNESS", "PBR (Metallic Roughness)", ""),
        ("DOCUMENT_CHANNELS_NORMAL_AO_NO_ALPHA", "Document Channels + Normal + AO (No Alpha)", ""),
        ("DOCUMENT_CHANNELS_NORMAL_AO_WITH_ALPHA", "Document Channels + Normal + AO (With Alpha)", ""),
    ),
    default="ORM_GLB"
)
def connectNodes(node_tree, output_socket, input_socket):
    links = node_tree.links
    link = links.new(output_socket, input_socket)
    return link
    
def loadImageTexture(newPath, newNode, colorSpace):
     
     if os.path.exists(newPath):
         newNode.image = bpy.data.images.load(newPath)
         newNode.image.colorspace_settings.name = colorSpace
     else:
          print("Missing image files for material")
          
def setNodes(textures_dir):    
    auto_tex_props = bpy.context.scene.auto_tex_props
    apply_to = auto_tex_props.apply_to  # add this line
    if apply_to == "ALL_VISIBLE":
        # Apply to all materials
        visible_objects = [obj for obj in bpy.context.scene.objects if obj.visible_get()]
        for obj in visible_objects:
            for material_slot in obj.material_slots:
                mat = material_slot.material
                node_tree = mat.node_tree
                nTreeSetup(node_tree, textures_dir, mat.name)
    elif apply_to == "ALL_ATTACHED":
        # Apply to all materials attached to the active object
        obj = bpy.context.active_object
        if obj:
            for material_slot in obj.material_slots:
                mat = material_slot.material
                node_tree = mat.node_tree
                nTreeSetup(node_tree, textures_dir, mat.name)
    else:
        # Get the current active node tree
        node_tree = bpy.context.active_object.active_material.node_tree
        material_name = bpy.context.active_object.active_material.name
        nTreeSetup(node_tree, textures_dir, material_name)
        
 
def nTreeSetup(node_tree, textures_dir, material_name):
    file_type = bpy.context.scene.auto_tex_props.image_file_type
    
    # Clear all existing nodes
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)
    # Create nodes
    principled_node = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    image_node = node_tree.nodes.new(type='ShaderNodeTexImage')
    sep_color_node = node_tree.nodes.new(type='ShaderNodeSeparateColor')
    norm_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
    norm_image_node = node_tree.nodes.new(type='ShaderNodeTexImage')
    basecolor_node = node_tree.nodes.new(type='ShaderNodeTexImage')
    # Set the name of the nodes
    principled_node.name = 'Principled BSDF'
    norm_image_node.name = 'NormalMap'
    sep_color_node.name = 'Separate Color'
    image_node.name = 'ORM'
    basecolor_node.name = 'Color'
    # Add a new Material Output node
    material_output_node = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    node_tree.links.new(principled_node.outputs[0], material_output_node.inputs[0])
    # Set the spacing between nodes
    node_tree.nodes['ORM'].location = (-400, -100)
    node_tree.nodes['Separate Color'].location = (-100, -100)
    node_tree.nodes['Color'].location = (-400, 200)
    node_tree.nodes['NormalMap'].location = (-300, -400)
    node_tree.nodes['Normal Map'].location = (0, -350)
    principled_node.location = (200, 200)
    material_output_node.location = (600, 0)
   # Find the "glTF Settings" node
    gltf_settings = None
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
    # Connect the nodes together
    connectNodes(node_tree, image_node.outputs[0], sep_color_node.inputs[0])
    connectNodes(node_tree, sep_color_node.outputs[2], principled_node.inputs['Metallic'])
    connectNodes(node_tree, sep_color_node.outputs[1], principled_node.inputs['Roughness'])
    connectNodes(node_tree, basecolor_node.outputs[0], principled_node.inputs['Base Color'])
    connectNodes(node_tree, norm_node.outputs[0], principled_node.inputs['Normal'])
    connectNodes(node_tree, norm_image_node.outputs[0], norm_node.inputs['Color'])  
    connectNodes(node_tree, sep_color_node.outputs[0], gltf_node.inputs[0])
    # Set the image file path for nodes
    orm_file_path = os.path.join(textures_dir, material_name + '_ORM'+file_type)
    color_file_path = os.path.join(textures_dir, material_name + '_Color' + file_type)   
    norm_file_path = os.path.join(textures_dir, material_name + '_NormalMap' + file_type)
    loadImageTexture(orm_file_path,image_node, 'Non-Color')
    loadImageTexture(color_file_path, basecolor_node, 'sRGB')
    loadImageTexture(norm_file_path,norm_image_node, 'Non-Color')
    
class ShaderAutoLoad(bpy.types.Operator):
    """Auto-load textures for all nodes in the shader"""
    bl_label = "Auto Load"
    bl_idname = "node.autoload"

    def execute(self, context):
        blend_dir = os.path.dirname(bpy.data.filepath)
        parent_dir = os.path.dirname(blend_dir)
        texturesFolder = os.path.join(parent_dir, 'Textures')
        setNodes(texturesFolder)
        
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
            textures_dir = os.path.abspath(os.path.dirname(self.filepath))
            setNodes(textures_dir)

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
