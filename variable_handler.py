import asyncio
from aiohttp import web

@asyncio.coroutine
def variable_handler(request):
    print(request.match_info)
    return web.Response(text="Hello, {}".format(request.match_info['name']))

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/{name}', variable_handler)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
