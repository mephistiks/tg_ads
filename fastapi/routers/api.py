import json

from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from fastapi import APIRouter, Request, status, Response, Body
from fastapi.encoders import jsonable_encoder

import cfg
import models.post
from utils.utls import save_img
import dbq

router = APIRouter()

bot = Bot(token=cfg.TG_TOKEN, parse_mode="HTML")

mongo: dbq.mongo.MongoQueries = None


@router.get("/")
async def index_ok():
    return Response("ok", status_code=status.HTTP_200_OK)


@router.get("/send_post/{_id}")
async def send_post_to_channel(
        #        data_sc: models.post.PostSchema = Body(...)
        _id: str
):
    # data = jsonable_encoder(data_sc)
    print(_id)
    # await bot.send_message(data["chanel_id"], data["post"])
    return "ok"
    pass


@router.post("/create")
async def create_new_post(data_sc: models.post.NewPostSchema = Body(...)):
    data = jsonable_encoder(data_sc)
    img_name = await save_img(data_sc.img)
    await mongo.save_post(post_name=data_sc.post_name,
                          img_name=img_name,
                          post_text=data_sc.post_text,
                          buttons=data_sc.buttons)

    # await bot.send_message(data["chanel_id"], data["post"])
    # return {"message": "ok", "status_code": status.HTTP_200_OK}
    # message = json.dumps({
    #    "message": "ok",
    #    "2 kozla": "skolko?"
    # })
    # return Response(
    #    message,
    #    status_code=status.HTTP_200_OK
    # )
    # pass


@router.patch("/edit")
async def edit():
    ...


@router.get("/posts")
async def get_posts():
    posts = [
        {"name1": "http://link1.com"},
        {"name2": "http://link2.com"}
    ]
    return posts


"""
        async function get_p(event) {
            let response = await fetch('http://127.0.0.1:8000/api/posts', {
                headers: {
                    'accept': 'application/json'
                }
            });
            let result = await response.text;
            var posts = document.getElementById('posts')
            var post = document.createElement('li')
            var content = document.createTextNode(result)
            post.appendChild(content)
            posts.appendChild(post)
        }
"""


async def start_bot():
    # await bot.send_message(-1001827662376, """<b>qwe</b> <i>qwe</i> <s>qwe</s> <u>qwe</u> <a href='vk.com'>вк</a>""", )
    pass
