class Quantity:

    __counter = 0

    def __init__(self):
        cls = type(self)
        cls_name = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(cls_name, index)
        cls.__counter += 1

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('Value must be >0')

    def __get__(self, instance, owner):
        return getattr(instance, self.storage_name)


def class_decorator(cls):
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Quantity):
            attr.storage_name = '_{}#{}'.format(type(attr).__name__, key)
    return cls


class Meta(type):
    print('MetaClass is running')
    def __init__(cls, name, bases, attr_dict):
        print('Initialize class')
        for key, attr in attr_dict.items():
            if isinstance(attr, Quantity):
                attr.storage_name = '_{}#{}'.format(type(attr).__name__, key)


class entity(metaclass=Meta):
    pass


# @class_decorator
class Lineitem(entity):
    weight = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price




