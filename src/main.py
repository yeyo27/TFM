from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from src.text_scraping import HtmlCleaner, PyMuPdfCleaner, get_readable_html
from src.embeddings_calculator import EmbeddingsCalculator
from src.vector_db import VectorDB
from urllib.parse import unquote


class ArticleUrl(BaseModel):
    href: HttpUrl
    origin: HttpUrl
    hostname: str
    pathname: str


class HealthCheckResponse(BaseModel):
    status: str


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
async def submit_article(article_url: ArticleUrl):
    """
    :param article_url: the url of the article with some info about the domain
    :return dict: contains url info, the collection_id in the vector database and the number of vectors
    """

    readable_html = get_readable_html(article_url.href)

    cleaner = HtmlCleaner(readable_html)
    lines = cleaner.extract_text_lines()

    embeddings = calculator.get_text_embeddings_pairs(lines)

    collection_id = str(hash(article_url.href))
    await database.create_or_replace_collection(collection_id)
    await database.insert_into(collection_id, embeddings)

    return {"url": article_url.href,
            "collection_id": collection_id,
            "number_of_vectors": len(embeddings)}


@app.post("/api/v1/pdf")
async def submit_pdf(pdf: UploadFile = File(...)):
    """
    :param pdf:
    :return dict: contains the url and the number of vectors
    """
    bytes_content = pdf.file.read()
    collection_id = str(hash(pdf.filename))
    cleaner = PyMuPdfCleaner(mem_file=bytes_content)
    blocks = cleaner.extract_text_blocks()

    embeddings = calculator.get_text_embeddings_pairs(blocks)

    await database.create_or_replace_collection(collection_id)
    await database.insert_into(collection_id, embeddings)

    pdf.file.close()
    cleaner.close_document()

    return {"file_name": pdf.filename,
            "collection_id": collection_id,
            "number_of_vectors": len(embeddings)}


@app.get("/api/v1/query")
async def query_collection(collection_id: str, query: str):
    decoded_id = unquote(collection_id).strip()
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
