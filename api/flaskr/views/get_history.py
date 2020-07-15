import os
from flask import request, jsonify
from flaskr import bp, get_profile, get_resource, logger
from flaskr.models import db
from hashlib import sha256


@bp.route("/history", methods=["GET"])
def get_history():
    idToken = request.args.get("idToken")
    resource, status_code = get_resource("history", idToken)
    return jsonify(resource), status_code


@bp.route("/bookmark", methods=["GET"])
def get_bookmark():
    idToken = request.args.get("idToken")
    resource, status_code = get_resource("bookmarks", idToken)
    return jsonify(resource), status_code


@bp.route("/library", methods=["GET"])
def get_library():
    idToken = request.args.get("idToken")
    resource, status_code = get_resource("favolib", idToken)
    return jsonify(resource), status_code
