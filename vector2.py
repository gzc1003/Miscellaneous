import array
import math


class Vector:

    typecode = 'd'

    def __init__(self,x,y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, self.x, self.y)

    def __bytes__(self):
        return (bytes([ord(self.typecode)])+
                bytes(array.array(self.typecode, self))
               )

    @classmethod
    def frombytes(cls, b):
        typecode = chr(b[0])
        memv = memoryview(b[1:]).cast(typecode)
        return cls(*memv)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    def __eq__(self, other):
        return tuple(self)==tuple(other)

    def __hash__(self):
        return hash(self.x)^hash(self.y)

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            cood = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            cood = self
            outer_fmt = '({}, {})'
        components = (format(v,fmt_spec) for v in cood)
        return outer_fmt.format(*components)


