import os
import requests
import logging
from dotenv import load_dotenv
from flask import Blueprint, Flask, render_template, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError


load_dotenv()

LOGFILE = "log"
formatter = "%(asctime)s  %(levelname)s  %(name)s  %(funcName)s  %(lineno)d : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)


line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])
bp = Blueprint("bot", __name__, static_folder="static", template_folder="template")

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(bp)
    logger.info("Bot app is initialized")

    from flaskr.brain import richmenu
    from flaskr.brain.events import (
        FollowEvent, ImageMessage, PostbackEvent,
        TextMessage, UnfollowEvent
    )
    richmenu.create_richmenu()

    return app


def get_profile(access_token):
    headers = {
        f'Authorization': 'Bearer {access_token}',
    }

    response = requests.get('https://api.line.me/v2/profile', headers=headers)
    if response.status_code != 200:
        raise ValueError

    return response.json()


@bp.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    logger.debug("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)

    except InvalidSignatureError as e:
        logger.info(f"InvalidSignatureError: {e}")
        abort(400)

    return "Signature is confirmed"


@bp.route("/", methods=['GET'])
def index():
    return "Hello!"
