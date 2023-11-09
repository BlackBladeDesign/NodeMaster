import bpy
from bpy.props import PointerProperty
from bpy.props import (EnumProperty, StringProperty, BoolProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)
from .Panel.nm_panel import NodeMasterPanel, texSuffixPanel, fileSettingsPanel, nodeStructurePanel, nmToolsPanel
from .Operators.nm_operators import AutoLoad, LoadFromPath, ImportNodes, ExportNodes, AddProperty, ExportTransforms
from .Props.nm_props import NodeMasterProperties
from .Operators.nm_matCleanup import matCleanup, imgCleanup
import bpy
from bpy.types import Operator, AddonPreferences, Panel
from bpy.props import StringProperty


bl_info = {
    "name": "NodeMaster",
    "description": "Streamlines and automates texture loading and node creation",
    "author": "BlackBladeDesign",
    "version": (1, 4),
    "blender": (3, 5, 0),
    "location": "Shader Editor > Options Panel > NodeMaster",
    "category": "Shader",
    "warning": "Still under development. Be sure to save in-between large operations to avoid lost progress!",
    "doc_url": "https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/blob/6cf5bd2d70def1a228a64453e71590976ac718ce/README.md",
    "tracker_url": "https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/issues",
    "support": "COMMUNITY",
    "paypal_donate_link": "https://www.paypal.com/donate/?hosted_button_id=X44329R2WEKGS"
}

class OpenPayPalDonateLink(Operator):
    bl_idname = "preferences.open_paypal_donate_link"
    bl_label = "Donate (PayPal)"

    def execute(self, context):
        bpy.ops.wm.url_open(url=bl_info["paypal_donate_link"])
        return {'FINISHED'}

def show_tooltips(self, context):
    preferences = context.preferences.addons[__name__].preferences
    return preferences.show_tooltips

def set_tooltips(self, context, value):
    preferences = context.preferences.addons[__name__].preferences
    preferences.show_tooltips = value

bpy.types.AddonPreferences.show_tooltips = BoolProperty(
    name="Show Tooltips",
    description="Enable/disable tooltips",
    get=show_tooltips,
    set=set_tooltips,
)

def draw_addon_info(self, context):
    layout = self.layout
    layout.label(text="Addon Information:")
    layout.label(text=f"Name: {bl_info['name']}")
    layout.label(text=f"Description: {bl_info['description']}")
    layout.label(text=f"Author: {bl_info['author']}")
    layout.label(text=f"Version: {bl_info['version'][0]}.{bl_info['version'][1]}")
    layout.label(text=f"Blender Version: {bl_info['blender'][0]}.{bl_info['blender'][1]}.{bl_info['blender'][2]}")
    layout.label(text=f"Category: {bl_info['category']}")
    layout.label(text=f"Warning: {bl_info['warning']}")
    layout.separator()
    
    # Add a label for "Support" and a button to open the PayPal link
    layout.label(text="Support:")
    row = layout.row()
    row.label(text="If you find this addon useful, you can support the developer:")
    row.operator("preferences.open_paypal_donate_link")
    
    layout.operator("preferences.addon_enable").module = __name__
    layout.operator("preferences.addon_disable").module = __name__
    layout.operator("preferences.addon_refresh")
    layout.operator("preferences.addon_filter")
    layout.prop(context.preferences.addons[__name__].preferences, "show_tooltips")
    row = layout.row(align=True)
    row.operator("preferences.addon_expand", text="Expand All").action = 'EXPAND'
    row.operator("preferences.addon_expand", text="Collapse All").action = 'COLLAPSE'

bpy.types.AddonPreferences.draw = draw_addon_info

classes = [
    NodeMasterProperties,
    NodeMasterPanel,
    AutoLoad,
    LoadFromPath,
    AddProperty,
    ImportNodes,
    ExportNodes,
    ExportTransforms,
    nodeStructurePanel,
    fileSettingsPanel,
    nmToolsPanel,
    matCleanup,
    imgCleanup,
    OpenPayPalDonateLink,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.nm_props = PointerProperty(type=NodeMasterProperties)
    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.nm_props
