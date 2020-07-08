from flaskr import logger
from flaskr.errors import BookNotFound, MetadataNotFound
from flaskr.models import db
from hashlib import sha256


def add_history(event=None, bookdoc=None):
    """
    Register new history at specified user.

    Parameters
    ----------
    event: LINE event
        LINE event
    libinfo: dict
        New library book document.

    Returns
    -------
    None

    Raises
    ------
    None
    """

    userid = event.source.user_id if event else "testid"
    hashed_userid = sha256(userid.encode()).hexdigest()
    user_doc = db.user.find(hashed_userid)
    history = user_doc["history"]

    try:
        logger.debug(f"hashed userid: {hashed_userid}, history: {history}")

        history.append(bookdoc)
        logger.debug(f"registaring history: {bookdoc}")

        user_doc["history"] = history
        db.user.set(hashed_userid, user_doc)  # update history
        logger.debug(f"successed in registaring history")

    except Exception as e:
        logger.info(e)
