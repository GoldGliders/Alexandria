import time
from flaskr import logger
from flaskr.models import db, record
from flaskr.errors import DuplicateLibraryError, UserNotFound
from hashlib import sha256


def add_favoilib(event=None, libinfo=None):
    """
    Register new library at specified user.

    Parameters
    ----------
    event: LINE event
        LINE event
    libinfo: dict
        New library information.

    Returns
    -------
    status: str
        Return status string.

    Raises
    ------
    UserNotFound
        Raises UserNotFound if user is not registered.
    DuplicateLibraryError
        Raises DuplicateLibraryError if new library is already registered.

    """

    lib_doc = record.library
    status = ""
    userid = event.source.user_id if event else "testid"
    hashed_userid = sha256(userid.encode()).hexdigest()
    logger.debug(event)

    # test code
    # libinfo  = {"formal": "会津大学附属図書館", "systemid": "Univ_Aizu"}
    if libinfo is None:
        libinfo = {"formal": "会津大学附属図書館", "systemid": "Univ_Aizu", "libid": "104688"}

    # confirmation of uniquness of the user
    if db.user.find(hashed_userid) is None:
        logger.info("user not found")
        raise UserNotFound

    user_doc = db.user.find(hashed_userid)
    favolib = user_doc["favolib"]
    logger.debug(f"registered favorite libraries: {favolib}")

    if libinfo["libid"] in list(map(lambda x: x["libid"], favolib)):
        raise DuplicateLibraryError

    # get info of one library from db
    libinfo = db.library.find(libinfo["libid"])
    # make favorite library doc
    lib_doc["timestamp"] = int(time.time())
    lib_doc["formal"] = libinfo["formal"]
    lib_doc["libid"] = libinfo["libid"]
    lib_doc["systemid"] = libinfo["systemid"]
    logger.debug(f"additional favorite library: {lib_doc}")

    favolib.append(lib_doc)
    user_doc["favolib"] = favolib
    db.user.set(hashed_userid, user_doc)  # update favorite library
    logger.info(f"{favolib} is registared")
    status = "success"

    return status
