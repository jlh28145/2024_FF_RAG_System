# setup_chromadb.py

import os
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

PROCESSED_DIR = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/processed"
CHROMA_DIR = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/chroma_db"

def load_documents_from_txt(folder):
    documents = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(Document(page_content=text))
    return documents

def persist_to_chroma():
    docs = load_documents_from_txt(PROCESSED_DIR)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")  # You can replace this with another Ollama model if needed

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    
    print(f"✅ ChromaDB saved to {CHROMA_DIR}")

if __name__ == "__main__":
    persist_to_chroma()
