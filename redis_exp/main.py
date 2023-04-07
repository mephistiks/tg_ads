import redis
import time
import requests

#debug = 1, prod = 0
type = 0
if type:
    host_name = "http://127.0.0.1:9898"
else:
    host_name = "http://fastapi:8000"

api_part = "api/v2/start_task_by_id"


print("reids exp started")
r = redis.StrictRedis("redis", 6379)
pubsub = r.pubsub()
#pubsub.subscribe("__keyevent@0__:expired")
pubsub.subscribe("__keyevent@0__:expired")
for msg in pubsub.listen():
    #print(time.time(), msg)
    #print(msg['data'])
    try:
        a = requests.get(f"{host_name}/{api_part}/{msg['data'].decode()}")
    except BaseException as e:
        print(e)
