import time
from concurrent import futures


def wait_on_b():
    print('b')
    # time.sleep(1)
    # print(c)
    # raise Exception
    print('bb')
    # print(b.result())   # b will never complete because it is waiting on a.
    print('b continue')
    print('aasdsdf')
    print(123)
    return 5


def wait_on_a():
    # print(n)
    # time.sleep(float(n))
    # print('aa')
    # Exception
    # time.sleep(2)
    #print(a.result()) # a will never complete because it is waiting on b.
    print('aa')
    print('kk')
    print('ff')
    return n


executor = futures.ThreadPoolExecutor(max_workers=2)
# re = executor.map(wait_on_a, '12')
# print('intervene')
# print(next(re))
a = executor.submit(wait_on_b)
print(a)
b = executor.submit(wait_on_a)
print(b)
# print(b.result())
# print(a.result())
# print(a)
# print('main')
# d = executor.shutdown()
# print(d)
# it = futures.as_completed(a)# print(it)
# f = next(it)
# print(f)
# f = next(it)
# print(f)