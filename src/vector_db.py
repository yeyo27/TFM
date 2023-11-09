from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class VectorDB:
    def __init__(self):
        self.client = QdrantClient(":memory:")

    def create_or_replace_collection(self, name: str, size=300):
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(size=300, distance=Distance.COSINE),
        )

    def insert_into(self, name: str, lines_vectors: list):
        self.client.upsert(
            collection_name="faq_covid",
            points=[
                PointStruct(
                    id=idx,
                    vector=row["encoded"],
                    payload={"answer": row["answer"]}
                )
                for idx, row in df.iterrows()
            ]
        )
