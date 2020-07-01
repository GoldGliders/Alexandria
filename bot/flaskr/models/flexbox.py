notfound = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://i.pinimg.com/originals/c6/5f/37/c65f370cbaf947842c35d6fe59cc8b9a.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://dic.nicovideo.jp/a/%E5%AE%87%E5%AE%99%E7%8C%AB"
                },
            "margin": "none"
            },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "本は見つかりませんでした",
                    "weight": "regular",
                    "size": "xl",
                    "align": "center"
                    }
                ]
            },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "spacer",
                    "size": "sm"
                    }
                ],
            "flex": 0
            }
        }


bookmeta = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://4.bp.blogspot.com/-2t-ECy35d50/UPzH73UAg3I/AAAAAAAAKz4/OJZ0yCVaRbU/s1600/book.png",
        "size": "xl",
        "aspectMode": "fit",
        },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "spacing": "sm",
        "paddingAll": "13px"
        },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "button",
                "style": "link",
                "action": {
                    "type": "uri",
                    "label": "詳細",
                    "uri": "https://calil.jp/"
                }
            },{
                "type": "button",
                "style": "link",
                "action": {
                    "type": "postback",
                    "label": "ブックマークに登録する",
                    "data": ""
                },
            }
        ]
    },
    "size": "kilo",
}

flex_bookstatus = {
    "type": "bubble",
    "hero": {
        "type": "image",
        "url": "https://4.bp.blogspot.com/-2t-ECy35d50/UPzH73UAg3I/AAAAAAAAKz4/OJZ0yCVaRbU/s1600/book.png",
        "size": "full",
        "aspectMode": "cover",
        },
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "spacing": "sm",
        "paddingAll": "13px"
        },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": []
    },
    "size": "kilo",
}

minitext = {
    "type": "text",
    "text": "somthing",
    "size": "md",
    "weight": "regular",
    "wrap": True
}

button = {
    "type": "button",
    "style": "link",
    "action": {
        "type": "uri",
        "label": "予約する",
        "uri": "https://calil.jp/"
    }
}
