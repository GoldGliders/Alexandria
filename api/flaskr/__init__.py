import os
import requests
from logging import getLogger, FileHandler, Formatter, INFO, DEBUG
from flask import Blueprint, Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
bp = Blueprint("api", __name__, static_folder="static", template_folder="template")


LOGFILE = "/var/log/flask/access.log"
handler = FileHandler(filename=LOGFILE, encoding="utf-8")
handler.setFormatter(Formatter("%(asctime)s  %(levelname)s  %(name)s  %(funcName)s  %(lineno)d : %(message)s"))
handler.setLevel(INFO)

logger = getLogger(__name__)
logger.addHandler(handler)

def get_profile(id_token):
    data = {
        "id_token": id_token,
        "client_id": os.getenv("LOGIN_CHANNEL_ID")
    }

    response = requests.post("https://api.line.me/oauth2/v2.1/verify", data=data)

    if response.status_code != 200:
        error_response = response.json()["error_description"]
        logger.info(error_response)
        raise ValueError(error_response)

    return response.json()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from flaskr.views import (
        index, get_history, get_area_oriented_library
    )
    app.register_blueprint(index.bp)
    app.register_blueprint(get_history.bp)
    app.register_blueprint(get_area_oriented_library.bp)

    app.config["JSON_AS_ASCII"] = False

    logger.info("create api")

    return app
