import bpy
from bpy.types import Panel
from bpy.props import EnumProperty, StringProperty
from ..Operators.nm_operators import (LoadFromPath, AutoLoad)
from ..Props.nm_props import AutoTexProperties

class AutoTexPanel(bpy.types.Panel):
    """Creates a new tab in the shader editor options panel"""
    bl_label = "NodeMaster"
    bl_idname = "NODE_PT_autotex"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "NodeMaster"

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
        
        
