from enjalice.attachments.cards import BigImage
from enjalice.request import AliceRequest
from enjalice.response import AliceResponse
from enjalice.routers import Blueprint

bp = Blueprint()


@bp.message_handler(10, ["lets_start"])
async def start_game_handler(req: AliceRequest) -> AliceResponse:
    current_dialog = req.state.session.get("current_dialog", None)
    ans = AliceResponse()
    if not current_dialog or current_dialog == "start_game":
        # TODO: получаем из БД случайное место, получаем картинку и описание этого места
        text = "TODO NOW!"
        right_answer = "TODO NOW!"
        ans.response.text = text
        ans.response.card = BigImage(
            image_id="IMAGE_ID_HERE",
            description=text
        )
        ans.session_state["current_dialog"] = "wait_answer"
        ans.session_state["right_answer"] = right_answer

    else:
        ans.response.text = "Ошибка!"

    return ans
