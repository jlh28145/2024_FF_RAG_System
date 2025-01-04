import pickle
import chromadb
from chromadb.config import Settings

# Load embeddings from the .pkl file
with open("data/embeddings/2024_Fantasy_Football_Season_In_Review:_What_Natha.pkl", "rb") as file:
    embeddings = pickle.load(file)

# Initialize Chroma client
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))

# Create or get a collection
collection_name = "my_collection"
collection = client.create_collection(name=collection_name)

# Insert embeddings into the collection (assume you have metadata to go with them)
metadata = [{"id": str(i), "text": f"Sample text {i}"} for i in range(len(embeddings))]
collection.add(
    documents=[m["text"] for m in metadata],
    metadatas=metadata,
    embeddings=embeddings
)

# # Query the vectorstore
# query = "example query text"
# query_embedding = your_embedding_function(query)
# results = collection.query(
#     query_embeddings=[query_embedding],
#     n_results=5
# )

# print(results)
