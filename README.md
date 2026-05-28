# TechGadgets Customer Support AI Agent

This repository contains the prototype for a Customer Support Automation Agent built for the AI Researcher evaluation. 

## Features
- **Multi-step Agent Workflow**: Accurately classifies user intent before generating a response.
- **Retrieval-Augmented Generation (RAG)**: Utilizes ChromaDB to securely answer questions based on company policies.
- **Accessible Tools**: Built using Google Gemini APIs and free local sentence embeddings.
- **Interactive UI**: A sleek, reactive frontend built entirely in Python using Streamlit.

## Installation

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Set up your API Keys:
   Rename `.env.example` to `.env` and insert your Google Gemini API key.

## Running the Project

1. **Initialize the Vector Database** (Run this once to ingest the knowledge base):
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   python backend/rag.py
   ```
2. **Start the FastAPI Backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. **Start the Streamlit Frontend** (In a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

## Repository Structure
- `backend/`: FastAPI application, LangChain logic, and RAG data.
- `frontend/`: Streamlit interactive UI.
- `research_evaluation.md`: Part 1: Comparison of AI tools and frameworks.
- `recommendation_report.md`: Part 3: Production architecture and scaling strategy.
