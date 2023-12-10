from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from src.text_scraping import HtmlCleaner
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
    clean_text = cleaner.extract_text_from_html()

    embeddings = calculator.get_text_embeddings_pairs(clean_text)

    collection_id = str(hash(readable_html.url))
    await database.create_or_replace_collection(collection_id)
    await database.insert_into(collection_id, embeddings)

    return {"url": readable_html.url,
            "collection_id": collection_id,
            "number_of_vectors": len(embeddings),
            "probably_readable": readable_html.probably_readable}


@app.get("/api/v1/url")
async def query_collection(collection_id: str, query: str):
    decoded_id = unquote(collection_id)
    decoded_query = unquote(query)
    query_embeddings = calculator.calculate(decoded_query)
    hits = await database.search_collection(decoded_id, query_embeddings)
    return {"id": decoded_id, "query": decoded_query, "hits": hits}


@app.get("/api/v1/healthz", response_model=HealthCheckResponse)
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8080)
