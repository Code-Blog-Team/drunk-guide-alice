from enjalice.request import AliceRequest
from enjalice.response import AliceResponse
from enjalice.routers import Blueprint

bp = Blueprint()


@bp.message_handler(6, ["get_fact"])
async def get_fact_handler(req: AliceRequest) -> AliceResponse:
    current_dialog = req.state.session.get("current_dialog", None)
    ans = AliceResponse()

    if current_dialog == "wait_answer":
        # TODO: получаем из БД случайный факт о данном месте
        fact = "TODO!"
        ans.session_state["current_dialog"] = "wait_answer"
        ans.session_state["right_answer"] = req.state.session.get("right_answer")
        ans.response.text = fact

    else:
        ans.response.text = "ошибка!"

    return ans
