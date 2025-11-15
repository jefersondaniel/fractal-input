import pytest
from fractal_input import InputHandler


class TestEmailNode(object):
    @pytest.mark.asyncio
    async def test_valid_email_is_normalized(self):
        class EmailHandler(InputHandler):
            def define(self):
                self.add('email', 'email', {'required': True})

        handler = EmailHandler()
        await handler.bind({'email': '  USER@Example.COM  '})

        assert handler.is_valid()
        assert handler.get_data()['email'] == 'user@example.com'

    @pytest.mark.asyncio
    async def test_invalid_email_formats(self):
        class EmailHandler(InputHandler):
            def define(self):
                self.add('email', 'email', {'required': True})

        invalids = [
            'abc',
            'user@',
            '@example.com',
            'user@@example.com',
            'user example@example.com',
            'user@-example.com',
            'user@example..com',
        ]

        for invalid in invalids:
            handler = EmailHandler()
            await handler.bind({'email': invalid})
            assert not handler.is_valid()
            err = handler.get_error_as_string()
            assert 'Invalid email:' in err
            assert invalid in err

    @pytest.mark.asyncio
    async def test_integer_input_is_invalid(self):
        class EmailHandler(InputHandler):
            def define(self):
                self.add('email', 'email', {'required': True})

        handler = EmailHandler()
        await handler.bind({'email': 123})

        assert not handler.is_valid()
        err = handler.get_error_as_string()
        assert 'Invalid email:' in err
        assert '123' in err

    @pytest.mark.asyncio
    async def test_optional_email_missing_is_ok(self):
        class EmailHandler(InputHandler):
            def define(self):
                self.add('email', 'email', {'required': False})

        handler = EmailHandler()
        await handler.bind({})

        assert handler.is_valid()
        assert 'email' not in handler.get_data()

    @pytest.mark.asyncio
    async def test_optional_email_default_is_normalized(self):
        class EmailHandler(InputHandler):
            def define(self):
                self.add('email', 'email', {'required': False})

        handler = EmailHandler()
        await handler.bind({}, defaults={'email': '  ADMIN@EXAMPLE.com '})

        assert handler.is_valid()
        assert handler.get_data()['email'] == 'admin@example.com'
