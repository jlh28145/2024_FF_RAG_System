# 2024_FF_RAG_System
# Retrieval-Augmented Generation (RAG) System for Fantasy Football 2024

## Project Overview
This project implements a Retrieval-Augmented Generation (RAG) system based on the 2024 fantasy football season. The system uses 1 to 3 articles as its initial knowledge base and provides a simple front-end GUI for querying the knowledge. It is built using open-source Python libraries, incorporates Ollama for text generation, and is dockerized for easy deployment. The entire project is hosted in a GitHub repository.

---

## Features
- **Knowledge Base:** Utilizes 1 to 3 articles on fantasy football.
- **RAG Pipeline:** Combines retrieval and generation using embeddings.
- **Frontend:** Interactive GUI for querying the knowledge base.
- **Dockerized:** Simplified deployment and portability.
- **Open Source:** Built entirely with open-source Python libraries.

---

## System Architecture
1. **Knowledge Ingestion:** Articles are preprocessed and converted into embeddings.
2. **Retrieval:** Relevant sections of the articles are retrieved based on user queries.
3. **Generation:** Retrieved sections are enhanced with AI-generated responses.
4. **Frontend:** Provides a GUI for user interaction.

---

## Setup Instructions

### Prerequisites
- Python 3.9 or later
- Docker
- A machine with internet access

### Installation
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate # On Windows: .\env\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Prepare Knowledge Base**
   - Add 1 to 3 articles in the `data/articles` directory.
   - Run the script to preprocess and create embeddings:
     ```bash
     python preprocess.py
     ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Run with Docker**
   - Build the Docker image:
     ```bash
     docker build -t rag-system .
     ```
   - Run the container:
     ```bash
     docker run -p 8501:8501 rag-system
     ```

---

## Usage Instructions
1. Launch the GUI (available at `http://localhost:8501` when using Docker).
2. Enter your query in the input box.
3. View the generated answer in the response area.

---

## Folder Structure
```
.
├── data
│   ├── articles       # Folder for raw article files
│   ├── embeddings     # Folder for preprocessed embeddings
├── src
│   ├── preprocess.py  # Script to preprocess and embed articles
│   ├── app.py         # Main application file
│   ├── rag_pipeline.py # Retrieval and generation logic
├── Dockerfile          # Docker setup file
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## Future Improvements
- Add support for dynamic knowledge base updates.
- Expand GUI functionality for enhanced user interaction.
- Incorporate advanced generation techniques.
- Explore integration with additional fantasy football data sources.

---

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


