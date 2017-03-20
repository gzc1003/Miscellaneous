import asyncio

@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        #yield from asyncio.sleep(5)
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()


# 使用asyncio：
#
# Coroutine1
# Print()
# Yield from coroutineA
# Print()
#
# Coroutine2
# Print()
# Yield from coroutineB
# Print()
#
# Coroutine3
# Print()
# Yield from coroutineC
# Print()
#
# 同一个线程中，先执行coroutine1 中的可执行语句，直至遇到yield from coroutineA，中断coroutine1；
# 转而执行coroutine2 中的可执行语句，直至遇到yield from coroutineB，中断coroutine2；
# 转而执行Coroutine3 中的可执行语句，直至遇到yield from coroutineC，中断coroutine3；
#
# coroutineA B C谁先结束，即coroutine1 2 3谁的中断先结束，谁先继续向下执行
