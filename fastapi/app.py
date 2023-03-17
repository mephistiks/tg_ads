import dbq.mongo
import dbq.red
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from routers import pages, api

app = FastAPI(
    middleware=[Middleware(CORSMiddleware, allow_origins=["*"])]
)

app.include_router(pages.router)
app.include_router(api.router, prefix="/api")
app.mount("/static",
          StaticFiles(directory="static"),
          name="static")

app.mount("/images",
          StaticFiles(directory="images"),
          name="images")

app.mount("/api", api.router, name="api")


@app.on_event("startup")
async def start():
    try:
        await api.start_bot()
        mongo = dbq.mongo.MongoQueries()
        await mongo.run()
        api.mongo = mongo
        rds = dbq.red.RedisQueries()
        await rds.run()
        api.rds = rds
    except BaseException as e:
        print(e)
