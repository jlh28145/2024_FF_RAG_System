import os
import pickle
from typing import List, Optional
from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM  # Updated import
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings  # Updated import

@dataclass
class Config:
    """Configuration for the RAG system"""
    embeddings_dir: str = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/embeddings"
    chroma_db_dir: str = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/chroma_db"
    processed_dir: str = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/processed"
    embedding_model_name: str = "nomic-embed-text"  # or "nomic-embed-text" for Ollama
    llm_model_name: str = "mistral"
    retrieval_k: int = 3
    use_ollama_embeddings: bool = True

class RAGSystem:
    """A complete RAG system with document loading, vector storage, and query capabilities"""
    
    def __init__(self, config: Config):
        self.config = config
        self.vectordb = None
        self.qa_chain = None
        
    def load_documents_from_pkl(self) -> List[Document]:
        """Load documents from pickle files in the embeddings directory"""
        all_docs = []
        for file in os.listdir(self.config.embeddings_dir):
            if file.endswith(".pkl"):
                with open(os.path.join(self.config.embeddings_dir, file), "rb") as f:
                    docs = pickle.load(f)
                    all_docs.extend(docs)
        return all_docs
    
    def load_documents_from_txt(self) -> List[Document]:
        """Load documents from text files in the processed directory"""
        documents = []
        for filename in os.listdir(self.config.processed_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(self.config.processed_dir, filename), "r", encoding="utf-8") as f:
                    text = f.read()
                    documents.append(Document(page_content=text))
        return documents
    
    def get_embedding_model(self):
        """Initialize the appropriate embedding model based on configuration"""
        if self.config.use_ollama_embeddings:
            return OllamaEmbeddings(model=self.config.embedding_model_name)
        return HuggingFaceEmbeddings(model_name=self.config.embedding_model_name)
    
    def initialize_vectorstore(self, documents: List[Document]) -> Chroma:
        """Initialize ChromaDB vectorstore with documents"""
        embedding_model = self.get_embedding_model()
        
        vectordb = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=self.config.chroma_db_dir
        )
        
        print(f"✅ ChromaDB initialized and saved to {self.config.chroma_db_dir}")
        return vectordb
    
    def load_existing_vectorstore(self) -> Chroma:
        """Load an existing ChromaDB vectorstore"""
        embedding_model = self.get_embedding_model()
        return Chroma(
            persist_directory=self.config.chroma_db_dir,
            embedding_function=embedding_model
        )
    
    def build_qa_chain(self) -> RetrievalQA:
        """Build the RetrievalQA chain with the configured LLM"""
        llm = OllamaLLM(model=self.config.llm_model_name)
        retriever = self.vectordb.as_retriever(search_kwargs={"k": self.config.retrieval_k})
        
        return RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )
    
    def setup(self) -> None:
        """Setup the complete RAG system"""
        # Try to load existing vectorstore first
        if os.path.exists(self.config.chroma_db_dir):
            print("Loading existing ChromaDB...")
            self.vectordb = self.load_existing_vectorstore()
        else:
            print("No existing ChromaDB found, creating one...")
            # Try loading from pickle files first, then fall back to text files
            try:
                documents = self.load_documents_from_pkl()
            except (FileNotFoundError, pickle.PickleError):
                documents = self.load_documents_from_txt()
            
            self.vectordb = self.initialize_vectorstore(documents)
        
        self.qa_chain = self.build_qa_chain()
    
    def query(self, question: str) -> str:
        """Query the RAG system with a question"""
        if not self.qa_chain:
            raise ValueError("RAG system not initialized. Call setup() first.")
        # Updated from run() to invoke()
        result = self.qa_chain.invoke({"query": question})
        return result["result"]
    
    def interactive_query(self) -> None:
        """Run an interactive query session"""
        print("\nInteractive RAG Query Session (type 'exit' to quit)")
        while True:
            query = input("\nAsk a question: ")
            if query.lower() == 'exit':
                break
            response = self.query(query)
            print(f"\nAnswer: {response}")

def main():
    # Configure the RAG system
    config = Config(
        embeddings_dir = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/embeddings",
        chroma_db_dir = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/chroma_db",
        processed_dir = "/home/von/Desktop/Personal/2024_FF_RAG_System/data/processed",
        embedding_model_name = "nomic-embed-text",  # or "nomic-embed-text" for Ollama
        llm_model_name = "mistral",
        use_ollama_embeddings = True
    )
    
    # Initialize and run the RAG system
    rag = RAGSystem(config)
    rag.setup()
    rag.interactive_query()

if __name__ == "__main__":
    main()