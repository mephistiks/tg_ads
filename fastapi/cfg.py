import os

TG_TOKEN = ""

img_extensions = ['.jpg', '.jpeg', '.png']
gif_extensions = ['.gif']
video_extensions = ['.mp4', '.mov']
host_url = os.getenv("HOST_URL", "localhost")

#debug = 1, docker = 0
type = os.getenv("DEBUG", True)

if type == True: #debug
    redis_host = "localhost"
    redis_port = 6500
    mongodb_link = "mongodb://mongo:mongo@localhost:27029/"

else:
    redis_host = "redis"
    redis_port = 6379
    mongodb_link = "mongodb://mongo:mongo@mongodb:27017/"

