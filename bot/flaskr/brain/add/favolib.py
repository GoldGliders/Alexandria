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

    # libinfo  = {"formal": "会津大学附属図書館", "systemid": "Univ_Aizu"}
    if libinfo is None:
        libinfo = {"formal": "会津大学附属図書館", "systemid": "Univ_Aizu"}
    elif libinfo.get("formal") is None:
        libinfo["formal"] = db.libraries.find_one(
            {"systemid": libinfo["systemid"]})["formal"]

    # confirmation the user is unique
    if hashed_userid not in db.users.find_one({"userid": hashed_userid})["userid"]:
        raise UserNotFound

    favolib = db.users.find_one({"userid": hashed_userid})["favolib"]
    logger.debug(f"registered favorite libraries: {favolib}")

    if libinfo["formal"] in list(map(lambda x: x["formal"], favolib)):
        raise DuplicateLibraryError

    # get info of one library from mongo db
    libinfo = db.libraries.find_one(
        {"systemid": libinfo["systemid"],
         "formal": libinfo["formal"]}
    )
    # make favorite library doc
    lib_doc["timestamp"] = int(time.time())
    lib_doc["formal"] = libinfo["formal"]
    lib_doc["systemid"] = libinfo["systemid"]
    logger.debug(f"additional favorite library: {lib_doc}")

    favolib.append(lib_doc)
    db.users.update_one(
        {"userid": hashed_userid},
        {"$set": {"favolib": favolib}}
    )  # update favorite library
    logger.info(f"{favolib} is registared")
    status = "success"

    return status
