from neo4j import GraphDatabase
import pickle
import os

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"

def store_embeddings_in_neo4j(embeddings_dir):
    """Stores embeddings and metadata in a Neo4j database."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def insert_embedding(tx, title, embedding):
        query = """
        CREATE (a:Article {title: $title, embedding: $embedding})
        """
        tx.run(query, title=title, embedding=embedding)

    with driver.session() as session:
        for file in os.listdir(embeddings_dir):
            if file.endswith(".pkl"):
                filepath = os.path.join(embeddings_dir, file)
                title = file.replace(".pkl", "")
                with open(filepath, "rb") as f:
                    embedding = pickle.load(f)
                session.write_transaction(insert_embedding, title, embedding)

    print("Embeddings stored in Neo4j.")

if __name__ == "__main__":
    store_embeddings_in_neo4j("data/embeddings")
