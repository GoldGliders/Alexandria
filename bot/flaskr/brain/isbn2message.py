from flaskr import logger
from flaskr import handler, line_bot_api
from flaskr.errors import DuplicateUserError, BookNotFound, MetadataNotFound, UserNotFound
from flaskr.models import db, record, flexbox
from flaskr.brain import add, call_api, send
from hashlib import sha256
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

def isbn2message(event, isbn):
    """
    Create from isbn to message and send it.

    Parameters
    ----------
    event: LINE event
        LINE event
    isbn: str
        The isbn which a user input.

    Returns
    -------
    None

    Raises
    ------
    None
    """

    userid = event.source.user_id if event else "testid"
    hashed_userid = sha256(userid.encode()).hexdigest()
    favolib = db.users.find_one({"userid": hashed_userid})["favolib"]
    logger.debug(favolib)
    bookstatus = []

    try:
        bookdoc = call_api.openbd(isbn)
        if bookdoc:
            flex_message = send.bookmeta(bookdoc)
            add.history(event, bookdoc)

        else:
            bookdoc, flex_message = send.compact_bookmeta(isbn)
            add.history(event, bookdoc)

        line_bot_api.push_message(
            event.source.user_id,
            messages=flex_message
        )

        for library in favolib:
            try:
                bookstatus.append(call_api.calil(isbn, library["systemid"]))
            except BookNotFound:
                pass

        if bookstatus:
            # When you cannot get book meta information from google books api, you pass NoneType to this function.
            flex_message = send.bookstatus(bookstatus)
            line_bot_api.reply_message(
                event.reply_token,
                messages=flex_message
            )
            event = None

        else:
            raise BookNotFound

    except MetadataNotFound:
        pass

    except BookNotFound:
        logger.info("book not found")
        status = "book not found"

    except Exception as e:
        logger.info(e)
        status = "Fail"

    finally:
        # A message is already sent, event is None.
        if event:
            flexcontent = flexbox.notfound
            flexcontent["body"]["contents"][0]["text"] = status
            line_bot_api.reply_message(
                event.reply_token,
                messages=FlexSendMessage(alt_text=status, contents=flexcontent)
            )
