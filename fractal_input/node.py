from datetime import datetime
from .constraint import RequiredConstraint, ConstraintException


class Node(object):
    def __init__(self, type_handler=None):
        self.name = 'root'
        self.children = []
        self.constraints = []
        self.type_handler = type_handler
        self.is_required = True

    def has_children(self):
        return len(self.children) > 0

    def transform(self, value):
        return value

    def get_value(self, value):
        for constraint in self.constraints:
            if not constraint.validate(value):
                raise ConstraintException(constraint.message.replace('{field}', self.name))

        value = self.transform(value)

        return value

    def walk(self, value):
        if not isinstance(value, dict):
            return value

        if not self.has_children():
            return value

        result = {}

        for child in self.children:
            if child.name not in value and not child.is_required:
                continue
            child_value = value.get(child.name, None)
            result[child.name] = child.get_value(child.walk(child_value))

        return result

    def add(self, name, node_type, options=None):
        node = self.type_handler.create_node(node_type)
        node.configure(name, options)
        self.children.append(node)
        return node

    def configure(self, name, options=None):
        self.name = name

        if not options:
            options = {}

        self.is_required = options.get('required', True)

        if self.is_required:
            self.constraints.append(RequiredConstraint())


class StringNode(Node):
    def transform(self, value):
        if value is None:
            return None

        return str(value)


class IntegerNode(Node):
    def transform(self, value):
        if value is None:
            return None

        return int(value)


class FloatNode(Node):
    def transform(self, value):
        if value is None:
            return None

        return float(value)


class BooleanNode(Node):
    def transform(self, value):
        if value is None:
            return None

        return bool(value)


class ObjectNode(Node):
    def __init__(self, object_class, type_handler=None):
        super(ObjectNode, self).__init__(type_handler)
        self.object_class = object_class

    def get_value(self, input_value):
        data = super(ObjectNode, self).get_value(input_value)
        instance = self.object_class()

        if input_value is None:
            return None

        if not isinstance(data, dict):
            raise ConstraintException('Invalid field {}: {}'.format(self.name, data))

        for key in data:
            setattr(instance, key, data[key])

        return instance


class DatetimeNode(Node):
    def __init__(self, formatter=None):
        super(DatetimeNode, self).__init__()
        self.formatter = formatter

    def transform(self, value):
        if value is None:
            return None

        try:
            return datetime.strptime(value, self.formatter)
        except ValueError as e:
            raise ConstraintException('Invalid {}: {}'.format(self.name, str(e)))


class ListNode(Node):
    def __init__(self, inner_node_type, type_handler=None):
        super(ListNode, self).__init__(type_handler)
        self.inner_node_type = inner_node_type
        self.inner_node = None

    def get_inner_node(self):
        if not self.inner_node:
            self.inner_node = self.type_handler.create_node(self.inner_node_type)
        return self.inner_node

    def walk(self, values):
        if not self.isiterable(values):
            return None

        result = []

        for value in values:
            item_node = self.get_inner_node()
            item_value = item_node.get_value(item_node.walk(value))
            result.append(item_value)

        return result

    def add(self, name, node_type, options=None):
        self.get_inner_node().add(name, node_type, options)

    def isiterable(self, value):
        try:
            iter(value)
        except TypeError:
            return False
        return True
