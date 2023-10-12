import bpy
import json
from json import JSONEncoder
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..Operators.nm_operators import (connectNodes,createNode, errorGen)

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
    def export_node_tree_internal(node_tree, id_dict):
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
                    input_name = input_socket.name
                    input_type = input_socket.bl_idname

                    input_value = None  # Default value for input value

                    if hasattr(input_socket, 'default_value'):
                        if isinstance(input_socket.default_value, float):
                            input_value = str(input_socket.default_value)
                        elif input_socket.bl_idname == 'NodeSocketColor':
                            input_value = ', '.join(map(str, input_socket.default_value))
                        else:
                            input_value = ', '.join(map(str, input_socket.default_value))

                    node_data['inputs'].append((input_idx, input_name, input_type, input_value))

                for output_idx, output_socket in enumerate (node.outputs):
                    output_name = output_socket.name
                    output_type = output_socket.bl_idname
                    node_data['outputs'].append((output_idx, output_name, output_type))

                # Recursively export nodes inside the group
                node_data['nodes'] = export_node_tree_internal(node.node_tree, id_dict)
            else:
                # Regular node inputs and outputs
                for input_idx, input_socket in enumerate(node.inputs):
                    input_name = input_socket.name
                    input_type = input_socket.bl_idname

                    input_value = None  # Default value for input value

                    if hasattr(input_socket, 'default_value'):
                        if isinstance(input_socket.default_value, float):
                            input_value = str(input_socket.default_value)
                        elif input_socket.bl_idname == 'NodeSocketColor':
                            input_value = ', '.join(map(str, input_socket.default_value))
                        else:
                            input_value = ', '.join(map(str, input_socket.default_value))

                    node_data['inputs'].append((input_idx, input_name, input_type, input_value))

                for output_idx, output_socket in enumerate(node.outputs):
                    output_name = output_socket.name
                    output_type = output_socket.bl_idname
                    node_data['outputs'].append((output_idx, output_name, output_type))

            data['nodes'].append(node_data)
            node_dict[node.name] = node

        for link in node_tree.links:
            from_node = link.from_node
            from_socket = link.from_socket
            to_node = link.to_node
            to_socket = link.to_socket

            from_socket_idx = list(from_node.outputs).index(from_socket)
            to_socket_idx = list(to_node.inputs).index(to_socket)

            from_name = from_node.node_tree.name if from_node.type == 'GROUP' else from_node.name
            to_name = to_node.node_tree.name if to_node.type == 'GROUP' else to_node.name
            data['links'].append((from_name, from_socket_idx, to_name, to_socket_idx))

        return data

    id_dict = assign_unique_ids(node_tree)
    data = export_node_tree_internal(node_tree, id_dict)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, cls=NodeEncoder, ensure_ascii=False, indent=4)

    return {'FINISHED'}

def import_node_tree_internal(node_tree, data):
    node_dict = {}
    group_dict = {}
    groupCreated = False
    # Collect all existing nodes in the current node_tree
    existing_nodes = node_tree.nodes

    for node_data in data['nodes']:
        node_type = node_data['type']
        node_name = node_data['name']
        node_label = node_data['label']
        node_location = node_data['location']

        # Check if a node with the same name already exists in the current node_tree
        existing_node = existing_nodes.get(node_name)
        if existing_node:
            node = existing_node
        else:
            if node_type == 'ShaderNodeGroup':
                # Check if the group already exists
                if node_name in bpy.data.node_groups:
                    existing_group = bpy.data.node_groups[node_name]
                    group_dict[node_name] = existing_group
                else:
                    groupNodes = node_data['nodes']
                    group_inputs = node_data['inputs']
                    group_outputs = node_data['outputs']

                    newGroup = bpy.data.node_groups.new(name=node_name, type='ShaderNodeTree')
                    group_dict[node_name] = newGroup  # Store the group for linking

                    # Create group inputs
                    for input_idx, input_data in enumerate(group_inputs):
                        input_name = input_data[1]
                        input_socket_type = input_data[2]
                        try:
                            new_input = newGroup.inputs.new(input_socket_type, input_name)
                        except RuntimeError as e:
                            errorGen(f"Error creating input socket for {input_name} in group {node_name}: {e}", 'Error', 'ERROR')
                            return

                    # Create group outputs (if needed)
                    for output_idx, output_data in enumerate(group_outputs):
                        output_name = output_data[1]
                        output_socket_type = output_data[2]
                        try:
                            new_output = newGroup.outputs.new(output_socket_type, output_name)
                        except RuntimeError as e:
                            errorGen(f"Error creating output socket for {output_name} in group {node_name}: {e}", 'Error', 'ERROR')
                            return

                    # Recursively import nodes within the group
                    import_node_tree_internal(newGroup, groupNodes)

            # Now, create the node
            if node_type == 'ShaderNodeGroup':
                node = node_tree.nodes.new('ShaderNodeGroup')
                node.node_tree = group_dict[node_name]  # Use the stored group
            else:
                node = node_tree.nodes.new(node_type)

            node.location = node_location
            node.name = node_name
            node.label = node_label

            if node_type == 'ShaderNodeTexImage':
                color_space = node_data.get('color_space')
                if color_space:
                    node.image.colorspace_settings.name = color_space

        node_dict[node_name] = node

    # After processing all nodes, create the links
    create_links(node_tree, data['links'], node_dict, group_dict)
    
    return {'FINISHED'}

def create_links(node_tree, links_data, node_dict, group_dict):
    for link_data in links_data:
        from_node_name = link_data[0]
        from_socket_index = link_data[1]
        to_node_name = link_data[2]
        to_socket_index = link_data[3]

        from_node = node_dict.get(from_node_name) or group_dict.get(from_node_name)
        to_node = node_dict.get(to_node_name) or group_dict.get(to_node_name)

        if from_node is not None and to_node is not None:
            # Check if the nodes are ShaderNodeGroups
            if isinstance(from_node, bpy.types.NodeGroup):
                from_node = from_node.nodes[from_socket_index]
            if isinstance(to_node, bpy.types.NodeGroup):
                to_node = to_node.nodes[to_socket_index]

            from_socket = from_node.outputs[from_socket_index]
            to_socket = to_node.inputs[to_socket_index]

            # Create a link between nodes
            try:
                node_tree.links.new(from_socket, to_socket)
            except (IndexError, RuntimeError) as e:
                errorGen(f"Error creating link from {from_node_name} to {to_node_name}: {e}", 'Error', 'ERROR')
                return
    if bpy.context.active_object.active_material:
        bpy.ops.node.view_all()
def import_node_tree(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    selected_material = bpy.context.active_object.active_material
    node_tree = selected_material.node_tree
    import_node_tree_internal(node_tree, data)

    # Center the view on the selected nodes

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