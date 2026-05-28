# TechGadgets Customer Support AI Agent

This repository contains the prototype for a Customer Support Automation Agent built for my AI Researcher evaluation. 

## Features
- **Multi-step Agent Workflow**: Accurately classifies user intent before generating a response.
- **Retrieval-Augmented Generation (RAG)**: Utilizes FAISS vector database to securely answer questions based on company policies.
- **Lightweight Embeddings**: Uses Google's `gemini-embedding-001` API to keep memory usage under 50MB, making it easily deployable on free cloud tiers.
- **Cloud Microservices Architecture**: Backend deployed on Render, Frontend deployed on Streamlit Community Cloud.
- **Interactive UI**: A sleek, reactive frontend built entirely in Python using Streamlit, featuring a purple gradient theme.

## Installation & Running Locally

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv customerenv
   source customerenv/bin/activate
   pip install -r requirements.txt
   ```
3. Set up your API Keys in a `.env` file:
   ```env
   GROQ_API_KEY=your_key
   GOOGLE_API_KEY=your_key
   SMTP_EMAIL=your_email
   SMTP_PASSWORD=your_app_password
   ESCALATION_EMAIL=forwarding_target_email
   ```

## Running the Project

1. **Start the FastAPI Backend**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   uvicorn backend.main:app --reload
   ```
2. **Start the Streamlit Frontend** (In a new terminal):
   ```bash
   streamlit run frontend/app.py
   ```

## Repository Structure
- `backend/`: FastAPI application, LangChain logic, FAISS RAG data, and email escalation service.
- `frontend/`: Streamlit interactive UI.
- `research_evaluation.md`: Part 1: Comparison of AI tools and frameworks.
- `recommendation_report.md`: Part 3: Production architecture and scaling strategy.
- `PROJECT_REPORT.md`: Detailed breakdown of my workflow, challenges, and implementation.
