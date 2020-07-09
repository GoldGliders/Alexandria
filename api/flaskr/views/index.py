from flaskr import logger, bp


@bp.route("/index", methods=["GET"])
def index_():
    return "api bp"

@bp.route("/", methods=["GET"])
def index():
    return "api bp"
