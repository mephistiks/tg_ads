from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

import cfg
import models.post


router = APIRouter()

bot = Bot(token=cfg.TG_TOKEN, parse_mode="HTML")



@router.post("/send_post")
async def send_post_to_channel(data_sc: models.post.PostSchema = Body(...)):
    data = jsonable_encoder(data_sc)
    print(data)
    await bot.send_message(data["chanel_id"], data["post"])
    pass

async def start_bot():
    #await bot.send_message(-1001827662376, """<b>qwe</b> <i>qwe</i> <s>qwe</s> <u>qwe</u> <a href='vk.com'>вк</a>""", )
    pass



