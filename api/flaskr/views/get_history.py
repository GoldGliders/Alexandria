import os
from flask import request, jsonify
from flaskr import bp, get_profile, logger
from flaskr.models import db
from hashlib import sha256
from pymongo.errors import ServerSelectionTimeoutError


@bp.route("/history", methods=["GET"])
def get_history():
    id_token = request.args.get("id_token") or os.getenv("DEFAULT_HASHED_USERId")
    try:
        response = get_profile(id_token)
        userid = response["sub"]

        hashed_useid = sha256(userid.encode()).hexdigest()
        logger.debug(hashed_useid)
        document = db.user.find(hashed_useid)
        logger.debug(document)
        history = document["history"]
        items = {"items": history}
        logger.debug(items)

        return jsonify(items), 200

    except ValueError as e:
        logger.info(f"id_token error: {e}")

        return jsonify({"error": str(e)}), 400

    except ServerSelectionTimeoutError as e:
        logger.info(f"server error: {e}")

        return jsonify({"error": str(e)}), 500



@bp.route("/history", methods=["POST"])
def remove_history():
    return "api bp"
