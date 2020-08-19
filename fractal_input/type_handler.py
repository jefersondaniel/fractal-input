from .node import Node, ObjectNode, StringNode, IntegerNode, FloatNode, BooleanNode


class InvalidTypeException(Exception):
    pass


class TypeHandler(object):
    def __init__(self):
        self.type_map = {
            'string': StringNode,
            'integer': IntegerNode,
            'float': FloatNode,
            'boolean': BooleanNode,
            'dict': Node,
        }

    def create_node(self, node_type):
        if not isinstance(node_type, str) and not isinstance(node_type, Node):
            node_type = ObjectNode(node_type)

        if isinstance(node_type, Node):
            node_type.type_handler = self
            return node_type

        node_class = self.type_map.get(node_type)

        if not node_class:
            raise InvalidTypeException('Invalid node type: {}'.format(node_class))

        node = node_class()
        node.type_handler = self
        return node
