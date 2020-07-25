import os
from hashlib import sha256
import logging
import requests
from flask import Blueprint, Flask
from dotenv import load_dotenv
from flaskr.models import db
from flask_cors import CORS

load_dotenv()
bp = Blueprint("api", __name__, static_folder="static", template_folder="template")

formatter = "%(asctime)s  %(levelname)s  %(name)s  %(funcName)s  %(lineno)d : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)


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


def get_resource(resource_name, id_token=None):
    id_token = id_token or os.getenv("DEFAULT_HASHED_USERId")
    try:
        response = get_profile(id_token)
        userid = response["sub"]

        hashed_useid = sha256(userid.encode()).hexdigest()
        logger.debug(hashed_useid)
        document = db.user.find(hashed_useid)
        logger.debug(document)
        items = document if resource_name == "ALL" else {"items": document[resource_name]}
        logger.debug(items)

        return (items, 200)

    except ValueError as e:
        logger.info(f"id_token error: {e}")

        return ({"error": str(e)}, 400)


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from flaskr.views import (
        index, get_history, get_area_oriented_library,
        put_library, delete_resource
    )
    app.register_blueprint(index.bp)
    app.register_blueprint(get_history.bp)
    app.register_blueprint(get_area_oriented_library.bp)
    app.register_blueprint(put_library.bp)
    app.register_blueprint(delete_resource.bp)

    app.config["JSON_AS_ASCII"] = False

    logger.info("create api")
    CORS(app)

    return app
