import datetime
import hashlib


async def save_img(img_str: str):
    name = hashlib.md5(img_str.encode()).hexdigest()
    with open(f"images/{name}", "wb") as f:
        f.write(img_str.encode())
    return name


async def get_img(name: str):
    with open(f"images/{name}", "rb") as f:
        resp = f.read()
    return resp.decode()

async def get_seconds(date:str, time:str):
    s = date + "-" + time
    s = s.replace(":", "-")
    z = list(map(int, s.split("-")))
    resp = (datetime.datetime(*z) - datetime.datetime.now()).seconds
    return resp
