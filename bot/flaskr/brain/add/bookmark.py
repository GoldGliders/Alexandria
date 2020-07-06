import json
import time
from flaskr import logger
from flaskr.models import db, record
from flaskr.errors import DuplicateBookError, DuplicateUserError, UserNotFound
from hashlib import sha256


def add_bookmark(event=None):
    """
    Register new bookmark at specified user.

    Parameters
    ----------
    event: LINE event
        LINE event

    Returns
    -------
    status: str
        Return status string.

    Raises
    ------
    UserNotFound
        Raises UserNotFound if user is not registered.
    DuplicateBookError
        Raises DuplicateLibraryError if new book is already registered.
    """

    bookmeta = record.bookmeta
    book_doc = record.book_doc
    status = ""
    userid = event.source.user_id if event else "testid"
    hashed_userid = sha256(userid.encode()).hexdigest()

    postback_data = event.postback.data.replace("'", '"') # replace single quotation to double
    waitingbook = json.loads(postback_data)
    if hashed_userid in db.users.find({"userid": hashed_userid}):
        raise DuplicateUserError

    if db.users.count() == 0:
        raise UserNotFound

    bookmarks = db.users.find_one({"userid": hashed_userid})["bookmarks"]
    logger.debug(f"registared bookmarks: {bookmarks}")

    if waitingbook["isbn"] in list(map(lambda x: x["bookmeta"]["isbn"], bookmarks)):
        raise DuplicateBookError

    bookmeta["title"] = waitingbook["title"]
    bookmeta["author"] = waitingbook["author"]
    bookmeta["isbn"] = waitingbook["isbn"]
    book_doc["timestamp"] = int(time.time())
    book_doc["bookmeta"] = bookmeta
    logger.debug(f"addtional book marks: {book_doc}")

    bookmarks.append(book_doc)
    db.users.update_one(
        {"userid": hashed_userid},
        {"$set": {"bookmarks": bookmarks}}
    )  # update bookmarks
    logger.info(f"{bookmarks} is registared")
    status = "本が登録されました"

    return status
