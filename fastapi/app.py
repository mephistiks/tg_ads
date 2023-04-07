import dbq.mongo
import dbq.red
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import pages
from routers import v1
from routers.v2 import v2

app = FastAPI(
    middleware=[Middleware(CORSMiddleware, allow_origins=["*"])]
)

app.include_router(pages.router)
app.include_router(v1.router, prefix="/api")
app.include_router(v2.router, prefix="/api/v2")
app.mount("/static",
          StaticFiles(directory="static"),
          name="static")

app.mount("/images",
          StaticFiles(directory="images"),
          name="images")

app.mount("/files",
          StaticFiles(directory="files"),
          name="files")

@app.on_event("startup")
async def start():
    try:
        #await v1.start_bot()
        mongo = dbq.mongo.MongoQueries()
        await mongo.run()
        v1.mongo = mongo
        v2.mongo = mongo
        rds = dbq.red.RedisQueries()
        await rds.run()
        v1.rds = rds
        v2.rds = rds
    except BaseException as e:
        print(e)
