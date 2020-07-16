import os
import requests
import time
from copy import deepcopy
from flaskr import logger
from flaskr.errors import BookNotFound
from flaskr.models import flexbox, db, record
from linebot.models import FlexSendMessage
from lxml import html
from urllib.parse import urlencode, quote


def add_links(hashed_userid, title, isbn):
    title = quote(title)
    user_doc = db.user.find(hashed_userid)
    options = user_doc["options"]
    links_names = {
        "calil": {
            "link": f"https://calil.jp/book/{isbn}",
            "displayName": "詳細"
        },
        "google": {
            "link": f"https://www.google.com/search?q={isbn}",
            "displayName": "Google"
        },
        "honto": {
            "link": f"https://honto.jp/netstore/search_10{title}.html",
            "displayName": "honto"
        },
        "amazon": {
            "link": f"https://amazon.co.jp/s?k={title}",
            "displayName": "Amazon"
        },
        "rakuten": {
            "link": f"https://search.rakuten.co.jp/search/mall/{title}/",
            "displayName": "楽天"
        },
        "yodobashi": {
            "link": f"https://www.yodobashi.com/category/81001/?word={isbn}",
            "displayName": "ヨドバシドットコム"
        },
        "yahoo": {
            "link": f"https://shopping.yahoo.co.jp/search?&p={title}",
            "displayName": "ヤフーショッピング"
        },
        "mercari": {
            "link": f"https://www.mercari.com/jp/search/?keyword={title}&category_root=5",
            "displayName": "メルカリ"
        },
        "rakuma": {
            "link": f"https://fril.jp/s?query={title}&category_id=733",
            "displayName": "ラクマ"
        },
        "paypayfleamarket": {
            "link": f"https://paypayfleamarket.yahoo.co.jp/search/{title}?categoryIds=10002",
            "displayName": "PayPayフリマ"
        },
    }

    chunk_list = list()
    for key, enable in options.items():
        if enable:
            name = links_names[key]["displayName"]
            link = links_names[key]["link"]
            chunk_list.append([name, link])

    # swap
    num = list(map(lambda x: x[0], chunk_list)).index("詳細")
    chunk_list[num], chunk_list[-1] = chunk_list[-1], chunk_list[num]

    return chunk_list

def bookmeta(book_doc, hashed_userid):
    """
    Create from book_doc to flexbox and return it.

    Parameters
    ----------
    book_doc: dict
        Book status.

    Returns
    -------
    flex_message: dict
        Flex message style dict.

    Raises
    ------
    None

    See also
    --------
    flaskr.models.record.book_doc
    """

    meta = book_doc["bookmeta"]
    flex_bookmeta = deepcopy(flexbox.bookmeta)
    bookmeta = deepcopy(record.bookmeta)

    # variable of meta contains too much information, so bookmeta is less than it.
    bookmeta["isbn"] = meta["isbn"]
    bookmeta["title"] = meta["title"]
    bookmeta["author"] = meta["author"]

    # key: {size: text size, weight: text weight, prefix: prefix of bookmeta[key]}
    order = {
        "title": {"size": "xl", "weight": "bold"},
        "subtitle": {"size": "lg"},
        "author": {"prefix": "著者: "},
        "publisher": {"prefix": "出版社: "},
        "publishdate": {"prefix": "出版日: "},
        "page": {"prefix": "ページ数: "}
    }

    for key in order:
        # some meta[key] are "" (not specified)
        if meta[key]:
            minitext = deepcopy(flexbox.minitext)
            minitext["text"] = order[key].get("prefix", "") + meta[key]
            minitext["size"] = order[key].get("size", "md")
            minitext["weight"] = order[key].get("weight", "regular")
            flex_bookmeta["body"]["contents"].append(deepcopy(minitext))

    # if None, then use an image from irasutoya
    flex_bookmeta["hero"]["url"] = meta["image"] if meta["image"] else "https://4.bp.blogspot.com/-2t-ECy35d50/UPzH73UAg3I/AAAAAAAAKz4/OJZ0yCVaRbU/s1600/book.png"

    buttons = list()
    options = add_links(hashed_userid, meta["title"], meta["isbn"])
    for name, link in options:
        logger.debug(link)
        button = {
            "type": "button",
            "style": "link",
            "action": {
                "type": "uri",
                "label": name,
                "uri": link
            }
        }
        buttons.append(button)

    button = {
        "type": "button",
        "style": "link",
        "action": {
            "type": "postback",
            "label": "ブックマークに登録する",
            "data": f"{bookmeta}"
        },
    }

    buttons.append(button)
    flex_bookmeta["footer"]["contents"] = buttons

    flex_message = FlexSendMessage(
        alt_text="book information",
        contents=flex_bookmeta
    )


    return flex_message


def compact_bookmeta(isbn):
    """
    Create from isbn to flexbox and return it.

    Parameters
    ----------
    isbn: str
        The isbn which openbd does not much information.

    Returns
    -------
    flex_message: dict
        Normal flex message.

    Raises
    ------
    BookNotFound
        There is no information in calil website.
    """

    # scrape from calil web site, not api
    url = f"https://calil.jp/book/{isbn}"
    title_xpath = '//*[@id="ccontent"]/div/div[1]/div[2]/div/div[2]/h1'
    author_xpath = '//*[@id="ccontent"]/div/div[1]/div[2]/div/div[2]/p/a'
    rq = requests.get(url)
    status_code = rq.status_code

    if status_code == 200:
        minitext = deepcopy(flexbox.minitext)
        flex_bookmeta = deepcopy(flexbox.bookmeta)
        bookmeta = deepcopy(record.bookmeta)

        tree = html.fromstring(rq.content)
        title = tree.xpath(title_xpath)[0].text.replace(
            " ", "").replace("\n", "")
        author = tree.xpath(author_xpath)[0].text.replace(
            " ", "").replace("\n", "")

        bookmeta["isbn"] = isbn
        bookmeta["title"] = title
        bookmeta["author"] = author

        minitext["text"] = title
        minitext["size"] = "xl"
        flex_bookmeta["body"]["contents"].append(minitext)

        content = list()
        content.append({
            "type": "button",
            "style": "link",
            "action": {
                "type": "uri",
                "label": "詳細",
                "uri": "https://calil.jp/book/{isbn}"
            }
        })

        content.append({
            "type": "button",
            "style": "link",
            "action": {
                "type": "postback",
                "label": "ブックマークに登録する",
                "data": bookmeta
            },
        })

        flex_bookmeta["footer"]["contents"] = content
        logger.debug(flex_bookmeta)

        flex_message = FlexSendMessage(
            alt_text='book information',
            contents=flex_bookmeta
        )

        return (bookmeta, flex_message)

    else:
        raise BookNotFound


def bookstatus(bookstatus):
    """
    Create from bookstatus to flexbox and return it.

    Parameters
    ----------
    bookstatus: list
       List of bookstatus which is searched in different libraries.

    Returns
    -------
    flex_message: dict
        Carousel flex message.
    Raises
    ------
    BookNotFound
        There is no information in calil website.
    """

    flexboxes = []
    for status, systemid in bookstatus:
        flex_bookstatus = deepcopy(flexbox.flex_bookstatus)
        try:
            flex_bookstatus["hero"]["url"] = "https://3.bp.blogspot.com/-FJiaJ8gidCs/Ugsu-rSFw0I/AAAAAAAAXNA/JFiIUoxggW4/s800/book_tate.png"
            """
            if os.path.exists(f"./flaskr/static/images/library/{systemid}.jpg"):
                flex_bookstatus["hero"]["url"] = f"/static/images/library/{systemid}.jpg"
            else:
                flex_bookstatus["hero"]["url"] = "https://3.bp.blogspot.com/-FJiaJ8gidCs/Ugsu-rSFw0I/AAAAAAAAXNA/JFiIUoxggW4/s800/book_tate.png"
            """

            library = db.library.filter("systemid", "==", systemid)
            libid = list(library.keys())[0]
            minitext = deepcopy(flexbox.minitext)
            systemname = library[libid]["systemname"]

            # both reserveurl and libkey are None
            if (status.get("reserveurl") and status.get("libkey")) is False:
                minitext["text"] = f"{systemname}: 在書"
                flex_bookstatus["body"]["contents"].append(minitext)

            else:
                minitext["text"] = systemname
                minitext["size"] = "lg"
                minitext["weight"] = "bold"
                flex_bookstatus["body"]["contents"].append(minitext)

            if status.get("libkey"):
                text = ""
                keylist = status["libkey"].keys()

                # status depends on libraries
                minitext = deepcopy(flexbox.minitext)
                for libkey in keylist:
                    # short = library[libid]["short"] if library else libkey
                    state = status["libkey"][libkey]
                    text += f"{libkey}: {state}\n"

                minitext["text"] = text
                flex_bookstatus["body"]["contents"].append(minitext)

            if status.get("reserveurl"):
                button = deepcopy(flexbox.button)
                button["action"]["uri"] = status["reserveurl"]
                flex_bookstatus["footer"]["contents"].append(button)

            logger.debug(flex_bookstatus)
            flexboxes.append(flex_bookstatus)

        except KeyError:
            pass

        except Exception as e:
            logger.info(e)

    carousel = {
        "type": "carousel",
        "contents": flexboxes
    }

    flex_message = FlexSendMessage(
        alt_text='book status information',
        contents=carousel
    )

    return flex_message
