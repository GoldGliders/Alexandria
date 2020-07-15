import json
import os
import time
from hashlib import sha256
from flask import request, jsonify
from flaskr import bp, get_profile, get_resource, logger
from flaskr.models import db

def create_resource(resource, id_token=None):
    id_token = id_token or os.getenv("DEFAULT_HASHED_USERId")
    try:
        response = get_profile(id_token)
        userid = response["sub"]

        hashed_useid = sha256(userid.encode()).hexdigest()
        logger.debug(hashed_useid)
        db.user.set(hashed_useid, resource)

        return {"status": "success"}, 200

    except Exception as e:
        logger.info(f"undefined error: {e}")

        return {"error": str(e)}, 500


@bp.route("/library", methods=["PUT"])
def put_library():
    """
    Create favorite library on record. It must be unique on one user record.
    """
    body = request.get_json()
    id_token = body.get("idToken")
    libid = body.get("libid")
    logger.debug(body)
    document, status_code = get_resource(resource_name="ALL", id_token=id_token)

    if status_code == 200:
        registered_favolib = document["favolib"]
        registered_libid = list(map(lambda favolib: favolib["libid"], registered_favolib))

        if libid in registered_libid:
            # 406: not acceptable
            return jsonify({"error": "This library is already registered."}, 406)
        else:
            libinfo = db.library.find(libid)

            lib_doc = dict()
            lib_doc["timestamp"] = int(time.time())
            lib_doc["formal"] = libinfo["formal"]
            lib_doc["libid"] = libinfo["libid"]
            lib_doc["systemid"] = libinfo["systemid"]

            logger.debug(f"additional favorite library: {lib_doc}")
            document["favolib"].append(lib_doc)

            resource, status_code = create_resource(document, id_token)
            return jsonify(resource), status_code

    else:
        return jsonify({"error": "api server error"}), 500
