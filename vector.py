import reprlib
import itertools
import math
import numbers
from functools import reduce
from array import array


class Vector:

    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return type(self)(self._components[item])
        elif isinstance(item, numbers.Integral):
            return self._components[item]
        else:
            raise TypeError('Vector indices must be integers')

    def __len__(self):
        return len(self._components)

    shortcuts = 'xyzt'

    def __getattr__(self, item):
        cls = type(self)
        if len(item) ==1:
            offset = cls.shortcuts.find(item)
            if 0 <= offset < len(self):
                return self[offset]
        raise AttributeError("'Vector' object has no attribute {!r}".format(item))

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format( components)

    def __str__(self):
        return str(tuple(self))

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            cood = itertools.chain([abs(self)], self.angles())
            outer_format = '<{}>'
        else:
            cood = self
            outer_format = '({})'
        components = (format(x, fmt_spec) for x in cood)
        return outer_format.format(', '.join(components))

    def __hash__(self):
        return reduce(lambda a,b: a^b, (hash(x) for x in self), 0)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return len(self) == len(other) and all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented

    def __neg__(self):
        return Vector(-x for x in self)

    def __pos__(self):
        return self

    def __abs__(self):
        return math.sqrt(sum(x**2 for x in self))

    def __add__(self, other):
        try:
            return Vector(a+b for a,b in itertools.zip_longest(self, other, fillvalue=0))
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        return self+other

    def __mul__(self, other):
        if isinstance(other, numbers.Real):
            return Vector(x * other for x in self)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __bool__(self):
        return abs(self)

    def __bytes__(self):
        return bytes([ord(self.typecode)])+bytes(self._components)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        components = memoryview(octets[1:]).cast(typecode)
        return Vector(components)








