from flaskr import logger, handler, line_bot_api
from flaskr.models import db, record
from flaskr.brain import add, isbn2message
from flaskr.errors import DuplicateUserError, DuplicateLibraryError
from hashlib import sha256
from linebot.models import MessageEvent, TextMessage, TextSendMessage


@handler.add(MessageEvent, message=TextMessage)
def chat(event=None):
    user_doc = record.user # copy the record to save user information
    userid = event.source.user_id if event else "testid"
    text = event.message.text if event else "some text"
    hashed_userid = sha256(userid.encode()).hexdigest()

    status = ""
    try:
        cmd = text.split(" ")
        if event.reply_token == "00000000000000000000000000000000":
            event = None
            return 200

        elif cmd[0] == "/addlib":
            add.favolib(event, {"systemid": cmd[1]})
            status = "Success!"

        elif cmd[0] == "liff":
            status = "https://liff.line.me/1654371886-xorapzM6"

        elif cmd[0].replace("-", "").isdigit():
            isbn2message(event, cmd[0].replace("-", ""))
            event = None

        else:
            status = "miss command"

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
