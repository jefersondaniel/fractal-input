
class ConstraintException(Exception):
    def __init__(self, message):
        super(ConstraintException, self).__init__()

        self.message = message


class Constraint(object):
    pass


class RequiredConstraint(Constraint):
    def __init__(self):
        super(Constraint, self).__init__()
        self.message = r'{field} is required'

    def validate(self, value):
        return value is not None
