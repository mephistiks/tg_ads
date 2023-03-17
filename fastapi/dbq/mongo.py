import hashlib
import time

import motor.motor_asyncio

import cfg


class MongoQueries:
    db: motor.motor_asyncio.AsyncIOMotorClient

    async def run(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(cfg.mongodb_link)
        self.db = client.data

    async def stop(self):
        ...

    async def save_post(self, post_name, img_name, post_text, buttons) -> str:
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

    async def get_post_by_id(self, _id) -> dict:
        var = await self.db["posts"].find_one({"_id": _id})
        return var

    async def get_post_by_name(self, _id):
        ...

    async def list_posts(self, offset: int = 0) -> list:
        var = await self.db["posts"].find({}, {"_id": 1, "post_name": 1}).to_list(offset + 100)
        print(var)
        return var
        ...

    async def list_channels(self) -> list:
        var = await self.db["channels"].find({}, {"name": 1, "_id": 0}).to_list(200)
        return var

    async def modify_channels(self, *, delete: list, add: list):
        channels: list = [i["name"] for i in await self.list_channels()]
        channels.extend([i["name"] for i in add])
        if len(channels) != len(set(channels)):
            return -2
        for i in add:
            base = {
                "_id": i["id"],
                "name": i["name"]
            }
            try:
                await self.db["channels"].insert_one(base)
            except:
                return -1
        for i in delete:
            try:
                await self.db["channels"].delete_one({"name": i})
            except:
                return -1
        return 0

    async def create_task(self, *, post_id, channels_id: list, dates: list):
        print(post_id, channels_id, dates)
        name = hashlib.md5((str(post_id) + str(channels_id) + str(dates)).encode()).hexdigest()
        print(name)
        base = {
            "_id": name,
            "post_id": post_id,
            "channels_id": channels_id,
            "dates": dates
        }
        print(base)
        q = await self.db["tasks"].insert_one(base)
        print(q)
        response = []
        for i in dates:
            name2 = hashlib.md5((name + str(i)).encode()).hexdigest()
            base2 = {
                "_id": name2,
                "task_id": q.inserted_id
            }
            var = await self.db["redis"].insert_one(base2)
            response.append(
                {
                    "_id": var.inserted_id,
                    "exp": i
                }
            )
            print(var)
        print(response)
        return response
