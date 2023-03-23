import datetime
import hashlib

from aiogram import types


async def save_img(img_str: str):
    name = hashlib.md5(img_str.encode()).hexdigest()
    with open(f"images/{name}", "wb") as f:
        f.write(img_str.encode())
    return name


async def get_img(name: str):
    with open(f"images/{name}", "rb") as f:
        resp = f.read()
    return resp.decode()


async def get_seconds(date:str, time:str):
    s = date + "-" + time
    s = s.replace(":", "-")
    z = list(map(int, s.split("-")))
    resp = (datetime.datetime(*z) - datetime.datetime.now()).seconds
    return resp

async def get_keyboard(buttons: list | None = None, ref: str | None = None) -> None | types.InlineKeyboardMarkup:
    if buttons == []:
        return None
    if buttons == None:
        return None
    kb = types.InlineKeyboardMarkup()
    for i in buttons:
        row_btns = (types.InlineKeyboardButton(j["text"],
                                               url=(j["link"].replace("{}", ref) if ref is not None else j["link"])) for j in i)
        kb.row(*row_btns)
    return kb



