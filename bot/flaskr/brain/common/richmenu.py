import os
from flaskr import logger, line_bot_api
from linebot.models import (
    RichMenu, RichMenuArea, RichMenuSize, RichMenuBounds,
    MessageAction, URIAction
)


WIDTH = 2500
HEIGHT = 1686
W = WIDTH // 3
H = HEIGHT // 2


def create_richmenu():
    """
    Create richmenu.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    None
    """

    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=False,
        name='richmenu',
        chat_bar_text='Menu',
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=W*0, y=H*0, width=W, height=H),
                action=MessageAction(text="bookmark")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=W*1, y=H*0, width=W, height=H),
                action=MessageAction(text="favolib")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=W*2, y=H*0, width=W, height=H),
                action=URIAction(uri="https://liff.line.me/1654371886-xorapzM6", label="history")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=W*0, y=H*1, width=W, height=H),
                action=MessageAction(text="option")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=W*1, y=H*1, width=W, height=H),
                #action=MessageAction(text="help")
                action=MessageAction(text="liff")
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=W*2, y=H*1, width=W, height=H),
                action=MessageAction(text="liff")
            )
        ]
    )
    richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

    # upload an image for rich menu
    path = "flaskr/static/images/richmenu/image.jpg"

    with open(path, 'rb') as f:
        line_bot_api.set_rich_menu_image(richMenuId, "image/jpeg", f)

    # set the default rich menu
    line_bot_api.set_default_rich_menu(richMenuId)
