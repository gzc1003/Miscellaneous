import asyncio
from threading import current_thread
import time



def slow_io():
    time.sleep(4)
    print('slow io in %s' % current_thread())


@asyncio.coroutine
def main_io():
    print('main io in %s' % current_thread().name)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, slow_io)
    # slow_io()
    print('main continues')

loop = asyncio.get_event_loop()
loop.run_until_complete(main_io())


