from datetime import datetime
from os import getenv
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, HttpUrl, EmailStr
from src.text_scraping import HtmlCleaner, PyMuPdfCleaner, get_readable_html
from src.embeddings_calculator import EmbeddingsCalculator
from src.question_generator import QuestionGeneratorTransformers
from src.vector_db import VectorDB
from urllib.parse import unquote
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path("../.env"))
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "hashed_password": "fakehashedsecret2",
    },
}


class NewUser(BaseModel):
    email: EmailStr
    name: str
    password: str
    confirm_password: str


class User(BaseModel):
    username: str
    email: EmailStr
    name: str


class ArticleUrl(BaseModel):
    href: HttpUrl
    origin: HttpUrl
    hostname: str
    pathname: str


class HealthCheckResponse(BaseModel):
    status: str


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

generator = QuestionGeneratorTransformers()


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/")
async def root():
    """
    A function that serves as the root endpoint for the API.

    Returns:
        dict: A dictionary with a single key-value pair containing the message of the API.
    """
    return {"message": "TFM API v1.0"}


@app.post("/api/v1/login")
async def login(credentials: User):
    user_exists = True
    if not user_exists:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "User logged in", "credentials": credentials}


@app.post("/api/v1/signup")
async def signup(user_data: NewUser):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    # store credentials in db
    new_user = {
        "email": user_data.email,
        "name": user_data.name,
        "password": user_data.password,  # maybe hash it
        "created_at": datetime.now(),
    }
    return {"message": "User created successfully", "new_user": new_user}


@app.get("/api/v1/history")
def history(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.post("/api/v1/url")
async def submit_article(article_url: ArticleUrl):
    """
    :param article_url: the url of the article with some info about the domain
    :return dict: contains url info, the collection_id in the vector database and the number of vectors
    """

    readable_html = get_readable_html(article_url.href)

    cleaner = HtmlCleaner(readable_html)
    lines = cleaner.extract_text_lines()

    questions = generator.generate_questions(lines)
    embeddings = calculator.get_questions_embeddings(questions, lines)

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
    questions = generator.generate_questions(blocks)
    embeddings = calculator.get_questions_embeddings(questions, blocks)

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
