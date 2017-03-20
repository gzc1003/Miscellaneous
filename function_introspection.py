def fun(integer: int, default:'int >0'=1, *args: tuple,
        keyword_only: str='a', **keyword: dict) -> 'jj':
    """just for test"""
    pass


def test(a, *b, c='cat', **d):
    print(b)

from functools import partial
new_test = partial(test, 1,2,3)
