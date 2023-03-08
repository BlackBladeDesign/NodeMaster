bl_info = {
    "name": "AutoTex",
    "description": "Auto loads ORM, Normal map, and basecolor textures and builds a node tree, or load from a specified path",
    "author": "BlackBladeDesign",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "Shader Editor > Options Panel > AutoTex",
    "category": "Shader"}

import bpy
import os
from bpy.props import StringProperty

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

def setNodes(textures_dir):
        # Get the current active node tree
        node_tree = bpy.context.active_object.active_material.node_tree

        # Clear all existing nodes
        for node in node_tree.nodes:
            node_tree.nodes.remove(node)

        # Create path for textures located in parent directory with selected material name
        material_name = bpy.context.active_object.active_material.name
       
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

        # Connect the nodes together
        node_tree.links.new(image_node.outputs[0], sep_color_node.inputs[0])
        node_tree.links.new(sep_color_node.outputs[2], principled_node.inputs['Metallic'])
        node_tree.links.new(sep_color_node.outputs[1], principled_node.inputs['Roughness'])
        node_tree.links.new(basecolor_node.outputs[0], principled_node.inputs['Base Color'])
        node_tree.links.new(norm_node.outputs[0], principled_node.inputs['Normal'])
        node_tree.links.new(norm_image_node.outputs[0], norm_node.inputs['Color'])
        

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
       

        # Set the image file path for nodes
        image_node.image = bpy.data.images.load(os.path.join(textures_dir, material_name + '_ORM.jpg'))
        basecolor_node.image = bpy.data.images.load(os.path.join(textures_dir, material_name + '_Color.jpg'))
        norm_image_node.image = bpy.data.images.load(os.path.join(textures_dir, material_name + '_NormalMap.jpg'))

        # Set the color space of normal and ORM
        norm_image_node.image.colorspace_settings.name = 'Non-Color'
        image_node.image.colorspace_settings.name = 'Non-Color'
        
      
         # Find the "glTF Settings" node
        gltf_settings = None
        for node in bpy.data.node_groups:
            if node.name == "glTF Material Output":
                gltf_settings = node
                break

        # If the "glTF Settings" node is found, add it to the node tree
        if gltf_settings:
            node = node_tree.nodes.new("ShaderNodeGroup")
            node.node_tree = gltf_settings
            node_tree.links.new(sep_color_node.outputs[0], node.inputs[0])
        else : 
            glTF_settings.node_tree = bpy.data.node_groups.new(name='glTF Settings', type='ShaderNodeTree')
            glTF_input = glTF_settings.node_tree.nodes.new(type='NodeGroupInput')
            glTF_input.name = 'Occlusion'
            glTF_settings.node_tree.inputs.new('NodeSocketVector', 'Occlusion')
            glTF_output = glTF_settings.node_tree.nodes.new(type='NodeGroupOutput')
            node_tree.links.new(sep_color_node.outputs[0], glTF_settings.inputs[0])
                
        
        

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
    bpy.utils.register_class(AutoTexPanel)
    bpy.utils.register_class(ShaderAutoLoad)
    bpy.utils.register_class(ShaderLoadFromPath)
    bpy.types.Scene.first_time_run = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.textures_dir = bpy.props.StringProperty(
        name="Textures Directory",
        subtype='DIR_PATH',
        default='')


def unregister():
    del bpy.types.Scene.first_time_run
    bpy.utils.unregister_class(AutoTexPanel)
    bpy.utils.unregister_class(ShaderAutoLoad)
    bpy.utils.unregister_class(ShaderLoadFromPath)
    del bpy.types.Scene.textures_dir

if __name__ == "__main__":
    register()
