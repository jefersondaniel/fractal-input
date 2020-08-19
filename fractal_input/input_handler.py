from .type_handler import TypeHandler
from .node import Node, ConstraintException


class InputHandler(object):
    def __init__(self, type_handler=None):
        if not type_handler:
            type_handler = TypeHandler()
        self.root_node = Node(type_handler)
        self.input_data = None
        self.output = None
        self.errors = []

    def bind(self, input_data):
        self.define()

        self.input_data = input_data
        self.errors = []
        self.output = None

        try:
            self.output = self.root_node.get_value(self.root_node.walk(self.input_data))
        except ConstraintException as e:
            self.errors.append(e.message)

    def add(self, name, node_type, options=None):
        return self.root_node.add(name, node_type, options)

    def get_data(self):
        return self.output

    def is_valid(self):
        return len(self.errors) == 0

    def get_error_as_string(self):
        if not self.errors:
            return None

        return ','.join(self.errors)
