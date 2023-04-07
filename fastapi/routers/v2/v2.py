import hashlib
import time

from fastapi import APIRouter, Request, status, Response, Body, UploadFile, File
import cfg
from .models import NewPostSchema, PostSchema
from .utls import pre_send_post
import utils.utls
import dbq

router = APIRouter()

mongo: dbq.mongo.MongoQueries = None
rds: dbq.red.RedisQueries = None


@router.post("/create")
async def create_new_post(data_sc: NewPostSchema = Body(...)):
    _id = await mongo.save_post_with_file(post_name=data_sc.post_name,
                                file_name=data_sc.file_name,
                                post_text=data_sc.post_text,
                                buttons=data_sc.buttons)
    return _id


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    name = file.filename
    name_s = name.split(".")
    new_name = hashlib.md5((name + str(time.time())).encode()).hexdigest() + "." + name_s[1]
    with open(f"files/{new_name}", 'wb') as f:
        f.write(contents)
    return new_name


@router.post("/send_post")
async def send_post_to_channel_handler(
        data_sc: PostSchema = Body(...),
):
    post_id = data_sc.post_id
    # match id_type:
    #    case "tg":
    #        print(1)
    #        _channel = await mongo.get_channel_by_tg_id(tg_id=tg)
    #    case "_id":
    #        _channel = await mongo.get_channel_by_id(_id=tg)
    #    case "name":
    #        _channel = await mongo.get_channel_by_name(name=tg)
    #    case _:
    #        raise Exception("channel id type error")
    post = await mongo.get_post_by_id(post_id)
    tg_data = await mongo.get_channel_by_name(name=data_sc.channel_id)
    await pre_send_post(tg_data=tg_data, post=post)
