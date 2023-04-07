import hashlib
import json
import base64
import time

from aiogram import Bot, types
from fastapi import APIRouter, Request, status, Response, Body
from starlette.responses import FileResponse

import cfg
import models.post
import utils.utls
from utils.utls import save_img
import dbq

router = APIRouter()

bot = Bot(token=cfg.TG_TOKEN, parse_mode="HTML")

mongo: dbq.mongo.MongoQueries = None
rds: dbq.red.RedisQueries = None


async def send_post(*, tg: str | int, post_id: str, id_type: str = "tg"):
    match id_type:
        case "tg":
            print(1)
            _channel = await mongo.get_channel_by_tg_id(tg_id=tg)
        case "_id":
            _channel = await mongo.get_channel_by_id(_id=tg)
        case "name":
            _channel = await mongo.get_channel_by_name(name=tg)
        case _:
            raise Exception("channel id type error")
    post = await mongo.get_post_by_id(post_id)
    print(_channel)
    tg_id = _channel.get("tg_id")
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
    if str(tg_id).isdigit():
        tg_id = int("-100" + str(tg_id))
    with open(filename, "rb") as f:
        await bot.send_photo(chat_id=tg_id, photo=f.read(), caption=text, reply_markup=kb)


@router.post("/send_post")
async def send_post_to_channel_handler(
        data_sc: models.post.PostSchema = Body(...),
):
    post_id = data_sc.post_id
    channel_id = data_sc.channel_id
    id_type = data_sc.id_type
    await send_post(tg=channel_id, post_id=post_id, id_type=id_type)


@router.get("/start_task_by_id/{_id}")
async def start_task_by_id(_id):
    task = await mongo.get_task(_id)
    for i in task["channels_id"]:
        try:
            await send_post(tg=i, post_id=task["post_id"], id_type="name")
        except BaseException as e:
            print(e)
    return Response(None, status_code=status.HTTP_200_OK)


@router.post("/create_tasks")
async def create_new_task(data_sc: models.post.Calendar = Body(...)):
    var = await mongo.create_task(post_id=data_sc.post_id, channels_id=data_sc.channels_id, dates=data_sc.times)
    for i in var:
        secs = await utils.utls.get_seconds(i["exp"]["date"], i["exp"]["time"])
        print(secs)
        await rds.add_timer(i["_id"], secs)


@router.post("/create")
async def create_new_post(data_sc: models.post.NewPostSchema = Body(...)):
    img_name = await save_img(data_sc.img)
    _id = await mongo.save_post_with_image(post_name=data_sc.post_name,
                                img_name=img_name,
                                post_text=data_sc.post_text,
                                buttons=data_sc.buttons)
    return _id


@router.post("/add_chanels")
async def add_chanels(data_sc: models.post.Channels = Body(...)):
    print(data_sc)
    try:
        var = await mongo.modify_channels(delete=data_sc.delete, add=data_sc.add)
        if var == -1:
            return Response(content="ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if var == -2:
            return Response("Названия каналов должны быть уникальны", status_code=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("ERROR", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(None, status_code=status.HTTP_200_OK)


@router.get("/get_channels")
async def get_chanels():
    var = await mongo.list_channels()
    return var


@router.get("/get_channels_array")
async def get_chanels_array():
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
    print(_id)
    return post


@router.get("/get_img/{_id}")
async def get_img(_id: str):
    img = await utils.utls.get_img(_id)
    return img


@router.get("/download")
async def download_file(file_path: str):

    return FileResponse(file_path, media_type="application/octet-stream", filename=file_path.split("/")[-1])


async def start_bot():
    # await bot.send_message(-1001827662376, """<b>qwe</b> <i>qwe</i> <s>qwe</s> <u>qwe</u> <a href='vk.com'>вк</a>""", )

    pass
