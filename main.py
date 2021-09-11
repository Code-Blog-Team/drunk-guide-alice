from aiohttp import web
from enjalice.routers import Dispatcher
from enjalice.response import AliceResponse, text
from enjalice.request import AliceRequest


async def handle(request: web.Request):
    data = await request.json()
    response = await request.app['dp'].dispatch_request(
        AliceRequest.parse_obj(data)
    )
    return web.json_response(response.dict())


app = web.Application()
app.router.add_post('/alice-webhook-path', handle)


START_TEXT = 'Добро пожаловать! ' \
             '"Пьяный гид" - это викторина-гид ' \
             'по достопримечательностям Санкт-Петербурга. ' \
             'Во время игры я буду кидать обработанную фильтром ' \
             'фотографию достопримечательности и говорить описание ' \
             'места, ваша задача - назвать место. Начнем игру?'


async def start_handler(_: AliceRequest) -> AliceResponse:
    resp = text(START_TEXT)
    return resp

dp = Dispatcher(start_handler)

if __name__ == '__main__':
    app['dp'] = dp
    web.run_app(app, host="0.0.0.0")
