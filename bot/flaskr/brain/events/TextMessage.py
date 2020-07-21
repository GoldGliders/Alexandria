from flaskr import logger, handler, line_bot_api
from flaskr.models import db, record
from flaskr.brain import add, isbn2message
from flaskr.errors import DuplicateUserError, DuplicateLibraryError
from hashlib import sha256
from linebot.models import MessageEvent, TextMessage, TextSendMessage

HELP = \
"""
---使い方---
メニューの"Library"欄から、検索対象にしたい図書館を選びます（複数可）。
そのあと本の裏にあるバーコードの写真か、その下に書いてある13桁の数字を送ってください。
数秒後に本についての情報と検索対象の図書館にその本が在書しているかどうかが分かります。


---メニューの説明---
検索した本の情報カードにある"ブックマークに登録する"を選ぶとブックマークに登録されます。
登録した本はメニューの"Bookmark"欄にて確認できます。

検索した本の履歴は残ります。
検索した本はメニューの"History"欄にて確認できます。
虫眼鏡ボタンを押すと再検索できます。

検索対象の図書館はメニューの"Library"欄にて管理できます。

このボットでは本を検索すると同時に、その本が売られているオンラインショップへのショートカットボタンを提供しています。
メニューの"Option"欄にてショートカットボタンの表示の有無をサイトごとに変更できます。


---ヒント---
現状では登録できるブックマークの数、図書館の数に制限は設けていません。
ただしこれほボットの運用状況によって変更する可能性があるのでご了承ください。
検索対象の図書館を一件増やすたびにレスポンスが2秒ほど遅くなります。
速いレスポンスをお望みの方は検索対象の図書館の数を減らしてみてください。
"""


@handler.add(MessageEvent, message=TextMessage)
def chat(event=None):
    # user_doc = record.user # copy the record to save user information
    # userid = event.source.user_id if event else "testid"
    # hashed_userid = sha256(userid.encode()).hexdigest()
    text = event.message.text if event else "some text"

    status = ""
    try:
        cmd = text.split(" ")
        if event.reply_token == "00000000000000000000000000000000":
            event = None
            return 200

        elif cmd[0] == "help":
            status = HELP

        elif cmd[0].replace("-", "").isdigit() and len(cmd[0].replace("-", "")) == 13:
            isbn2message(event, cmd[0].replace("-", ""))
            event = None

        else:
            status = "すみません、よくわかりません。"

        logger.info("Successed chatting!")

    except DuplicateLibraryError:
        status = "This library is already registared"

    except Exception as e:
        logger.info("Faild to registaring new follower!")
        logger.info(e)
        status = "Fail"

    finally:
        if event:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text=status)
            )

    return status
