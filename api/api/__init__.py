import os
import requests
from flask import Blueprint, Flask, render_template, request
from flaskr import logger

bp = Blueprint("api", __name__, static_folder="static", template_folder="template")

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

from flaskr.api.views import index, get_history
logger.info("create api")
