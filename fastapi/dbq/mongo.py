import hashlib
import time

import motor.motor_asyncio

import cfg


class MongoQueries:
    db: motor.motor_asyncio.AsyncIOMotorClient

    async def run(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(cfg.mongodb_link)
        self.db = client.data

    async def save_post(self, post_name, img_name, post_text, buttons):
        tmp = (img_name + str(time.time())).encode()
        _id = hashlib.md5(tmp).hexdigest()
        base = {
            "_id": _id,
            "post_name": post_name,
            "img_name": img_name,
            "post_text": post_text,
            "buttons": buttons
        }
        var = await self.db["posts"].insert_one(base)
        return var.inserted_id
        ...

    async def get_post_by_id(self, _id):
        var = await self.db["posts"].find_one({"_id": _id})
        return var
        ...

    async def get_post_by_name(self, _id):
        ...

    async def list_posts(self, offset: int = 0):
        var = await self.db["posts"].find({}, {"_id":1, "post_name":1}).to_list(offset+100)
        print(var)
        return var
        ...