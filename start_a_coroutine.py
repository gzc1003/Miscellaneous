import asyncio



@asyncio.coroutine
def coro():
    yield from asyncio.sleep(2)
    print('=_=')


@asyncio.coroutine
def coro2():
    print('coro2')
    yield from asyncio.sleep(1)
    print('- -')

loop = asyncio.get_event_loop()
# asyncio.async(coro())
asyncio.async(coro2())
loop.run_until_complete(coro())
# loop.run_forever()