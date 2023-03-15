import redis
import time
import requests

print("reids exp started")
r = redis.StrictRedis("redis", 6379)
pubsub = r.pubsub()
pubsub.subscribe("__keyevent@0__:expired")
for msg in pubsub.listen():
    print(msg['data'])
    try:
        a = requests.get(f"http://fastapi:8000/api/send_post/{msg['data'].decode()}")
    except BaseException as e:
        print(e)
