import pytest
from pydantic import BaseModel, HttpUrl


class Article(BaseModel):
    url: HttpUrl
    text: str

