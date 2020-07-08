from flaskr import logger, handler, line_bot_api
from flaskr.brain import add
from flaskr.errors import DuplicateBookError, DuplicateUserError, UserNotFound
from linebot.models import PostbackEvent, TextSendMessage


@handler.add(PostbackEvent)
def add_library(event=None, libinfo=None):
    try:
        status = add.favolib(event, libinfo)

    except InvalidName:
        logger.info("This user is not registared.")
        status = "This user is not registared"

    except DuplicateLibraryError:
        logger.info("This library is already registared.")
        status = "This library is already registared"

    except Exception as e:
        logger.info(e)
        status = "fail"

    finally:
        if event:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text=status)
            )


@handler.add(PostbackEvent)
def add_bookmark(event=None):
    try:
        status = add.bookmark(event)

    except DuplicateUserError:
        logger.info("This user is already registared.")
        status = "This user is already registared"

    except DuplicateBookError:
        logger.info("This book is already registared.")
        status = "This book is already registared"

    except UserNotFound:
        logger.info("Users are not found.")
        status = "Users are not found."

    except Exception as e:
        logger.info(e)
        status = "fail"

    finally:
        if event:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text=status)
            )
