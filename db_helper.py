from qdrant_client.http import models
from qdrant_client import QdrantClient
import streamlit as st

client = QdrantClient(
    url=st.secrets["QDRANT_URL"],
    api_key=st.secrets["QDRANT_API_KEY"]
)

collection_config = models.VectorParams(
    size=384,
    distance=models.Distance.COSINE
)


client.create_collection(
    collection_name="storm_agent",
    vectors_config=collection_config
)
