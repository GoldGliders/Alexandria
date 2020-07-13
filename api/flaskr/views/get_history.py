import os
from flask import request, jsonify
from flaskr import bp, get_profile, logger
from flaskr.models import db
from hashlib import sha256

def get_resource(resource_name):
    id_token = request.args.get("idToken") or os.getenv("DEFAULT_HASHED_USERId")
    try:
        response = get_profile(id_token)
        userid = response["sub"]

        hashed_useid = sha256(userid.encode()).hexdigest()
        logger.debug(hashed_useid)
        document = db.user.find(hashed_useid)
        logger.debug(document)
        history = document[resource_name]
        items = {"items": history}
        logger.debug(items)

        return jsonify(items), 200

    except ValueError as e:
        logger.info(f"id_token error: {e}")

        return jsonify({"error": str(e)}), 400


@bp.route("/history", methods=["GET"])
def get_history():
    resource = get_resource("history")
    return resource


@bp.route("/bookmark", methods=["GET"])
def get_bookmark():
    resource = get_resource("bookmarks")
    return resource


@bp.route("/library", methods=["GET"])
def get_library():
    resource = get_resource("favolib")
    return resource


@bp.route("/history", methods=["POST"])
def remove_history():
    return "api bp"
