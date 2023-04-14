import bpy
from bpy.props import PointerProperty
from bpy.props import (EnumProperty, StringProperty, BoolProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)
from .Panel.nm_panel import AutoTexPanel
from .Operators.nm_operators import AutoLoad, LoadFromPath
from .Props.nm_props import AutoTexProperties


bl_info = {
    "name": "NodeMaster",
    "description": "Streamlines and automates texture loading and node creation",
    "author": "BlackBladeDesign",
    "version": (1, 2),
    "blender": (3, 5, 0),
    "location": "Shader Editor > Options Panel > NodeMaster",
    "category": "Shader"
}


classes = [
    AutoTexProperties,
    AutoTexPanel,
    AutoLoad,
    LoadFromPath,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.auto_tex_props = PointerProperty(type=AutoTexProperties)
    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.auto_tex_props