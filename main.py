import json
import psutil
import os
import asyncio
import html
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Union
from pydantic import BaseModel

from websockets.exceptions import ConnectionClosed

from build_assets import AssetsBuilder


main_file_dir_path = os.path.abspath(os.path.dirname(__file__))
assets_builder = AssetsBuilder(main_file_dir_path)
assets_builder.build()


imports = {"imports": assets_builder.build_js_imports()}

app = FastAPI()
static_files = StaticFiles(directory="static")
app.mount("/static", static_files, name="static")
templates = Jinja2Templates(directory="templates")

print(imports)

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    print("request", dir(request))
    print("url", request.url)
    final_html = templates.TemplateResponse(
        request=request, name="index.html", context={"imports": imports})
    return final_html

async def handle_connection(data):
    return {}

