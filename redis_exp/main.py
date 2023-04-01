import redis
import time
import requests

#debug = 1, prod = 0
type = 0
if type:
    base_link = "http://127.0.0.1:9898/api/start_task_by_id"
else:
    base_link = "http://fastapi:8000/api/start_task_by_id"

print("reids exp started")
r = redis.StrictRedis("redis", 6379)
pubsub = r.pubsub()
#pubsub.subscribe("__keyevent@0__:expired")
pubsub.subscribe("__keyevent@0__:expired")
for msg in pubsub.listen():
    #print(time.time(), msg)
    #print(msg['data'])
    try:
        a = requests.get(f"{base_link}/{msg['data'].decode()}")
    except BaseException as e:
        print(e)
