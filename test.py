# import requests

# url = "https://e48e2bbc-51d8-4898-9c1b-cbaa2fea6c26.europe-west3-0.gcp.cloud.qdrant.io/collections"
# headers = {
#     "Authorization": "Bearer vm-sD1hZvTTQFb8a_PLk-nuwM7lugKHSy3OVB_keG_LL6ULKjiCy2Q"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     print("Collections:", response.json())
# else:
#     print(f"Failed to connect: {response.status_code}")



import streamlit as st


print(st.secrets["QDRANT_URL"])
