Fractal Input
======================================

|Build Status| |Version| |Pyversions|

Abstracts HTTP request input handling, providing an easy interface for data hydration and validation Based on https://github.com/LinioIT/input

Documentation
~~~~~~~~~~~~~

Usage
^^^^^

Install:
''''''''

.. code:: bash

   $ pip install fractal_input

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: python

    from fractal_input import InputHandler, DatetimeNode, Telephone

    class UserHandler(InputHandler):
        def define(self):
            user = self.add('user', User)
            user.add('name', 'string')
            user.add('email', 'string')
            user.add('age', 'integer', {'required': False})
            user.add('createdAt', DatetimeNode('%m/%d/%y %H:%M:%S'))

            address = user.add('address', Address)
            address.add('street', 'string')

            telephone = user.add('telephones', ListNode(Telephone))
            telephone.add('number', 'string')

  dict_data = {
    'user': {
      'name': 'James',
      'email': 'james@email.com',
      'age': 20
    }
  }

  input = UserHandler()
  input.bind(dict_data)

  if not input.is_valid():
    print(input.get_error_as_string())

  user = input.get_data()['user']

''''

.. |Build Status| image:: https://travis-ci.org/jefersondaniel/fractal-input.svg
   :target: https://travis-ci.org/jefersondaniel/fractal-input

.. |Version| image:: https://badge.fury.io/py/fractal_input.svg
   :target: https://pypi.python.org/pypi/fractal_input

.. |Pyversions| image:: https://img.shields.io/pypi/pyversions/fractal_input.svg
   :target: https://pypi.python.org/pypi/fractal_input
