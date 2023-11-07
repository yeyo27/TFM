from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

import src.scraper

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return "<h1>Hello World</h1>"


@app.post("/api/v1/url")
async def process_url(url: HttpUrl):
    """

    :param url:
    :return:
    """
    return {"url": url, "text": "toDo"}


class HealthCheckResponse(BaseModel):
    status: str


@app.get("/api/v1/healthz", response_model=HealthCheckResponse)
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
