import bpy
from bpy.props import PointerProperty
from bpy.props import (EnumProperty, StringProperty, BoolProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)
from .Panel.nm_panel import NodeMasterPanel, matSettingsPanel, texSuffixPanel, fileSettingsPanel, nodeStructurePanel, nmToolsPanel
from .Operators.nm_operators import AutoLoad, LoadFromPath
from .Props.nm_props import NodeMasterProperties
from .Operators.nm_nodeEXP import ImportNodes, ExportNodes
from .Operators.nm_matCleanup import matCleanup, imgCleanup



bl_info = {
    "name": "NodeMaster",
    "description": "Streamlines and automates texture loading and node creation",
    "author": "BlackBladeDesign",
    "version": (1, 3),
    "blender": (3, 5, 0),
    "location": "Shader Editor > Options Panel > NodeMaster",
    "category": "Shader"
}
  


classes = [
    NodeMasterProperties,
    NodeMasterPanel,
    AutoLoad,
    LoadFromPath,
    ImportNodes,
    ExportNodes,
    nodeStructurePanel,
    fileSettingsPanel,
    matSettingsPanel,
    texSuffixPanel,
    nmToolsPanel,
    matCleanup,
    imgCleanup
    
    
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.nm_props = PointerProperty(type=NodeMasterProperties)
    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.nm_props