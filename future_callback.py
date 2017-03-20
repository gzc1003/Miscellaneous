from concurrent import futures
import time


def loiter():
    print('loiter: begin')
    time.sleep(10)
    print('loiter: done')
    return 'finished'


def callback(fs):
    print('future: done')

with futures.ThreadPoolExecutor(max_workers=5) as executor:
    future = executor.submit(loiter)
    print(future)
    future.add_done_callback(callback)
    print('waiting')
    res = future.result()
    print(res)