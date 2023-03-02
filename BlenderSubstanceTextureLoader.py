import bpy
import os

# Generated with ChatGPT by BlackBladeDesign

# Get the current active node tree
node_tree = bpy.context.active_object.active_material.node_tree

# Clear all existing nodes
for node in node_tree.nodes:
    node_tree.nodes.remove(node)

# Create path for textures located in parent directory with selected material name
glTF_settings = node_tree.nodes.new(type='ShaderNodeGroup')
blend_dir = os.path.dirname(bpy.data.filepath)
parent_dir = os.path.dirname(blend_dir)
textures_dir = os.path.join(parent_dir, 'Textures')
material_name = bpy.context.active_object.active_material.name


# Create nodes
principled_node = node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
image_node = node_tree.nodes.new(type='ShaderNodeTexImage')
sep_color_node = node_tree.nodes.new(type='ShaderNodeSeparateRGB')
norm_node = node_tree.nodes.new(type='ShaderNodeNormalMap')
norm_image_node = node_tree.nodes.new(type='ShaderNodeTexImage')
basecolor_node = node_tree.nodes.new(type='ShaderNodeTexImage')
glTF_settings.node_tree = bpy.data.node_groups.new(name='glTF Settings', type='ShaderNodeTree')
glTF_input = glTF_settings.node_tree.nodes.new(type='NodeGroupInput')
glTF_input.name = 'Occlusion'
glTF_settings.node_tree.inputs.new('NodeSocketVector', 'Occlusion')
glTF_output = glTF_settings.node_tree.nodes.new(type='NodeGroupOutput')

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
node_tree.links.new(sep_color_node.outputs[0], glTF_settings.inputs['Occlusion'])

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
glTF_output.location

# Set the image file path for nodes
image_node.image = bpy.data.images.load(os.path.join(textures_dir, material_name + '_ORM.jpg'))
basecolor_node.image = bpy.data.images.load(os.path.join(textures_dir, material_name + '_Color.jpg'))
norm_image_node.image = bpy.data.images.load(os.path.join(textures_dir, material_name + '_NormalMap.jpg'))



# Set the color space of normal and ORM
norm_image_node.image.colorspace_settings.name = 'Non-Color'
image_node.image.colorspace_settings.name = 'Non-Color'
