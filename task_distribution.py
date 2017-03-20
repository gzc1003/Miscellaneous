import asyncio
from time import strftime

def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)



@asyncio.coroutine
def sec2():
    yield from asyncio.sleep(3)
    display('coroutine 2 sec2')


@asyncio.coroutine
def loiter1():
    a = 0
    display('coroutine 1')
    yield from asyncio.sleep(2.5)
    while True:
        yield from asyncio.sleep(.1)
        display('fast_function 1')
        a += 1
        if a == 6:
            break


@asyncio.coroutine
def loiter2():
    a = 0
    display('coroutine 2')
    yield from sec2()
    yield from asyncio.sleep(1)
    while True:
        yield from asyncio.sleep(.1)
        display('fast_function 2')
        a += 1
        if a ==6:
            break

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([loiter1(), loiter2()]))
loop.close()
