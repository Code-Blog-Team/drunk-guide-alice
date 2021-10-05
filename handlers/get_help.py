from enjalice.request import AliceRequest
from enjalice.response import AliceResponse
from enjalice.routers import Blueprint

bp = Blueprint()

HELP_TEXT = 'Добро пожаловать! ' \
             '"Пьяный гид" - это викторина-гид ' \
             'по достопримечательностям Санкт-Петербурга. ' \
             'Во время игры я буду кидать обработанную фильтром ' \
             'фотографию достопримечательности и говорить описание ' \
             'места, ваша задача - назвать место. Начнем игру?'


@bp.message_handler(100, ["YANDEX.HELP"])
async def get_help_handler(_: AliceRequest) -> AliceResponse:
    ans = AliceResponse()
    ans.response.text = HELP_TEXT
    return ans
