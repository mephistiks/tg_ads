from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

import cfg
from routers import pages, api
from aiogram import Dispatcher, Bot, executor
app = FastAPI()

app.include_router(pages.router)
app.include_router(api.router, prefix="/api")
app.mount("/static",
          StaticFiles(directory="static"),
          name="static")

@app.on_event("startup")
async def start():
    try:
        await api.start_bot()
    except BaseException as e:
        print(e)