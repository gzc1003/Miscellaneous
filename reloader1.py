import types
from importlib import reload


def transitive_reload(objects, visited):
    for object in objects:
        if type(object) == types.ModuleType and object not in visited:
            reload(object)
            print('reload %s' % object)
            visited.add(object)
            transitive_reload(object.__dict__.values(), visited)


def reloadall(*args):
    transitive_reload(args, set())

