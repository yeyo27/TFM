import asyncio

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import logging
from embeddings_calculator import EmbeddingsCalculator
from src.text_scraping import HtmlCleaner, PyMuPdfCleaner
from src.question_generator import QuestionGeneratorTransformers


class VectorDB:
    def __init__(self):
        self.client = AsyncQdrantClient(":memory:")

    async def create_or_replace_collection(self, name: str, size: int = 300) -> None:
        """
        Create or replace a collection in the QDrant client
        :param name: name of the collection
        :param size: size of the vectors. Depends on the model.
        :return:
        """
        await self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

    async def create_collection(self, name: str, size: int = 300) -> None:
        """
        Create a collection in the QDrant client. If the collection already exists, it will raise a ValueError
        :param name: name of the collection
        :param size: size of the vectors. Depends on the model.
        :return:
        """
        await self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

    async def insert_into(self, name: str, lines_vectors: list[tuple]):
        """
        Insert into a collection
        :param name: name of a collection
        :param lines_vectors: pairs of lines and their embeddings
        :return:
        """
        await self.client.upsert(
            collection_name=name,
            points=[
                PointStruct(
                    id=idx,
                    vector=pair[1],
                    payload={"question": pair[0], "answer": pair[2]}
                )
                for idx, pair in enumerate(lines_vectors) if all(element != 0.0 for element in pair[1])
            ]
        )

    async def search_collection(self, name: str, query_vector: list, limit: int = 3):
        """
        Search in a collection
        :param name: name of a collection
        :param query_vector: embedding of the desired query
        :param limit: number of returned hits
        :return hits: coincidences with the highest similarity
        """
        return await self.client.search(collection_name=name,
                                        query_vector=query_vector,
                                        with_vectors=False,
                                        limit=limit)

    async def count_collection(self, name: str):
        return await self.client.count(collection_name=name)


async def html_test():
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Starting vector database...")
    db = VectorDB()
    logging.debug("Database initiated")

    logging.debug("Creating embeddings calculator...")
    emb_calc = EmbeddingsCalculator("average_word_embeddings_komninos")
    logging.debug("Calculator created")

    logging.debug("Creating questions generator...")
    question_generator = QuestionGeneratorTransformers()
    logging.debug("Generator created")

    with open("../test/readability.html") as f:
        logging.debug("Reading file...")
        html = f.read()
        cleaner = HtmlCleaner(html)
        logging.debug("Extracting text...")
        lines = cleaner.extract_text_lines()

        logging.debug("Generating questions...")
        questions = question_generator.generate_questions(lines)

        logging.debug("Calculating embeddings...")
        embeddings = emb_calc.get_questions_embeddings(questions, lines)

        logging.debug("Creating collection 'test'...")
        await db.create_or_replace_collection("test", 300)

        logging.debug("Inserting embeddings into 'test' collection...")
        await db.insert_into("test", embeddings)
        logging.debug(await db.count_collection("test"))

        logging.debug("Calculating query embeddings...")
        query = "What are the major browsers today?"
        query_embeddings = emb_calc.calculate(query)

        logging.debug("Searching database...")
        hits = await db.search_collection("test", query_embeddings)
        logging.debug(query)
        for hit in hits:
            logging.debug(hit)


async def pdf_test():
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Starting vector database...")
    db = VectorDB()
    logging.debug("Database initiated")

    logging.debug("Creating embeddings calculator...")
    emb_calc = EmbeddingsCalculator("average_word_embeddings_komninos")
    logging.debug("Calculator created")

    logging.debug("Creating questions generator...")
    question_generator = QuestionGeneratorTransformers()
    logging.debug("Generator created")

    logging.debug("Reading file...")
    cleaner = PyMuPdfCleaner("../test/attention-is-all-you-need.pdf")
    blocks = cleaner.extract_text_blocks()
    cleaner.close_document()

    logging.debug("Generating questions...")
    questions = question_generator.generate_questions(blocks)

    logging.debug("Calculating embeddings...")
    embeddings = emb_calc.get_questions_embeddings(questions, blocks)

    logging.debug("Creating collection 'test'...")
    await db.create_or_replace_collection("test", 300)

    logging.debug("Inserting embeddings into 'test' collection...")
    await db.insert_into("test", embeddings)
    logging.debug(await db.client.count(collection_name="test"))

    logging.debug("Calculating query embeddings...")
    query = "What is an attention function?"
    query_embeddings = emb_calc.calculate(query)

    logging.debug("Searching database...")
    hits = await db.search_collection("test", query_embeddings)
    logging.debug(query)
    for hit in hits:
        logging.debug(hit)


if __name__ == "__main__":
    """
    model with decent results using our example webpage:
    - paraphrase-multilingual-MiniLM-L12-v2 (size=384, measure > 0.7)
    - average_word_embeddings_komninos (size=300, measure > 0.7)
    - distiluse-base-multilingual-cased-v1 (size=512, measure ~= 0.596)
    """
    asyncio.run(html_test())
