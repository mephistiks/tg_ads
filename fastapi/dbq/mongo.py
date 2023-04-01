import hashlib
import time

import motor.motor_asyncio
import pymongo.errors

import cfg


class MongoQueries:
    db: motor.motor_asyncio.AsyncIOMotorClient

    async def run(self) -> None:
        client = motor.motor_asyncio.AsyncIOMotorClient(cfg.mongodb_link)
        self.db = client.data

        # try:
        #    self.db["test"]

        try:
            await self.db["test"].insert_one({"_id":1})
        except pymongo.errors.DuplicateKeyError:
            print("OK")
        except pymongo.errors.ConnectionFailure as e:
            raise e
        except BaseException as e:
            raise e


    async def stop(self) -> None:
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

    async def get_post_by_name(self, name) -> dict:
        var = await self.db["posts"].find_one({"post_name": name})
        return var

    async def list_posts(self, offset: int = 0) -> list:
        var = await self.db["posts"].find({}, {"_id": 1, "post_name": 1}).to_list(offset + 100)
        return var

    async def list_channels(self) -> list:
        var = await self.db["channels"].find({}, {"name": 1, "_id": 0}).to_list(200)
        response = [i["name"] for i in var]
        return response

    async def get_channel_by_tg_id(self, *, tg_id) -> dict:
        var = await self.db["channels"].find_one({"tg_id": tg_id})
        return var

    async def get_channel_by_name(self, *, name) -> dict:
        var = await self.db["channels"].find_one({"name": name})
        return var

    async def get_channel_by_id(self, *, _id) -> dict:
        var = await self.db["channels"].find_one({"_id": _id})
        return var

    async def modify_channels(self, *, delete: list, add: list, modify: list) -> int:
        channels: list = [i["name"] for i in await self.list_channels()]
        channels.extend([i["name"] for i in add])
        if len(channels) != len(set(channels)):
            return -2
        for i in delete:
            try:
                await self.db["channels"].delete_one({"_id": i})
            except:
                return -1
        for i in add:
            _id = hashlib.md5(str(i).encode()).hexdigest()
            base = {
                "_id": _id,
                "name": i["name"],
                "tg_id": i["tg_id"],
                "ref": i["ref"]
            }
            try:
                await self.db["channels"].insert_one(base)
            except:
                return -1
        for i in modify:
            print(i)
        return 0


    async def update_channels(self, *, delete: list, add: list, modify: list) :
        errors = {"exists": []}
        for item in delete:
            result = await self.db["channels"].delete_one({"_id": item["_id"]})
            if not result.deleted_count:
                print(f"Did not delete item {item['_id']} - not found")

        for item in add:
            name = item["name"]
            existing = await self.db["channels"].find_one({"name": name})
            # добавить _id
            await self.db["channels"].insert_one(item)

        for item in modify:
            tg_id = item["tg_id"]
            result = await self.db["channels"].update_one({"tg_id": tg_id}, {"$set": item})

        return errors


    async def create_task(self, *, post_id, channels_id: list, dates: list) -> list:
        name = hashlib.md5((str(post_id) + str(channels_id) + str(dates)).encode()).hexdigest()
        base = {
            "_id": name,
            "post_id": post_id,
            "channels_id": channels_id,
            "dates": dates
        }
        q = await self.db["tasks"].insert_one(base)
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
        return response


    async def get_task_id(self, _id):
        var = await self.db["redis"].find_one({"_id": _id})
        return var

    async def get_task_by_id(self, _id):
        print(_id)
        var = await self.db["tasks"].find_one({"_id": _id})
        return var


    async def get_task(self, _id):
        var = await self.db["redis"].find_one({"_id":_id})
        task_id = var["task_id"]
        var2 = await self.db["tasks"].find_one({"_id": task_id})
        return var2


