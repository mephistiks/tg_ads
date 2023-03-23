import json
import base64
from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from fastapi import APIRouter, Request, status, Response, Body
from fastapi.encoders import jsonable_encoder

from fastapi import File, UploadFile
import os

import cfg
import models.post
import utils.utls
from utils.utls import save_img
import dbq

router = APIRouter()

bot = Bot(token=cfg.TG_TOKEN, parse_mode="HTML")

mongo: dbq.mongo.MongoQueries = None
rds: dbq.red.RedisQueries = None

"""
kb = None
    if post["buttons"] != []:
        kb = types.InlineKeyboardMarkup()
        for i in post["buttons"]:
            row_btns = (types.InlineKeyboardButton(j["text"], url=j["link"] if ("." in j["link"]) else "google.com") for j in i)
            kb.row(*row_btns)
"""


async def send_post(*, tg_id: int | str, post: dict):
    _channel = await mongo.get_chanel_by_tg_id(tg_id=tg_id)
    ref = _channel.get("ref")
    text = post["post_text"].replace("{}", ref or "")
    image = await utils.utls.get_img(post["img_name"])
    new_data = image.replace('data:image/jpeg;base64,', '')
    filename = 'some_image.jpeg'
    if image.startswith('data:image/png;base64,'):
        new_data = image.replace('data:image/png;base64,', '')
        filename = 'some_image.png'
    imgdata = base64.b64decode(new_data)
    with open(filename, 'wb') as f:
        f.write(imgdata)
    kb: None | types.InlineKeyboardMarkup = await utils.utls.get_keyboard(post["buttons"], ref)
    if tg_id.isdigit():
        tg_id = int("-100" + str(tg_id))
    with open(filename, "rb") as f:
        await bot.send_photo(chat_id=tg_id, photo=f.read(), caption=text, reply_markup=kb)


@router.post("/send_post")
async def send_post_to_channel(
        data_sc: models.post.PostSchema = Body(...),
):
    await bot.send_message(chat_id="qwdjqwjdlwjdl", text="test")
    errors = []
    for i in data_sc.tg_id:
        print(data_sc)
        post = await mongo.get_post_by_id(data_sc.post_id)
        try:
            await send_post(tg_id=i, post=post)
        except BaseException as e:
            errors.append({"tg_id": i, "error": e})
    if len(errors) == 0:
        return Response(None, status_code=status.HTTP_200_OK)
    return Response(content=str({"errors": errors}), status_code=status.HTTP_200_OK)


@router.get("/complete_task_by_id/{_id}")
async def complete_task_by_id(_id):
    ...

@router.post("/create_tasks")
async def create_new_task(data_sc: models.post.Calendar = Body(...)):
    var = await mongo.create_task(post_id=data_sc.post_id, channels_id=data_sc.channels_id, dates=data_sc.times)
    for i in var:
        secs = await utils.utls.get_seconds(i["exp"]["date"], i["exp"]["time"])
        print(secs)
        await rds.add_timer(i["_id"], secs)
    # print(var)
    ...


@router.post("/create")
async def create_new_post(data_sc: models.post.NewPostSchema = Body(...)):
    img_name = await save_img(data_sc.img)
    _id = await mongo.save_post(post_name=data_sc.post_name,
                                img_name=img_name,
                                post_text=data_sc.post_text,
                                buttons=data_sc.buttons)
    return _id


@router.post("/add_chanels")
async def add_chanels(data_sc: models.post.Channels = Body(...)):
    print(data_sc)
    try:
        var = await mongo.modify_channels(delete=data_sc.delete, add=data_sc.add, modify=data_sc.modify)
        if var == -1:
            return Response(content="ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if var == -2:
            return Response("Названия каналов должны быть уникальны", status_code=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(None, status_code=status.HTTP_200_OK)


@router.get("/get_chanels")
async def get_chanels():
    var = await mongo.list_channels()
    return var


@router.patch("/edit")
async def edit():
    ...


@router.get("/posts")
async def get_posts():
    var = await mongo.list_posts()
    return var


@router.get("/get_post/{_id}")
async def get_post(_id: str):
    post = await mongo.get_post_by_id(_id)
    return post


@router.get("/get_img/{_id}")
async def get_img(_id: str):
    img = await utils.utls.get_img(_id)
    return img


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # save the uploaded image
    file_name = file.filename
    file_path = os.path.join("imageses", file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"file_name": file_name}

async def start_bot():
    # await bot.send_message(-1001827662376, """<b>qwe</b> <i>qwe</i> <s>qwe</s> <u>qwe</u> <a href='vk.com'>вк</a>""", )

    pass
