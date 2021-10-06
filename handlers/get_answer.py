from enjalice.request import AliceRequest
from enjalice.response import AliceResponse
from enjalice.routers import Blueprint
from fuzzywuzzy import fuzz

bp = Blueprint()


@bp.message_handler(2, ["get_answer"])
async def get_answer(req: AliceRequest) -> AliceResponse:
    ans = AliceResponse()
    answer = req.request.nlu.intents.get("get_answer")["slots"]["place"]["value"]
    right_answer = req.state.session.get("right_answer")
    if fuzz.partial_ratio(answer, right_answer) >= 85:
        ans.response.text = "Вы угадали! Сыграть еще раз?"
    else:
        ans.response.text = "Вы не угадали... Сыграть еще раз?"

    ans.session_state["current_dialog"] = "wait_again"
    return ans
