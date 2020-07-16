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
    resource, status_code = get_resource("bookmark", idToken)
    return jsonify(resource), status_code


@bp.route("/library", methods=["GET"])
def get_library():
    idToken = request.args.get("idToken")
    resource, status_code = get_resource("favolib", idToken)
    return jsonify(resource), status_code

@bp.route("/option", methods=["GET"])
def get_option():
    title = ""
    isbn = ""
    idToken = request.args.get("idToken")
    resource, status_code = get_resource("options", idToken)

    links_names = {
        # "calil": {
        #    "link": f"https://calil.jp/book/{isbn}",
        #    "displayName": "詳細"
        #},
        "google": {
            "link": f"https://www.google.com/search?q={isbn}",
            "displayName": "Google"
        },
        "honto": {
            "link": f"https://honto.jp/netstore/search_10{title}.html",
            "displayName": "honto"
        },
        "amazon": {
            "link": f"https://amazon.co.jp/s?k={title}",
            "displayName": "Amazon"
        },
        "rakuten": {
            "link": f"https://search.rakuten.co.jp/search/mall/{title}/",
            "displayName": "楽天"
        },
        "yodobashi": {
            "link": f"https://www.yodobashi.com/category/81001/?word={isbn}",
            "displayName": "ヨドバシドットコム"
        },
        "yahoo": {
            "link": f"https://shopping.yahoo.co.jp/search?&p={title}",
            "displayName": "ヤフーショッピング"
        },
        "mercari": {
            "link": f"https://www.mercari.com/jp/search/?keyword={title}&category_root=5",
            "displayName": "メルカリ"
        },
        "rakuma": {
            "link": f"https://fril.jp/s?query={title}&category_id=733",
            "displayName": "ラクマ"
        },
        "paypayfleamarket": {
            "link": f"https://paypayfleamarket.yahoo.co.jp/search/{title}?categoryIds=10002",
            "displayName": "PayPayフリマ"
        },
    }
    display_name = {key: values["displayName"] for key, values in links_names.items()}

    resource["items"].pop("calil")
    res = {
        "items": {
            "options": resource["items"],
            "displayName": display_name
        }
    }
    logger.debug(res)

    return jsonify(res), status_code
