import re
from datetime import datetime
from .constraint import RequiredConstraint, ConstraintException


'''
Taken from HTML spec: https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address
'''
EMAIL_REGEX = (
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)


class Node(object):
    def __init__(self, type_handler=None):
        self.name = 'root'
        self.children = []
        self.constraints = []
        self.type_handler = type_handler
        self.is_required = True
        self.defaults = {}
        self.default = None

    def has_children(self):
        return len(self.children) > 0

    async def transform(self, value):
        return value

    async def get_value(self, value):
        for constraint in self.constraints:
            if not constraint.validate(value):
                raise ConstraintException(constraint.message.replace('{field}', self.name))

        value = await self.transform(value)

        return value

    async def walk(self, value):
        if not isinstance(value, dict):
            return value

        if not self.has_children():
            return value

        result = {}

        for child in self.children:
            if child.name not in value and not child.is_required:
                if child.default is None:
                    continue

                value[child.name] = child.default

            child_value = value.get(child.name, None)
            result[child.name] = await child.get_value(await child.walk(child_value))

        return result

    def add(self, name, node_type, options=None):
        node = self.type_handler.create_node(node_type)

        if name in self.defaults:
            node.default = self.defaults[name]

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

        if 'constraints' in options:
            self.constraints.extend(options['constraints'])


class StringNode(Node):
    async def transform(self, value):
        if value is None:
            return None

        return str(value)


class IntegerNode(Node):
    async def transform(self, value):
        if value is None:
            return None

        return int(value)


class FloatNode(Node):
    async def transform(self, value):
        if value is None:
            return None

        return float(value)


class BooleanNode(Node):
    async def transform(self, value):
        if value is None:
            return None

        return bool(value)


class ObjectNode(Node):
    def __init__(self, object_class, type_handler=None):
        super(ObjectNode, self).__init__(type_handler)
        self.object_class = object_class

    async def get_value(self, input_value):
        for constraint in self.constraints:
            if not constraint.validate(input_value):
                raise ConstraintException(constraint.message.replace('{field}', self.name))

        if input_value is None:
            return None

        data = await super(ObjectNode, self).get_value(input_value)

        if not isinstance(data, dict):
            raise ConstraintException('Invalid field {}: {}'.format(self.name, data))

        if self.default is not None:
            instance = self.default

            for key in data:
                setattr(instance, key, data[key])

            return instance

        try:
            instance = self.object_class()
            for key in data:
                setattr(instance, key, data[key])
        except TypeError:
            instance = self.object_class(**data)

        return instance


class DatetimeNode(Node):
    def __init__(self, formatter=None):
        super(DatetimeNode, self).__init__()
        self.formatter = formatter

    async def transform(self, value):
        if value is None:
            return None

        try:
            return datetime.strptime(value, self.formatter)
        except ValueError as e:
            raise ConstraintException('Invalid {}: {}'.format(self.name, str(e)))


class EmailNode(StringNode):
    def __init__(self):
        super(EmailNode, self).__init__()

    async def transform(self, value):
        value = await super(EmailNode, self).transform(value)

        if value is None:
            return None

        normalized_value = value.strip().lower()

        if not re.match(EMAIL_REGEX, normalized_value):
            raise ConstraintException('Invalid {}: {} is not a valid email address'.format(self.name, value))

        return normalized_value


class ListNode(Node):
    def __init__(self, inner_node_type, type_handler=None):
        super(ListNode, self).__init__(type_handler)
        self.inner_node_type = inner_node_type
        self.inner_node = None

    def get_inner_node(self):
        if not self.inner_node:
            self.inner_node = self.type_handler.create_node(self.inner_node_type)
        return self.inner_node

    async def walk(self, values):
        if not self.isiterable(values):
            return None

        result = []

        for value in values:
            item_node = self.get_inner_node()
            item_value = await item_node.get_value(await item_node.walk(value))
            result.append(item_value)

        return result

    def add(self, name, node_type, options=None):
        return self.get_inner_node().add(name, node_type, options)

    def isiterable(self, value):
        try:
            iter(value)
        except TypeError:
            return False
        return True
