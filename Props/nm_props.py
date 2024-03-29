import bpy
from bpy.props import (EnumProperty, StringProperty, BoolProperty)
from bpy.types import (PropertyGroup, Operator)
import os

def populate_node_structure_enum_items(self, context):
    script_directory = os.path.dirname(__file__)  # Get the directory where the script is located
    folder_path = os.path.abspath(os.path.join(script_directory, "../json/NodeStructures"))  # Combine with the subfolder name

    items = []

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                # Remove the .json extension
                display_name = os.path.splitext(filename)[0]
                items.append((filename, display_name, ''))

    return items

class NodeMasterProperties(bpy.types.PropertyGroup):

    loadImageNodes : bpy.props.BoolProperty(
        name="Load Image Texture Nodes",
        description="Enabled or disable to add or ignore adding image textures nodes.",
        default=True
    )
    clearNodes : bpy.props.BoolProperty(
        name="clear all nodes on load/reload",
        description="Clears all nodes in selected node tree prior to building new structure",
        default=True
    )
    loadTextures : bpy.props.BoolProperty(
        name="Load Image assets",
        description="Enabled or disable to load image textures assets. Helpful for if you just want the node structure without images.",
        default=True
    )
    image_file_type: bpy.props.EnumProperty(
        name="Image File Type",
        description="Select the image file type.",
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
        description="Apply to the selected material, all materials attatched to the selected object, or all materials for all visible objects.",
        items=(
            ("SELECTED", "Selected", ""),
            ("ALL_ATTACHED", "All Attached", ""),
            ("ALL_VISIBLE", "All Visible", ""),
        ),
        default="SELECTED"
    )

    apply_propertyTo: bpy.props.EnumProperty(
        name="Apply Property To",
        description="Apply Custom Property to the selected material, Objects, or Both",
        items=(
            ("Material", "Materials", ""),
            ("Object", "Objecs", ""),
            ("ALL", "All", ""),
        ),
        default="Material"
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
    orm_texture: bpy.props.StringProperty(
        name="ORM Texture",
        default="_ORM"
    )
    roughness_texture: bpy.props.StringProperty(
        name="Roughness",
        default="_Roughness"
    )
    metallic_texture: bpy.props.StringProperty(
        name="Metallic",
        default="_Metallic"
    )
    texturePath: bpy.props.StringProperty(
        name="Path",
        default = "/Textures"
    )
    customProperty: bpy.props.StringProperty(
        name="Custom Property",
        default = "hidden"
    )
    custom_property_val: bpy.props.FloatProperty(
        name="Custom Property Value",
        default=0.0
    )
    node_structure: bpy.props.EnumProperty(
        name="Node Structure",
        description="Select the node structure to create, read about each on the github page.",
        items=populate_node_structure_enum_items,
        default=None,
    )




