import bpy
from bpy.props import (EnumProperty, StringProperty, BoolProperty)
from bpy.types import (PropertyGroup, Operator)
import os

class NodeMasterProperties(bpy.types.PropertyGroup):
    

    loadImageNodes : bpy.props.BoolProperty(
        name="Load Image Texture Nodes",
        description="Enabled or disable to add or ignore adding image textures nodes.",
        default=True
    )
    loadTextures : bpy.props.BoolProperty(
        name="Load Image assets",
        description="Enabled or disable to load image textures assets. Helpful for if you just want the node structure without images.",
        default=True
    )
    gltf_Node : bpy.props.BoolProperty(
        name="Add glTF Node",
        description="Create a GLB/GLTF Output node, connect AO or ORM red channel to it for Ambient Occlusion.",
        default=False
    )
    texCoord : bpy.props.BoolProperty(
        name="Add Texture Coord",
        description="Add Texture Coordinate node with mapping.",
        default=False
    )
    displacement : bpy.props.BoolProperty(
        name="Add Displacement",
        description="Add a Displacement node, connect to material output.",
        default=False
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
    node_structure: bpy.props.EnumProperty(
        name="Node Structure",
        description="Select the node structure to create, read about each on the github page.",
        items=(
            ("ORM_GLB", "ORM - GLB", "ORM GLB (Custom)"),
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



