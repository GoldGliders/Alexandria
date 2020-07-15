import json
import os
import time
from hashlib import sha256
from flask import request, jsonify
from flaskr import bp, get_profile, get_resource, logger
from flaskr.models import db


def delete_resource(target_name, id_name):
    body = request.get_json()
    id_token = body.get("idToken")
    target_id = body.get("targetId")
    logger.info(body)
    document, status_code = get_resource(resource_name="ALL", id_token=id_token)

    if status_code == 200:
        registered_resource = document[target_name]
        logger.debug(registered_resource)
        if target_name == "bookmark":
            registered_target_id = list(map(lambda t: t["bookmeta"][id_name], registered_resource))
        elif target_name == "favolib":
            registered_target_id = list(map(lambda t: t[id_name], registered_resource))

        if target_id not in registered_target_id:
            # 404: not found
            return jsonify({"status": 404, "message": "The resource is not registered."}), 404
        else:
            index_num = registered_target_id.index(target_id)
            logger.debug(index_num)
            registered_resource.pop(index_num)
            logger.debug(registered_resource)

            response = get_profile(id_token)
            userid = response["sub"]
            hashed_useid = sha256(userid.encode()).hexdigest()

            document[target_name] = registered_resource
            logger.debug(document)
            db.user.set(hashed_useid, document)

            return jsonify({"status": 204, "message": "the resource is deleted"}), 200

    else:
        return jsonify({"status": 500, "message": "api server error"}), 500


@bp.route("/library", methods=["DELETE"])
def delete_library():
    resource, status_code = delete_resource("favolib", "libid")

    return resource, status_code


@bp.route("/bookmark", methods=["DELETE"])
def delete_bookmark():
    resource, status_code = delete_resource("bookmark", "isbn")

    return resource, status_code
