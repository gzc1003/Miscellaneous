import functools, inspect, asyncio


def coroutine(func):
    @functools.wraps(func)
    def coro(*args, **kw):
        res = func(*args, **kw)
        if inspect.isgenerator(res):
            res = yield from res
        return res
    coro._is_coroutine = True
    return coro

@coroutine
def normal_function():
    print('Hello world!')

loop = asyncio.get_event_loop()
a = loop.create_task(normal_function())
loop.run_until_complete(normal_function())
# loop.close()
#
# print(normal_function)
# print(normal_function())
# def caller():
#     yield from normal_function()
#
#
# def main():
#     try:
#         next(caller())
#     except StopIteration:
#         pass
#
# print(normal_function())
# print(normal_function)
# main()

# import asyncio
#
# @asyncio.coroutine
# def hello_world():
#     print("Hello World!")
#
# def main():
#     yield from hello_world()
#
# print(hello_world)
# print(hello_world())
# next(main())



