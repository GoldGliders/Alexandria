from flaskr import logger, handler, line_bot_api
from flaskr.models import db
from flaskr.errors import UserNotFound
from hashlib import sha256
from linebot.models import UnfollowEvent, TextSendMessage



@handler.add(UnfollowEvent)
def unfollowevent(event=None):
    userid = event.source.user_id if event else "testid"
    hashed_userid = sha256(userid.encode()).hexdigest()

    status = ""
    try:
        if db.user.find(hashed_userid):
            raise UserNotFound

        db.user.remove(hashed_userid)
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
