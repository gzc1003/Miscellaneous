import types
from importlib import reload


def transitive_reload(modules, visited):
    modules = list(modules)
    while modules:
        module = modules.pop()
        reload(module)
        print('reload %s' % module)
        visited.add(module)
        modules.extend(m for m in module.__dict__.values() if type(m) == types.ModuleType and m not in visited)


def reloadall(*args):
    transitive_reload(args, set())