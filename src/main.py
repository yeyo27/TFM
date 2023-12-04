from fastapi import FastAPI, Request, Form, HTTPException, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from src.scraper import HtmlCleaner
from src.embeddings_calculator import EmbeddingsCalculator
from src.vector_db import VectorDB
from urllib.parse import unquote


class ReadableHTML(BaseModel):
    url: HttpUrl
    encoded_html: str
    probably_readable: bool


class HealthCheckResponse(BaseModel):
    status: str


app = FastAPI()

calculator = EmbeddingsCalculator()

database = VectorDB()


@app.get("/")
async def root():
    """
    A function that serves as the root endpoint for the API.

    Returns:
        dict: A dictionary with a single key-value pair containing the message of the API.
    """
    return {"message": "TFM API v1.0"}


@app.post("/api/v1/url")
async def submit_article(readable_html: ReadableHTML):
    """
    :param readable_html:
    :return dict: contains the url and the number of vectors
    """
    decoded_html = unquote(readable_html.encoded_html)
    cleaner = HtmlCleaner(decoded_html)
    clean_text = cleaner.get_text_from_html()

    embeddings = calculator.get_lines_embeddings_pairs(clean_text)

    database.create_or_replace_collection(readable_html.url)
    database.insert_into(readable_html.url, embeddings)

    return {"url": readable_html.url, "number_of_vectors": len(embeddings)}


@app.get("/api/v1/url", response_class=HTMLResponse)
async def query_article():
    return ""


@app.get("/api/v1/healthz", response_model=HealthCheckResponse)
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
