import pytest
from fractal_input import InputHandler, ListNode, DatetimeNode


class TestInputHandler(object):
    def test_get_data_as_dict(self):
        class DataHandler(InputHandler):
            def define(self):
                self.add('name', 'string', {'required': True})
                self.add('email', 'string', {'required': True})
                self.add('age', 'integer')

        handler = DataHandler()
        handler.bind({
            'name': 'Jamal',
            'email': 'jamal@here.com',
            'age': 13
        })

        assert handler.is_valid()
        assert 'Jamal' == handler.get_data()['name']

    def test_get_data_as_object(self):
        class User:
            name = None
            email = None
            age = None
            address = None
            telephones = None
            is_active = None
            created = None

        class Address:
            street = None

        class Telephone:
            number = None

        class UserHandler(InputHandler):
            def define(self):
                user = self.add('user', User)
                user.add('name', 'string', {'required': True})
                user.add('email', 'string', {'required': True})
                user.add('age', 'integer')
                user.add('is_active', 'boolean')
                user.add('created', DatetimeNode('%Y-%m-%d'))
                user.add('values', ListNode('integer'))
                telephone = user.add('telephones', ListNode(Telephone))
                telephone.add('number', 'string')
                address = user.add('address', Address)
                address.add('street', 'string')
                owner = address.add('owner', User)
                owner.add('name', 'string')

        handler = UserHandler()

        handler.bind({
            'user': {
                'name': 'Jamal',
                'email': 'jamal@here.com',
                'age': 13,
                'values': [1, 2, 3],
                'is_active': False,
                'created': '2020-01-01',
                'address': {
                    'street': 'Lala',
                    'owner': {
                        'name': 'Emily'
                    }
                },
                'telephones': [
                    {'number': '123'}
                ]
            }
        })

        assert handler.is_valid()
        assert 'Jamal' == handler.get_data()['user'].name
        assert 2020 == handler.get_data()['user'].created.year
        assert not handler.get_data()['user'].is_active
        assert [1, 2, 3] == handler.get_data()['user'].values
        assert '123' == handler.get_data()['user'].telephones[0].number
        assert 'Lala' == handler.get_data()['user'].address.street
        assert 'Emily' == handler.get_data()['user'].address.owner.name

    def test_validation(self):
        class User:
            pass

        class DataHandler(InputHandler):
            def define(self):
                self.add('string_value', 'string')
                self.add('integer_value', 'integer')
                self.add('float_value', 'float')
                self.add('boolean_value', 'boolean', {'required': False})
                self.add('none_string_value', 'string', {'required': False})
                self.add('none_integer_value', 'integer', {'required': False})
                self.add('none_float_value', 'float', {'required': False})
                self.add('none_boolean_value', 'boolean', {'required': False})
                self.add('dict_value', 'dict', {'required': False})
                self.add('none_object_value', User, {'required': False})
                self.add('none_datetime_value', DatetimeNode('%Y-%m-%d'), {'required': False})
                self.add('none_list_value', ListNode('string'), {'required': False})

        handler = DataHandler()

        handler.bind({})
        assert not handler.is_valid()
        assert 'string_value is required' == handler.get_error_as_string()

        handler.bind({'string_value': '1'})
        assert 'integer_value is required' == handler.get_error_as_string()

        handler.bind({
            'string_value': '1',
            'integer_value': '1',
            'float_value': '1',
            'dict_value': {'a': 1},
            'none_string_value': None,
            'none_integer_value': None,
            'none_float_value': None,
            'none_boolean_value': None,
            'none_object_value': None,
            'none_datetime_value': None,
            'none_list_value': None,
        })

        assert handler.is_valid()
        assert not handler.get_error_as_string()

        assert {
            'string_value': '1',
            'integer_value': 1,
            'float_value': 1,
            'dict_value': {'a': 1},
            'none_string_value': None,
            'none_integer_value': None,
            'none_float_value': None,
            'none_boolean_value': None,
            'none_object_value': None,
            'none_datetime_value': None,
            'none_list_value': None,
        } == handler.get_data()

        handler.bind({
            'string_value': '1',
            'integer_value': '1',
            'float_value': '1',
            'none_object_value': 1,
        })

        assert not handler.is_valid()

        handler.bind({
            'string_value': '1',
            'integer_value': '1',
            'float_value': '1',
            'none_datetime_value': 'lala',
        })

        assert not handler.is_valid()

    def test_invalid_type(self):
        class DataHandler(InputHandler):
            def define(self):
                self.add('string_value', 'lala', {'required': True})

        handler = DataHandler()

        with pytest.raises(Exception):
            handler.bind({})
