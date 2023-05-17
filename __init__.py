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
    "developer": "BlackBladeDesign",
    "version": (1, 3),
    "blender": (3, 5, 0),
    "location": "Shader Editor > Options Panel > NodeMaster",
    "category": "Shader",
    "warning": "Still under development. Be sure to save inbetween large operations to avoid lost progress",
    "doc_url": "https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/blob/6cf5bd2d70def1a228a64453e71590976ac718ce/README.md",
    "tracker_url": "https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/issues",
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