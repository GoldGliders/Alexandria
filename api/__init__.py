import os
import requests
import logging
from flask import Flask, render_template

config = {
        "development": "flaskr.config.DevelopmentConfig",
        "production": "flaskr.config.ProductionConfig",
        }

LOGFILE = "log"
formatter = "%(asctime)s  %(levelname)s  %(name)s  %(funcName)s  %(lineno)d : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from flaskr import api, bot, liff

    app.register_blueprint(api.bp, url_prefix="/api")
    app.register_blueprint(bot.bp, url_prefix="/bot")
    app.register_blueprint(liff.bp, url_prefix="/liff")

    """
    app.register_blueprint(api.bp)
    app.register_blueprint(bot_bp, subdomain="bot")
    app.register_blueprint(liff_bp, subdomain="liff")
    """

    return app


def get_profile(access_token):
    headers = {
        f'Authorization': 'Bearer {access_token}',
    }

    response = requests.get('https://api.line.me/v2/profile', headers=headers)
    if response.status_code != 200:
        raise ValueError

    return response.json()
