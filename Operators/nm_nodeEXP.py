import bpy
import json
from json import JSONEncoder
from bpy_extras.io_utils import ExportHelper, ImportHelper


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


def export_node_tree(node_tree, file_path):
    data = {'nodes': [], 'links': []}

    for node in node_tree.nodes:
        node_data = {
            'name': node.name,
            'type': type(node).__name__,
            'location': (node.location.x, node.location.y),
            'inputs': [(input.identifier, input.name, input.type)
                       for input in node.inputs],
            'outputs': [(output.identifier, output.name, output.type)
                        for output in node.outputs]
        }
        if isinstance(node, bpy.types.ShaderNodeTexImage) and node.image is not None:
            node_data['color_space'] = node.image.colorspace_settings.name
        data['nodes'].append(node_data)

    for link in node_tree.links:
        data['links'].append((link.from_node, link.from_socket,
                              link.to_node, link.to_socket))

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, cls=NodeEncoder, ensure_ascii=False, indent=4)

    return {'FINISHED'}

def import_node_tree(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    selected_material = bpy.context.active_object.active_material
    node_tree = selected_material.node_tree

    node_dict = {}
    for node_data in data['nodes']:
        node_type = node_data['type']
        node_location = node_data['location']
        node = node_tree.nodes.new(node_type)
        node.location = node_location

        if node_type == 'ShaderNodeTexImage':
            color_space = node_data.get('color_space')
            if color_space:
                node.image.colorspace_settings.name = color_space

        node_dict[node_data['name']] = node

    for link_data in data['links']:
        from_node = node_dict[link_data[0]]
        from_socket = from_node.outputs[link_data[1]]
        to_node = node_dict[link_data[2]]
        to_socket = to_node.inputs[link_data[3]]
        node_tree.links.new(from_socket, to_socket)

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