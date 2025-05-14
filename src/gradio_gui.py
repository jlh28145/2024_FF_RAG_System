import gradio as gr
from rag_pipeline import RAGSystem, Config  # Assuming your RAG code is in rag_pipeline.py

class RAGApp:
    def __init__(self):
        # Initialize RAG system
        self.config = Config(
            embeddings_dir="/home/von/Desktop/Personal/2024_FF_RAG_System/data/embeddings",
            chroma_db_dir="/home/von/Desktop/Personal/2024_FF_RAG_System/data/chroma_db",
            processed_dir="/home/von/Desktop/Personal/2024_FF_RAG_System/data/processed",
            embedding_model_name="nomic-embed-text",
            llm_model_name="mistral",
            retrieval_k=3,
            use_ollama_embeddings=True
        )
        self.rag = RAGSystem(self.config)
        self.rag.setup()
        
    def ask_question(self, question):
        """Handle question submission"""
        if not question.strip():
            return "Please enter a question."
        try:
            response = self.rag.query(question)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

def create_gradio_interface():
    app = RAGApp()
    
    with gr.Blocks(title="RAG Question Answering System", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # RAG Question Answering System
        Ask questions about your documents and get AI-powered answers.
        """)
        
        with gr.Row():
            question_input = gr.Textbox(
                label="Enter your question",
                placeholder="What would you like to know?",
                lines=3
            )
        
        submit_btn = gr.Button("Ask", variant="primary")
        
        answer_output = gr.Textbox(
            label="Answer",
            interactive=False,
            lines=10
        )
        
        examples = gr.Examples(
            examples=[
                "What is the main topic of these documents?",
                "Can you summarize the key points?",
                "What are the most important findings?"
            ],
            inputs=question_input
        )
        
        submit_btn.click(
            fn=app.ask_question,
            inputs=question_input,
            outputs=answer_output
        )
        
        question_input.submit(
            fn=app.ask_question,
            inputs=question_input,
            outputs=answer_output
        )
    
    return demo

if __name__ == "__main__":
    # Create and launch the interface
    interface = create_gradio_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )