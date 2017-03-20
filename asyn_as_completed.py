import asyncio


@asyncio.coroutine
def loiter1():
    yield from asyncio.sleep(1)
    print('loiter1')


@asyncio.coroutine
def loiter2():
    print('loiter2')
    return 2


@asyncio.coroutine
def sta():
    it = asyncio.as_completed([loiter1(),loiter2()])
    print(it)
    f = next(it)
    # yield from asyncio.sleep(1)
    print(f)
    re = yield from f
    print(re)

loop = asyncio.get_event_loop()
loop.run_until_complete(sta())
