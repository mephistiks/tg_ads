import json
import base64
from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from fastapi import APIRouter, Request, status, Response, Body
from fastapi.encoders import jsonable_encoder

import cfg
import models.post
import utils.utls
from utils.utls import save_img
import dbq

router = APIRouter()

bot = Bot(token=cfg.TG_TOKEN, parse_mode="HTML")

mongo: dbq.mongo.MongoQueries = None


@router.get("/")
async def index_ok():
    return Response("ok", status_code=status.HTTP_200_OK)


@router.post("/send_post")
async def send_post_to_channel(
        data_sc: models.post.PostSchema = Body(...),
):
    # data = jsonable_encoder(data_sc)
    post = await mongo.get_post_by_id(data_sc.post_id)

    kb = types.InlineKeyboardMarkup()
    for i in post["buttons"]:
        row_btns = (types.InlineKeyboardButton(j["text"], url=j["link"] if ("." in j["link"]) else "google.com") for j in i)
        kb.row(*row_btns)

    data = await utils.utls.get_img(post["img_name"])
    #await bot.send_photo(chat_id=data_sc.chanel_id, photo=data.replace('data:image/jpeg;base64,', '').replace('data:image/png;base64,', ''), caption=post["post_text"], reply_markup=kb)
    if data.startswith('data:image/jpeg;base64,'):
        new_data = data.replace('data:image/jpeg;base64,', '')
        imgdata = base64.b64decode(new_data)
        filename = 'some_image.jpeg'
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print(kb)

        #for j in i
        with open(filename, "rb") as f:
            await bot.send_photo(chat_id=data_sc.chanel_id, photo=f.read(), caption=post["post_text"], reply_markup=kb)
    if data.startswith('data:image/png;base64,'):
        new_data = data.replace('data:image/png;base64,', '')
        imgdata = base64.b64decode(new_data)
        filename = 'some_image.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)
        print(kb)

        # for j in i
        with open(filename, "rb") as f:
            await bot.send_photo(chat_id=data_sc.chanel_id, photo=f.read(), caption=post["post_text"], reply_markup=kb)
    return "ok"
    pass


@router.post("/create")
async def create_new_post(data_sc: models.post.NewPostSchema = Body(...)):
    data = jsonable_encoder(data_sc)
    img_name = await save_img(data_sc.img)
    _id = await mongo.save_post(post_name=data_sc.post_name,
                          img_name=img_name,
                          post_text=data_sc.post_text,
                          buttons=data_sc.buttons)
    print(_id)
    return _id

@router.patch("/edit")
async def edit():
    ...


@router.get("/posts")
async def get_posts():
    var = await mongo.list_posts()
    return var


@router.get("/get_post/{_id}")
async def get_post(_id:str):
    post = await mongo.get_post_by_id(_id)
    print(_id)
    return post

@router.get("/get_img/{_id}")
async def get_img(_id:str):
    img = await utils.utls.get_img(_id)
    print(img)
    return img


async def start_bot():
    # await bot.send_message(-1001827662376, """<b>qwe</b> <i>qwe</i> <s>qwe</s> <u>qwe</u> <a href='vk.com'>вк</a>""", )
    pass
