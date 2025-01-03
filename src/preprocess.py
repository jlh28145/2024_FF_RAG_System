import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt")
nltk.download("stopwords")

OUTPUT_DIR = "data/processed"

def preprocess_text(filepath, output_dir=OUTPUT_DIR):
    """Cleans and preprocesses text from an article file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove non-alphanumeric characters
        content_cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", content)

        # Tokenization
        tokens = word_tokenize(content_cleaned)

        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        tokens_filtered = [word.lower() for word in tokens if word.lower() not in stop_words]

        # Save preprocessed text
        os.makedirs(output_dir, exist_ok=True)
        processed_filepath = os.path.join(output_dir, os.path.basename(filepath))
        
        with open(processed_filepath, "w", encoding="utf-8") as f:
            f.write(" ".join(tokens_filtered))

        print(f"Preprocessed file saved: {processed_filepath}")
        return processed_filepath
    except Exception as e:
        print(f"Error preprocessing file {filepath}: {e}")
        return None

if __name__ == "__main__":
    # Preprocess all articles in the extracted folder
    raw_articles_dir = "data/articles"
    for file in os.listdir(raw_articles_dir):
        preprocess_text(os.path.join(raw_articles_dir, file))

