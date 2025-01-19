from qdrant_client.http import models
from qdrant_client import QdrantClient
import os

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_config = models.VectorParams(
    size=3072,
    distance=models.Distance.COSINE
)


client.create_collection(
    collection_name="storm_agent",
    vectors_config=collection_config
)