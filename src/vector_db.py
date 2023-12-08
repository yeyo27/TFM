from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, ScoredPoint
import logging
from embeddings_calculator import EmbeddingsCalculator


class VectorDB:
    def __init__(self):
        self.client = QdrantClient(":memory:")

    def create_or_replace_collection(self, name: str, size: int = 300) -> None:
        """
        Create or replace a collection in the QDrant client
        :param name: name of the collection
        :param size: size of the vectors. Depends on the model.
        :return:
        """
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE),
        )

    def insert_into(self, name: str, lines_vectors: list[tuple]):
        """
        Insert into a collection
        :param name: name of a collection
        :param lines_vectors: pairs of lines and their embeddings
        :return:
        """
        self.client.upsert(
            collection_name=name,
            points=[
                PointStruct(
                    id=idx,
                    vector=pair[1],
                    payload={"answer": pair[0]}
                )
                for idx, pair in enumerate(lines_vectors) if all(element != 0.0 for element in pair[1])
            ]
        )

    def search_collection(self, name: str, query_vector: list, limit: int = 5):
        """
        Search in a collection
        :param name: name of a collection
        :param query_vector: embedding of the desired query
        :param limit: number of returned hits
        :return hits: coincidences with the highest similarity
        """
        return self.client.search(collection_name=name,
                                  query_vector=query_vector,
                                  limit=limit)


if __name__ == "__main__":
    """
    model with decent results using our example webpage:
    - paraphrase-multilingual-MiniLM-L12-v2 (size=384, measure > 0.7)
    - average_word_embeddings_komninos (size=300, measure > 0.7)
    - distiluse-base-multilingual-cased-v1 (size=512, measure ~= 0.596)
    """
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Starting vector database...")
    db = VectorDB()
    logging.debug("Database initiated")

    logging.debug("Creating embeddings calculator...")
    emb_calc = EmbeddingsCalculator("average_word_embeddings_komninos")
    logging.debug("Calculator created")

    with open("../test/clean_text_from_api.txt") as f:
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
