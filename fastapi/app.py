import dbq.mongo
import dbq.red
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import pages
from routers import v1 as api_v1

app = FastAPI(
    middleware=[Middleware(CORSMiddleware, allow_origins=["*"])]
)

app.include_router(pages.router)
app.include_router(api_v1.router, prefix="/api")
app.mount("/static",
          StaticFiles(directory="static"),
          name="static")

app.mount("/images",
          StaticFiles(directory="images"),
          name="images")


@app.on_event("startup")
async def start(*args):
    try:
        await api_v1.start_bot()
        mongo = dbq.mongo.MongoQueries()
        await mongo.run()
        api_v1.mongo = mongo
        rds = dbq.red.RedisQueries()
        await rds.run()
        api_v1.rds = rds
    except BaseException as e:
        print(e)
