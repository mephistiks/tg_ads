import os

TG_TOKEN = "5996947797:AAEFjYd2cIhCtvbT3sk7zBCpPRtOmxA68gQ"

#debug = 1, docker = 0
type = os.getenv("DBG", True)

if type == True: #debug
    redis_host = "localhost"
    redis_port = 6500

    mongodb_link = "mongodb://mongo:mongo@localhost:27029/"

else:
    redis_host = "redis"
    redis_port = 6379

    mongodb_link = "mongodb://mongo:mongo@mongodb:27017/"

