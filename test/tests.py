import re
from time import time

from transformers import T5Tokenizer, T5ForConditionalGeneration
from src.text_scraping import PyMuPdfCleaner
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


def question_generator_test():
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

    cleaner = PyMuPdfCleaner("../test/attention-is-all-you-need.pdf")
    blocks = cleaner.extract_text_blocks()
    cleaner.close_document()

    instruction = "Generate a generic question that can be answered using the following text:\n\n"
    start = time()
    for block in blocks[:50]:
        input_text = instruction + block
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids

        outputs = model.generate(input_ids, max_new_tokens=1000)
        print(tokenizer.decode(outputs[0], skip_special_tokens=True))
    print(f"Elapsed time: {time() - start} seconds")


def create_collection_test():
    client = QdrantClient(":memory:")

    client.create_collection(
        collection_name="test",
        vectors_config=VectorParams(size=300, distance=Distance.COSINE))
    try:
        client.create_collection(
            collection_name="test",
            vectors_config=VectorParams(size=300, distance=Distance.COSINE))
    except ValueError:
        print("Collection already exists")


def get_refresh_token():
    authorization = "Authorization: Bearer asd123"
    refresh_token = re.search(r'Bearer\s+(\S+)', authorization).group(1)
    print(refresh_token)


get_refresh_token()
