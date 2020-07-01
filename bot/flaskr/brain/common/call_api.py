import os
import requests
import time
from copy import deepcopy
from flaskr import logger
from flaskr import handler
from flaskr.errors import BookNotFound, MetadataNotFound
from flaskr.models import record


def calil(isbn, systemid):
    """
    Call calil api and return book status.

    Parameters
    ----------
    isbn: str
        The isbn of a book users want to know the status. It is 13 digits.
    sytemid:
        The systemid of a library where users want to know the book status.

    Returns
    -------
    book_doc: dict
        Return book_doc with status of the book specified with isbn at the library doen with systemid.

    Raises
    ------
    BookNotFound
        None of keys are found in calil api response or some unexpected exception is occured.

    See also
    --------
    flaskr.models.record.book_doc
    """

    url = "http://api.calil.jp/check?&format=json&callback=no&appkey={" + os.getenv("CALIL_API_KEY") + "}"
    queries = f"&isbn={isbn}&systemid={systemid}"
    # bookquery = json.loads(requests.get(url+queries).text)
    bookquery = requests.get(url + queries).json()
    """
    Response example
    {"session": "ea5e50999e96d1cd4361f6e1892ff4da", "books": {"9784873117836": {"Univ_Aizu": {"status": "Cache", "reserveurl": "https://libeopsv.u-aizu.ac.jp/gate?module=search&path=detail.do&method=detail&bibId=1000014556&bsCls=0", "libkey": {"４大": "貸出中"}}}}, "continue": 0}
    '"""
    logger.debug(bookquery)

    try:
        # When status is running, you have to wait a few seconds for detail information.
        cnt = 0
        # Call api again and again. If 10 times called, break
        while (bookquery["continue"] == 1 and cnt < 10):
            time.sleep(1)
            # Call by session
            queries = f"&session={bookquery['session']}"
            #bookquery = json.loads(requests.get(url+queries).text)
            bookquery = requests.get(url+queries).json()
            logger.debug(f"session: {bookquery}")
            cnt += 1

        bookstatus = {}
        found = False
        bookquery_isbn = bookquery["books"][isbn]
        # If one or more keys are found, return bookstatus.
        for query_systemid in bookquery_isbn.keys():
            reserveurl = bookquery_isbn[query_systemid].get("reserveurl")
            libkey = bookquery_isbn[query_systemid].get("libkey")
            if reserveurl or libkey:
                found = True
                bookstatus = ({"systemid": query_systemid, "reserveurl": reserveurl, "libkey": libkey})

        # If none of keys are found, raise BookNotFound.
        if found is False:
            raise BookNotFound

    except Exception as e:
        logger.info(e)
        raise BookNotFound

    else:
        logger.debug(f"bookstatus: {bookstatus}")
        return bookstatus


def openbd(isbn):
    """
    Call openbd api and return book meta data.

    Parameters
    ----------
    isbn: str
        The isbn of a book users want to know the status. It is 13 digits.

    Returns
    -------
    book_doc: dict
        Return book_doc with status of the book specified with isbn at the library doen with systemid.

    Raises
    ------
    UserNotFound
        Raises UserNotFound if user is not registered.
    DuplicateBookError
        Raises DuplicateLibraryError if new book is already registered.
    BookNotFound
        None of keys are found in calil api response or some unexpected exception is occured.

    See also
    --------
    flaskr.models.record.bookmeta
    flaskr.models.record.book_doc
    """

    url = f"https://api.openbd.jp/v1/get?isbn={isbn}"
    bookmeta = record.bookmeta
    book_doc = record.book_doc

    try:
        bookmeta["isbn"] = isbn
        # resourse path at the response
        # keyname: {path: path to resource, name: replace keyname to this name for easily understanding}
        necessary_keys = {
            "TitleText": {"path": "onix/DescriptiveDetail/TitleDetail/TitleElement/TitleText/content", "name": "title"},
            "Subtitle": {"path": "onix/DescriptiveDetail/TitleDetail/TitleElement/Subtitle/content", "name": "subtitle"},
            "PersonName": {"path": "onix/DescriptiveDetail/Contributor/0/PersonName/content", "name": "author"},
            "ExtentValue": {"path": "onix/DescriptiveDetail/Extent/0/ExtentValue", "name": "page"},
            "ResourceLink": {"path": "onix/CollateralDetail/SupportingResource/0/ResourceVersion/0/ResourceLink", "name": "image"},
            "ImprintName": {"path": "onix/PublishingDetail/Imprint/ImprintName", "name": "publisher"},
            "Date": {"path": "onix/PublishingDetail/PublishingDate/0/Date", "name": "publishdate"}
        }

        openbd = requests.get(url).json()[0]
        contain_keylist = get_keys(openbd, [])
        for key in necessary_keys.keys():
            if key in contain_keylist:
                content = find_resource(openbd, necessary_keys[key]["path"], 0)
            else:
                content = ""
            bookmeta[necessary_keys[key]["name"]] = content
        book_doc["timestamp"] = int(time.time())
        book_doc["bookmeta"] = bookmeta
        logger.debug(book_doc)

    except Exception as e:
        book_doc = ""
        logger.info(e)

    finally:
        return book_doc


def get_keys(target, keylist):
    """
    Get deep keys at json data converted to dict.

    Parameters
    ----------
    target: dict or list
        Target dict or list at searching level.
    keylist: list
        Searched keylist.

    Returns
    -------
    keylist: list
        Searched keylist.
    """

    if isinstance(target, dict):
        keys = target.keys()
        keylist.extend(keys)
        for key in keys:
            get_keys(target[key], keylist)
        return keylist

    elif isinstance(target, list):
        for dct in target:
            get_keys(dct, keylist)
    else:
        return


def find_resource(target, path, level):
    """
    Get deep resource at json data converted to dict.

    Parameters
    ----------
    target: dict or list
        Target dict or list at searching level.
    path: str
        Path to the target resource.
    level: int
        Number of searching level which begins from 0.

    Returns
    -------
    target: str
        Target resource.
    """

    if isinstance(target, (list, dict)):
        key = path.split("/")[level]
        # key is not only str, but also int
        if key.isdigit():
            key = int(key)
        return find_resource(target[key], path, level+1)

    else:
        return target
