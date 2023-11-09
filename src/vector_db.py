from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import logging
from embeddings_calculator import EmbeddingsCalculator


class VectorDB:
    def __init__(self):
        self.client = QdrantClient(":memory:")

    def create_or_replace_collection(self, name: str, size: int = 300):
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

    def insert_into(self, name: str, lines_vectors: list[tuple]):
        self.client.upsert(
            collection_name=name,
            points=[
                PointStruct(
                    id=idx,
                    vector=pair[1],
                    payload={"answer": pair[0]}
                )
                for idx, pair in enumerate(lines_vectors)
            ]
        )

    def search_collection(self, name: str, query_vector: list, limit: int = 5):
        hits = self.client.search(collection_name=name,
                                  query_vector=query_vector,
                                  limit=limit)
        return hits


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Starting vector database...")
    db = VectorDB()
    logging.debug("Database initiated")

    logging.debug("Creating embeddings calculator...")
    emb_calc = EmbeddingsCalculator()
    logging.debug("Calculator created")

    with open("../test/example_from_readability.txt") as f:
        logging.debug("Reading file...")
        context = f.read()

        logging.debug("Calculating embeddings...")
        embeddings = emb_calc.get_lines_embeddings_pairs(context)

        logging.debug("Creating collection 'test'...")
        db.create_or_replace_collection("test")

        logging.debug("Inserting embeddings into 'test' collection...")
        db.insert_into("test", embeddings)
        logging.debug(db.client.count(collection_name="test"))

        logging.debug("Calculating query embeddings...")
        query = "What are the major browsers today?"
        query_embeddings = emb_calc.calculate(query)

        logging.debug("Searching database...")
        hits = db.search_collection("test", query_embeddings)
        logging.debug(query)
        for hit in hits:
            logging.debug(hit)
