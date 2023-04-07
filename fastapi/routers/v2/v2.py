import hashlib
import time

from fastapi import APIRouter, status, Response, Body, UploadFile, File
from .models import NewPostSchema, PostSchema
from .utls import pre_send_post
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
    post = await mongo.get_post_by_id(post_id)
    tg_data = await mongo.get_channel_by_name(name=data_sc.channel_id)
    await pre_send_post(tg_data=tg_data, post=post)


@router.get("/start_task_by_id/{_id}")
async def start_task_by_id(_id):
    task = await mongo.get_task(_id)
    post = await mongo.get_post_by_id(task["post_id"])
    for i in task["channels_id"]:
        tg_data = await mongo.get_channel_by_name(name=i)
        await pre_send_post(tg_data=tg_data, post=post)
    return Response(None, status_code=status.HTTP_200_OK)