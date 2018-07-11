class Operator(object):
    op = 'exact'

    # Can be overridden via constructor.
    allow_negation = False

    def __init__(self, allow_negation=False):
        self.allow_negation = allow_negation

    # Lets us specify filters as an instance if we want to override the
    # default arguments (in addition to specifying them as a class).
    def __call__(self):
        return self

    def prepare_queryset_kwargs(self, field, value, negate):
        if negate:
            return {field: {'$not': {'${0}'.format(self.op): value}}}
        else:
            return {field: {'${0}'.format(self.op): value}}

    def apply(self, field, value, negate=False):
        kwargs = self.prepare_queryset_kwargs(field, value, negate)
        return kwargs


class Ne(Operator):
    op = 'ne'


class Lt(Operator):
    op = 'lt'


class Lte(Operator):
    op = 'lte'


class Gt(Operator):
    op = 'gt'


class Gte(Operator):
    op = 'gte'


class Exact(Operator):
    op = 'exact'

    def prepare_queryset_kwargs(self, field, value, negate):
        # Using <field>__exact causes mongoengine to generate a regular
        # expresison query, which we'd like to avoid.
        if negate:
            return {field: {'$ne': value}}
        else:
            return {field: value}

class In(Operator):
    op = 'in'

    def prepare_queryset_kwargs(self, field, value, negate):
        # only use 'in' or 'nin' if multiple values are specified
        if ',' in value:
            value = value.split(',')
            op = negate and 'nin' or self.op
        else:
            op = negate and 'ne' or ''
        return {field: {op: value}}

class Boolean(Operator):
    op = 'exact'

    def prepare_queryset_kwargs(self, field, value, negate):
        if value == 'false':
            bool_value = False
        else:
            bool_value = True

        if negate:
            bool_value = not bool_value

        return {field: bool_value}

		
class Startswith(Operator):
    op = 'startswith'

    def prepare_queryset_kwargs(self, field, value, negate):
        return {field: {'$regex' : '^{}'.format(value)}}

    def apply(self, field, value, negate=False):
        kwargs = self.prepare_queryset_kwargs(field, value, negate)
        return kwargs
