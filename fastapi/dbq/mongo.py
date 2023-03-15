import motor.motor_asyncio

import cfg


class MongoQueries:
    db: motor.motor_asyncio.AsyncIOMotorClient

    async def run(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(cfg.mongodb_link)
        self.db = client.data

    async def save_post(self, post_name, img_name, post_text, buttons):
        base = {
            # "_id":
            "post_name": post_name,
            "img_name": img_name,
            "post_text": post_text,
            "buttons": buttons
        }
        await self.db["posts"].insert_one(base)
        ...

    async def get_post_by_id(self, _id):
        ...

    async def get_post_by_name(self, _id):
        ...
