from sentence_transformers import SentenceTransformer
import os
import pickle

MODEL_NAME = "all-MiniLM-L6-v2"  # Example model for embeddings
EMBEDDINGS_DIR = "data/embeddings"

def generate_embeddings(filepath, model, output_dir=EMBEDDINGS_DIR):
    """Generates and saves embeddings for a given article."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Generate embeddings
        embeddings = model.encode(content, convert_to_tensor=True)

        # Save embeddings
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, os.path.basename(filepath).replace(".txt", ".pkl"))
        
        with open(output_file, "wb") as f:
            pickle.dump(embeddings, f)

        print(f"Embeddings saved: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error generating embeddings for {filepath}: {e}")
        return None

if __name__ == "__main__":
    model = SentenceTransformer(MODEL_NAME)
    processed_articles_dir = "data/processed"
    for file in os.listdir(processed_articles_dir):
        generate_embeddings(os.path.join(processed_articles_dir, file), model)
