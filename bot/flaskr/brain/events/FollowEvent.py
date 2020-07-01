from flaskr import logger, handler, line_bot_api
from  flaskr.errors import DuplicateUserError
from flaskr.models import db, record
from hashlib import sha256
from linebot.models import FollowEvent, TextSendMessage


@handler.add(FollowEvent)
def followevent(event=None):
    user_doc = record.user  # copy the record to save user information
    userid = event.source.user_id if event else "testid"
    hashed_userid = sha256(userid.encode()).hexdigest()

    user_doc["userid"] = hashed_userid
    user_doc["context"] = ""
    user_doc["options"] = {"Amazon": False, "Rakuten": False, "Yahoo": False, "Mercali": False}

    status = ""
    try:
        logger.debug(user_doc)
        if hashed_userid in db.users.find({"userid": hashed_userid}):
            raise DuplicateUserError

        db.users.insert(user_doc)
        logger.info("Successed in registaring new follower!")
        status = "登録アザス"

    except DuplicateUserError:
        logger.info("This user is already registared.")
        status = "This user is already registared"

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
