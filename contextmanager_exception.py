from contextlib import contextmanager

@contextmanager
def gen_contextmanager():
    print('enter')
    try:
        yield
    except ZeroDivisionError:
        print('exit')
    gen
    return 3

with gen_contextmanager():
    error = 1
    1/0