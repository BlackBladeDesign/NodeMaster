import bpy
from bpy.types import Panel
from bpy.props import EnumProperty, StringProperty

from ..Operators.nm_operators import (LoadFromPath, AutoLoad,AddProperty, ExportTransforms)
from ..Props.nm_props import NodeMasterProperties


class NodeMasterPanel(bpy.types.Panel):
    """Creates a new tab in the shader editor options panel"""
    bl_label = "NodeMaster"
    bl_idname = "NODE_PT_nodemaster"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "NodeMaster"

    def draw(self, context):
        layout = self.layout
        # Main Controls
        row = layout.column()
        row.label(text="Set your path, load textures & nodes")
        row.operator("node.autoload", text="Load / Reload")
        row.operator("node.loadfrompath", text="Set Texture Path")
        row.prop(context.scene.nm_props, "apply_to", text=" Apply To")


class nodeStructurePanel(bpy.types.Panel):
    bl_label = "Node Structure Settings"
    bl_idname = "NODE_PT_nodemaster_nsSettings"
    bl_category = "NodeMaster"
    bl_parent_id = "NODE_PT_nodemaster"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        # Sub-panel for material settings
        layout = self.layout
        # Main buttons and path
        row = layout.column()
        row.prop(context.scene.nm_props, "loadImageNodes", text="Load Image Nodes")
        row.prop(context.scene.nm_props, "clearNodes", text="Clear All Nodes")    
        if context.scene.nm_props.loadImageNodes:
            row.prop(context.scene.nm_props, "loadTextures", text="Load Image Assets")  
        row.prop(context.scene.nm_props, "node_structure", text=" Node Structure")
        row.label(text="")

        

class fileSettingsPanel(bpy.types.Panel):
    bl_label = "File Settings"
    bl_idname = "NODE_PT_nodemaster_fileSettings"
    bl_category = "NodeMaster"
    bl_parent_id = "NODE_PT_nodemaster"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'

    @classmethod
    def poll(cls, context):
        return context.scene.nm_props.loadTextures

    def draw(self, context):
        # Sub-panel for material settings
        layout = self.layout
        # Main buttons and path
        row = layout.column()
        row.prop(context.scene.nm_props, "texturePath", text="Texture Path")
        row.prop(context.scene.nm_props, "image_file_type", text=" File Type")

class nmToolsPanel(bpy.types.Panel):        
    bl_label = "Tools"
    bl_idname = "NODE_PT_nodemaster_tools"
    bl_category = "NodeMaster"
    bl_parent_id = "NODE_PT_nodemaster"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        layout = self.layout
        # Main Controls
        row = layout.column()
        row.operator("node.matcleaner", text="Clean Duplicate Materials")
        row.operator("node.imgcleaner", text="Clean Duplicate Images")
        row.operator("node.importjson", text="Load Node Tree (JSON)")
        row.operator("node.exportjson", text="Export Node Tree (JSON)")

        row.operator("node.addproperty", text="Add Custom Property")
        row.prop(context.scene.nm_props, "apply_propertyTo", text=" Apply Property To")
        row.prop(context.scene.nm_props, "customProperty", text="Custom Property")
        row.prop(context.scene.nm_props, "custom_property_val", text="Custom Property Value")
        
        row.operator("node.exporttransforms", text="Export Transforms for Babylon.js")
