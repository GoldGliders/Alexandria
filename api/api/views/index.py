from flaskr import logger
from flaskr.api import bp


@bp.route("/index", methods=["GET"])
def index():
    return "api bp"
