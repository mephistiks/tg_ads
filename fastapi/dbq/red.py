import cfg
import redis


class RedisQueries:
    redis_connection: redis.client.Redis

    async def run(self):
        redis_host = cfg.redis_host
        redis_port = cfg.redis_port
        self.redis_connection = redis.Redis(host=redis_host, port=redis_port)

    async def stop(self):
        print("Redis подключение закрыто")
        self.redis_connection.close()

    async def add_timer(self, _id, exp: int):
        try:
            self.redis_connection.set(_id, 1, ex=exp)
        except BaseException as e:
            print(e)

