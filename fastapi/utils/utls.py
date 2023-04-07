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
    new_buttons = []
    for buttons_row in buttons:
        new_row = []
        for button in buttons_row:
            new_row.append(
                types.inline_keyboard_button.InlineKeyboardButton(
                    text=button["text"],
                    url=button["link"].replace("{}", ref) if ref is not None else button["link"]
                )
            )
        new_buttons.append(new_row)
    new_keyboard = types.inline_keyboard_markup.InlineKeyboardMarkup(inline_keyboard=new_buttons)
    return new_keyboard
