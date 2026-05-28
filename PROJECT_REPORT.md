# Project Report: AI Customer Support Agent Prototype

## 1. Project Overview & Purpose
The goal of this project was to design, build, and deploy a robust AI-powered Customer Support Agent. My primary objective was to demonstrate practical, production-ready AI engineering skills, including **Retrieval-Augmented Generation (RAG)**, **Agentic Workflows**, and **Full-Stack Microservices Integration** (FastAPI + Streamlit deployed to the cloud).

To make the assignment stand out, I evolved the project from a generic "TechGadgets" template into a highly customized, production-grade prototype for a fictional digital agency named **WebCraft Digital** (heavily inspired by real-world digital agency workflows). This demonstrated my ability to research a specific domain, extract relevant business logic, and inject it into an AI workflow.

## 2. Technical Architecture & Tech Stack

### Core Frameworks
- **Backend:** FastAPI (Python) for high-performance API routing. Deployed on **Render.com**.
- **Frontend:** Streamlit for rapid, interactive, and beautiful UI prototyping. Deployed on **Streamlit Community Cloud**.
- **Orchestration:** LangChain for building the multi-step agent workflow.

### AI & Machine Learning Components
- **LLM Engine:** Groq API running `llama-3.3-70b-versatile`. I chose Groq for its blazing-fast inference speeds, and Llama 3.3 70B for its state-of-the-art reasoning capabilities.
- **Vector Database:** FAISS (Facebook AI Similarity Search) running completely in-memory.
- **Embeddings:** Google's `gemini-embedding-001` API. I explicitly migrated to this API-based embedding model to drop memory usage from ~500MB (PyTorch) to ~50MB, allowing the backend to run flawlessly on Render's free tier.

## 3. The Agentic Workflow
The system utilizes a 3-step LangChain workflow designed for determinism and accuracy:

1. **Intent Classification:** The user's prompt is first sent to the LLM to classify the intent (e.g., *Service Inquiry*, *Pricing*, *Escalation*). This step ensures I understand *why* the user is asking the question.
2. **Context Retrieval (RAG):** The prompt is vectorized via Google API and checked against the FAISS database. The top 3 most mathematically relevant chunks of the Markdown knowledge base are retrieved.
3. **Response Generation:** The retrieved chunks are injected into a strict system prompt. The LLM is instructed to answer the user's question **only** using the injected context, eliminating hallucination.

## 4. Key Milestones & Experimentation Phase

### Phase 1: The RAG Pipeline Upgrade
Initially, the RAG system was hardcoded to read a single `.txt` file. I upgraded the script (`rag.py`) to dynamically scan a `data/` directory and ingest both `.txt` and `.md` files. I implemented smart chunking logic that splits documents based on Markdown headers (`##`), ensuring that each vector chunk maintains semantic meaning rather than arbitrary character cut-offs.

### Phase 2: Web Scraping & Persona Rebranding
To demonstrate research capabilities, I scraped a real digital agency to understand their services, pricing models, and project timelines. I then synthesized this data into a new Markdown knowledge base (`webcraft_kb.md`), stripping out real contact info and locations to avoid legal/privacy issues. I updated the system prompts to adopt the persona of "WebCraft Digital."

### Phase 3: Frontend UI Polish & Escalation Workflow
I built a Streamlit frontend (`app.py`) and injected custom CSS to match the brand's aesthetic (a modern purple gradient). I added dynamic intent badges, a custom sidebar, and an automated email escalation workflow. If the AI detects frustration, it triggers an interactive form to collect the user's email, summarizes the conversation history, and fires off a real email via Gmail SMTP to a human manager.

## 5. Challenges Encountered & Solved

- **Cloud Memory Limits (OOM):** When deploying to Render, the container crashed with an Out Of Memory (OOM) error because `sentence-transformers` loaded PyTorch into memory (~500MB). I solved this by ripping out PyTorch and refactoring the RAG system to use Google's `gemini-embedding-001` API, dropping memory usage down to ~50MB.
- **OpenMP Library Conflicts:** Encountered `OMP: Error #15` crashes locally because PyTorch and FAISS both tried to link against the OpenMP runtime simultaneously. Solved by forcefully uninstalling all local torch packages since they were no longer needed.
- **Streamlit Secrets Handling:** When deploying the frontend to Streamlit Cloud, the app couldn't find the backend URL. I refactored the environment variable logic to gracefully fallback between `st.secrets` (for Cloud) and `os.getenv` (for Local), while stripping accidental whitespaces.

## 6. Conclusion
This prototype successfully demonstrates a complete, end-to-end AI application. It showcases my ability to manage vector databases, integrate ultra-fast cloud LLMs, handle backend API routing, build consumer-facing frontends, configure cloud microservices (Render + Streamlit), and debug complex Python environments and memory constraints.
