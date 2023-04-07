import io
import requests
from aiogram import Dispatcher, Bot, types
from aiogram.types import FSInputFile
import utils.utls
import cfg
from PIL import Image, GifImagePlugin
bot = Bot(token=cfg.TG_TOKEN, parse_mode="HTML")


async def send_photo(*, tg_id: int, file_name: str, text: str, kb: types.ReplyKeyboardMarkup = None):
    await bot.send_photo(chat_id=tg_id, photo=FSInputFile(f"files/{file_name}"), caption=text, reply_markup=kb)

async def send_gif(*, tg_id: int, file_name: str, text: str, kb: types.ReplyKeyboardMarkup = None):
    await bot.send_animation(chat_id=tg_id, animation=FSInputFile(f"files/{file_name}"), caption=text, reply_markup=kb)

async def send_video(*, tg_id: int, file_name: str, text: str, kb: types.ReplyKeyboardMarkup = None):
    await bot.send_video(chat_id=tg_id, video=FSInputFile(f"files/{file_name}"), caption=text, reply_markup=kb, supports_streaming=True)


async def pre_send_post(*, tg_data: dict, post: dict):
    tg_id = tg_data.get("tg_id")
    if str(tg_id).isdigit():
        tg_id = int("-100" + str(tg_id))
    ref = tg_data.get("ref")
    text = post.get("post_text").replace("{}", ref or "")
    kb: None | types.InlineKeyboardMarkup = await utils.utls.get_keyboard(post["buttons"], ref)
    file_name: str = post.get("file_name")
    if file_name.endswith(tuple(cfg.img_extensions)):
        await send_photo(tg_id=tg_id, file_name=file_name, text=text, kb=kb)
    if file_name.endswith(tuple(cfg.gif_extensions)):
        await send_gif(tg_id=tg_id, file_name=file_name, text=text, kb=kb)
    if file_name.endswith(tuple(cfg.video_extensions)):
        await send_video(tg_id=tg_id, file_name=file_name, text=text, kb=kb)

