from enjalice.request import AliceRequest
from enjalice.response import AliceResponse
from enjalice.routers import Blueprint
from fuzzywuzzy import fuzz

bp = Blueprint()


@bp.message_handler(2, ["get_answer"])
async def get_answer_handler(req: AliceRequest) -> AliceResponse:
    ans = AliceResponse()
    if req.state.session.get("current_dialog") == "wait_answer":
        answer = req.request.nlu.intents.get("get_answer")["slots"]["place"]["value"]
        right_answer = req.state.session.get("right_answer")
        if fuzz.partial_ratio(answer, right_answer) >= 85:
            ans.response.text = "Вы угадали! Сыграть еще раз?"
        else:
            ans.response.text = "Вы не угадали... Сыграть еще раз?"

        ans.session_state["current_dialog"] = "wait_again"
    else:
        ans.response.text = "error TODO"

    return ans
