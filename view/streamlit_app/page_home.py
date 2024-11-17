import streamlit as st

def app():
    """
    Render the Home page of the Inspector application.

    This page provides an overview of the application's features and architecture.
    """
    st.markdown("""
        # Inspector

        **Inspector** is a Proof of Concept (POC) for a Python-based web application designed to analyze documents.

        ### Key Features:
        - **Insight Extraction**: Leverages large language models (LLMs) for user-driven document analysis.
        - **Data Privacy**: Securely handles sensitive data by identifying and masking personal information (e.g., names, document numbers) before transmission to external services.
        - **Backend and Frontend Integration**:
            - Backend: Powered by **FastAPI**.
            - Frontend: Built with **Streamlit**.
        - **Tooling**:
            - **Redis** as a vector database for efficient data retrieval.
            - **Apache Tika** for extracting information from diverse document formats.
        - **Advanced AI Techniques**:
            - Retrieval-Augmented Generation (**RAG**).
            - Advanced prompting strategies like Chain-of-Thought and Tree-of-Thought.

        ### How It Works:
        Inspector combines cutting-edge AI and robust backend systems to deliver secure, insightful document analysis for sensitive domains such as medical records.
    """)