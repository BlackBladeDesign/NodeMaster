import bpy
import json
from json import JSONEncoder
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..Operators.nm_operators import (connectNodes,createNode)

class NodeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bpy.types.Node):
            return obj.name
        if isinstance(obj, bpy.types.NodeSocket):
            return obj.identifier
        if isinstance(obj, bpy.types.NodeLink):
            return (obj.from_node.name, obj.from_socket.identifier,
                    obj.to_node.name, obj.to_socket.identifier)
        return super().default(obj)


def assign_unique_ids(node_tree):
    # Create a dictionary to store IDs for nodes and groups
    id_dict = {}
    current_id = 0

    for node in node_tree.nodes:
        # Assign an ID to each node
        id_dict[node.name] = current_id
        current_id += 1

    for node in node_tree.nodes:
        if node.type == 'GROUP':
            # If it's a group, assign an ID to the group
            id_dict[node.node_tree.name] = current_id
            current_id += 1

    return id_dict

def export_node_tree(node_tree, file_path):
    def export_node_tree_internal(node_tree,id_dict):
        data = {'nodes': [], 'links': []}

        node_dict = {}
        for node in node_tree.nodes:
            node_data = {
                'name': node.name,
                'label': node.label,
                'type': type(node).__name__,
                'location': (node.location.x, node.location.y),
                'inputs': [],
                'outputs': []
            }
            
            if isinstance(node, bpy.types.ShaderNodeTexImage) and node.image is not None:
                node_data['color_space'] = node.image.colorspace_settings.name
                
            if node.type == 'GROUP':
                # Handle group inputs and outputs separately
                node_data['name'] = node.node_tree.name

                for input_idx, input_socket in enumerate(node.inputs):
                    # Mark this input as active
                    node_data['inputs'].append((input_idx, input_socket.name, input_socket.type))

                for output_idx, output_socket in enumerate(node.outputs):
                    # Mark this output as active
                    node_data['outputs'].append((output_idx, output_socket.name, output_socket.type))
                
                # Recursively export nodes inside the group
                node_data['nodes'] = export_node_tree_internal(node.node_tree, id_dict)
            else:
                # Regular node inputs and outputs
                node_data['inputs'] = [(i, input.name, input.type) for i, input in enumerate(node.inputs)]
                node_data['outputs'] = [(i, output.name, output.type) for i, output in enumerate(node.outputs)]



            data['nodes'].append(node_data)
            node_dict[node.name] = node

        for link in node_tree.links:
            from_node = link.from_node
            from_socket = link.from_socket
            to_node = link.to_node
            to_socket = link.to_socket

            from_socket_idx = list(from_node.outputs).index(from_socket)
            to_socket_idx = list(to_node.inputs).index(to_socket)

            data['links'].append((from_node.name, from_socket_idx, to_node.name, to_socket_idx))

        return data

    id_dict = assign_unique_ids(node_tree)  # Dictionary to store unique IDs for nodes and groups
    data = export_node_tree_internal(node_tree, id_dict)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, cls=NodeEncoder, ensure_ascii=False, indent=4)

    return {'FINISHED'}



def import_node_tree_internal(node_tree, data):
    node_dict = {}
    for node_data in data['nodes']:
        node_type = node_data['type']
        node_name = node_data['name']
        node_label = node_data['label']
        node_location = node_data['location']
        node = node_tree.nodes.new(node_type)
        node.location = node_location
        node.name = node_name
        node.label = node_label
        
        if node_type == 'ShaderNodeTexImage':
            color_space = node_data.get('color_space')
            if color_space:
                node.image.colorspace_settings.name = color_space

        node_dict[node_data['name']] = node
        if node_type == 'ShaderNodeGroup':
            groupNodes = node_data['nodes']
            newGroup = bpy.data.node_groups.new(name=node.name, type='ShaderNodeTree')
            for groupInput in node_data['inputs']:
                input_name, input_type = groupInput[1], groupInput[2]
                try:
                    new_input = newGroup.inputs.new(input_type, input_name)
                except RuntimeError as e:
                    print(f"Error creating input socket for {input_name}: {e}")

            for groupOutput in node_data['outputs']:
                output_name, output_type = groupOutput[1], groupOutput[2]
                try:
                    new_output = newGroup.outputs.new(output_type, output_name)
                except RuntimeError as e:
                    print(f"Error creating output socket for {output_name}: {e}")

            import_node_tree_internal(newGroup, groupNodes)

    for link_data in data['links']:
        from_node = node_dict.get(link_data[0])
        to_node = node_dict.get(link_data[2])

        if from_node is not None and to_node is not None:
            try:
                from_socket = from_node.outputs[link_data[1]]
                to_socket = to_node.inputs[link_data[3]]
                node_tree.links.new(from_socket, to_socket)
            except (IndexError, RuntimeError) as e:
                print(f"Error creating link: {e}")

    return {'FINISHED'}

def import_node_tree(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    selected_material = bpy.context.active_object.active_material
    node_tree = selected_material.node_tree
    import_node_tree_internal(node_tree, data)

    return {'FINISHED'}


class ImportNodes(bpy.types.Operator, ImportHelper):
    bl_label = "Import Nodes"
    bl_idname = "node.importjson"
    filename_ext = ".json"

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        file_path = self.filepath
        import_node_tree(file_path)
        return {'FINISHED'}
class ExportNodes(bpy.types.Operator, ExportHelper):
    bl_label = "Export Nodes"
    bl_idname = "node.exportjson"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        node_tree = context.active_object.active_material.node_tree
        file_path = self.filepath
        export_node_tree(node_tree, file_path)
        return {'FINISHED'}