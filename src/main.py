import re
from datetime import datetime, timedelta
from os import getenv
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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
ACCESS_TOKEN_SECRET_KEY = getenv("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = getenv("REFRESH_TOKEN_SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
        "created_at": datetime.utcnow(),
    },
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$yF8xd7gjmZfec4Z/wKYbXudFo0EVeqAJ5xPSzKXJdTRYi2rIVaoEq",  # secret2
        "created_at": datetime.utcnow(),
    },
    "johndoe@example.com": "johndoe",
    "alice@example.com": "alice",
}

fake_history_db = {
    "johndoe":
        [
            {
                'id': 1,
                'sourceName': 'url1.com',
                'date': '2022-01-01 12:00:00',
                'query': 'What is the weather like?',
                'response': 'The weather is sunny',
            },
            {
                'id': 2,
                'sourceName': 'url2.com',
                'date': '2031-01-01 12:00:00',
                'query': 'What is the weather like?',
                'response': 'The weather is nothing',
            },
            {
                'id': 4,
                'username': 'johndoe',
                'sourceName': 'pdf1',
                'date': '2022-01-01 12:00:00',
                'query': 'What is the weather like?',
                'response': 'The weather is sunny',
            },
        ],
    "alice":
        [
            {
                'id': 3,
                'username': 'alice',
                'sourceName': 'url3.com',
                'date': '2022-01-01 12:00:00',
                'query': 'What is the sñkfñodfksd like?',
                'response': 'The weather is skejfoiw',
            },
            {
                'id': 5,
                'username': 'alice',
                'sourceName': 'pdf3',
                'date': '2022-01-01 12:00:00',
                'query': 'What is the weather like?',
                'response': 'The weather is sunny',
            }
        ],
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenRefresh(Token):
    refresh_token: str


class TokenData(BaseModel):
    username: str | None = None


class NewUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class User(BaseModel):
    username: str
    email: EmailStr


class UserInDb(User):
    hashed_password: str
    created_at: datetime


class ArticleUrl(BaseModel):
    href: HttpUrl
    origin: HttpUrl
    hostname: str
    pathname: str


class HealthCheckResponse(BaseModel):
    status: str


calculator = EmbeddingsCalculator()

database = VectorDB()

generator = QuestionGeneratorTransformers()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/token")

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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDb(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if not user:
        raise credentials_exception
    return user


def refresh_current_user(x_authorization: Annotated[str, Header()]):
    """
    Get the refresh token from the request headers.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not x_authorization:
        raise credentials_exception
    try:
        refresh_token = re.search(r'Bearer\s+(\S+)', x_authorization).group(1)
    except AttributeError:
        raise credentials_exception

    try:
        payload = jwt.decode(refresh_token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        # I do not know if expiry time is necessary to check
        expiry_time = payload.get("exp")
        if datetime.utcfromtimestamp(expiry_time) < datetime.utcnow():
            raise credentials_exception
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if not user:
        raise credentials_exception
    return user


def insert_user_to_fake_db(user_data: NewUser):
    # store credentials in db
    fake_users_db[user_data.username] = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password),
        "created_at": datetime.utcnow(),
    }
    fake_users_db[user_data.email] = user_data.username
    return fake_users_db[user_data.username]


def get_fake_history(username):
    return fake_history_db[username]


@app.get("/")
async def root():
    """
    A function that serves as the root endpoint for the API.

    Returns:
        dict: A dictionary with a single key-value pair containing the message of the API.
    """
    return {"message": "TFM API v1.0"}


@app.post("/api/v1/token", response_model=TokenRefresh)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


@app.post("/api/v1/token/refresh", response_model=Token)
async def refresh(current_user: Annotated[User, Depends(refresh_current_user)]):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": current_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/v1/signup")
async def signup(user_data: NewUser):
    if user_data.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    if user_data.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already exists")
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    # store credentials in db
    new_user = insert_user_to_fake_db(user_data)
    return {"message": "User created successfully", "new_user": new_user}


@app.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@app.get("/api/v1/history")
async def history(current_user: Annotated[User, Depends(get_current_user)]):
    return get_fake_history(current_user.username)


async def store_embeddings(collection_id: str, text_units: list[str]):
    questions = generator.generate_questions(text_units)
    embeddings = calculator.get_questions_embeddings(questions, text_units)
    await database.insert_into(collection_id, embeddings)
    return len(embeddings)


@app.post("/api/v1/url")
async def submit_article(article_url: ArticleUrl, current_user: Annotated[User, Depends(get_current_user)]):
    """
    :param current_user: contains information about the current session
    :param article_url: the url of the article with some info about the domain
    :return dict: contains url info, the collection_id in the vector database and the number of vectors
    """
    # First check if collection already exists to avoid recreating it
    collection_id = str(hash(article_url.href))
    try:
        await database.create_collection(collection_id)
    except ValueError:
        # collection already exists
        return {"url": article_url.href,
                "collection_id": collection_id,
                "total_vectors": await database.count_collection(collection_id)}

    readable_html = get_readable_html(article_url.href)

    cleaner = HtmlCleaner(readable_html)
    lines = cleaner.extract_text_lines()

    total_vectors = await store_embeddings(collection_id, lines)

    return {"url": article_url.href,
            "collection_id": collection_id,
            "total_vectors": total_vectors}


@app.post("/api/v1/pdf")
async def submit_pdf(current_user: Annotated[User, Depends(get_current_user)], pdf: UploadFile = File(...)):
    """
    :param current_user: contains information about the current session
    :param pdf: the pdf file
    :return dict: contains the url and the number of vectors
    """
    # First check if collection already exists to avoid recreating it
    collection_id = str(hash(pdf.filename))
    try:
        await database.create_collection(collection_id)
    except ValueError:
        # collection already exists
        return {"file_name": pdf.filename,
                "collection_id": collection_id,
                "total_vectors": await database.count_collection(collection_id)}

    bytes_content = pdf.file.read()

    cleaner = PyMuPdfCleaner(mem_file=bytes_content)
    blocks = cleaner.extract_text_blocks()

    total_vectors = await store_embeddings(collection_id, blocks)

    pdf.file.close()
    cleaner.close_document()

    return {"file_name": pdf.filename,
            "collection_id": collection_id,
            "total_vectors": total_vectors}


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
