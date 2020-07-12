import os
from flask import Blueprint, Flask, render_template
from flaskr import logger

bp = Blueprint("liff", __name__, static_folder="static", template_folder="template")

from flaskr.liff.views import index
logger.info("create liff bp")
