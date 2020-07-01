from flaskr import logger, handler, line_bot_api
from flaskr.brain import isbn2message
from flaskr.errors import DuplicateUserError, IsbnNotFound, BookNotFound
from io import BytesIO
from linebot.models import MessageEvent, TextSendMessage, ImageMessage
from pyzbar.pyzbar import decode
from PIL import Image


@handler.add(MessageEvent, message=ImageMessage)
def img2message(event=None):
    try:
        img = line_bot_api.get_message_content(event.message.id).content
        isbn = img2isbn(BytesIO(img))
        logger.info(f"ISBN detected: {isbn}")
        isbn2message(event, isbn)

    except IsbnNotFound:
        logger.info("isbn not found")

    except BookNotFound:
        logger.info("book not found")

    except Exception as e:
        logger.info(e)


def img2isbn(img):
    try:
        barcodes = list(map(lambda barcode: str(barcode[0].decode("utf-8")), decode(Image.open(img)))) # detect multiple barcodes
        isbn = list(filter(lambda barcode: barcode[0] == "9", barcodes))[0] # use the first detected barcode which starts with 9 as detected isbn
        logger.debug(f"detected barcodes: {barcodes}")

    except (OSError, IndexError):
        raise IsbnNotFound

    else:
        return isbn
