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


# from qdrant_client import QdrantClient
# from qdrant_client.http import models
# import os

# client = QdrantClient(
#     url=os.getenv("QDRANT_URL"),
#     api_key=os.getenv("QDRANT_API_KEY")
# )

# # Delete the collection if it exists
# collection_name = "storm_agent"

# # Check if the collection exists
# collections = client.get_collections()
# if any(collection['name'] == collection_name for collection in collections['result']['collections']):
#     print(f"Collection {collection_name} exists. Deleting it...")
#     client.delete_collection(collection_name=collection_name)

# # Now, you can recreate the collection
# collection_config = models.VectorParams(
#     size=384,
#     distance=models.Distance.COSINE
# )

# client.create_collection(
#     collection_name=collection_name,
#     vectors_config=collection_config
# )
# print(f"Collection {collection_name} recreated.")
