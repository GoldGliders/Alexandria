import os
from flask import request, jsonify
from flaskr import bp, get_profile, logger
from flaskr.models import db
from hashlib import sha256


PREFECTURES = {
    "北海道": ["北海道"],
    "東北": ["青森県","岩手県","宮城県","秋田県","山形県","福島県"],
    "関東": ["茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県"],
    "中部": ["新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県", "静岡県","愛知県"],
    "近畿": ["三重県","滋賀県","京都府","大阪府","兵庫県", "奈良県","和歌山県"],
    "中国": ["鳥取県","島根県","岡山県","広島県","山口県"],
    "四国": ["徳島県","香川県","愛媛県","高知県"],
    "九州・沖縄": ["福岡県","佐賀県","長崎県", "熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
}


@bp.route("/onelibrary", methods=["GET"])
def get_arealib():
    fieldName = ["area", "pref", "city", "library"]
    fieldValue = list(map(lambda x: request.args.get(x), fieldName))
    args = request.args
    level = int(args.get("level"))
    logger.debug(args)
    items = list()

    if level == 1:
        items = PREFECTURES[args.get("area")]

    elif level == 2:
        filters = [
            ("pref", "==", args.get("pref"))
        ]
        resp = db.library.filter(filters)
        # city names
        items = list(set(map(lambda x: x["city"], resp.values())))

    elif level == 3:
        filters = [
            ("pref", "==", args.get("pref")),
            ("city", "==", args.get("city"))
        ]
        # library info
        items = list(db.library.filter(filters).values())

    elif level == 4:
        # register the library
        pass

    return jsonify({"items": items}), 200
