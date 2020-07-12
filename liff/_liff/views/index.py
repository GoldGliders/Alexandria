from flask import render_template
from flaskr import logger
from flaskr.liff import bp

@bp.route("/", methods=["GET"])
def index():
    logger.debug("liff index is accessed")
    return render_template("template.html", src="static/js/history.jsx")

@bp.route("/data", methods=["GET"])
def data():
    return render_template("sample.html")
