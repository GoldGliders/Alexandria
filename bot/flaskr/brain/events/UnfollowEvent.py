from flaskr import logger, handler, line_bot_api
from flaskr.models import db, record
from flaskr.errors import UserNotFound
from hashlib import sha256
from linebot.models import UnfollowEvent, TextSendMessage


@handler.add(UnfollowEvent)
def unfollowevent(event=None):
    user_doc = record.user # copy the record to save user information
    userid = event.source.user_id if event else "testid"
    hased_userid = sha256(userid.encode()).hexdigest()

    status = ""
    try:
        if db.users.find_one({"userid": hased_userid}) is None:
            raise UserNotFound
        db.users.delete_one({"userid": hased_userid})
        logger.info("Successed in removing follower!")
        status = "削除"

    except UserNotFound:
        logger.info("This user is not registared.")
        status = "This user is not registared."

    except Exception as e:
        logger.info("Faild to removing a follower!")
        logger.info(e)
        status = "Fail"

    return status
