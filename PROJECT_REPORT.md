# Project Report: AI Customer Support Agent Prototype

## 1. Project Overview & Purpose
The goal of this project was to design, build, and deploy a robust AI-powered Customer Support Agent. The primary objective was to demonstrate practical, production-ready AI engineering skills, including **Retrieval-Augmented Generation (RAG)**, **Agentic Workflows**, and **Full-Stack Integration** (FastAPI + Streamlit).

To make the assignment stand out, we evolved the project from a generic "TechGadgets" template into a highly customized, production-grade prototype for a fictional digital agency named **WebCraft Digital** (heavily inspired by real-world digital agency workflows, specifically Webvory). This demonstrated our ability to research a specific domain, extract relevant business logic, and inject it into an AI workflow.

## 2. Technical Architecture & Tech Stack

### Core Frameworks
- **Backend:** FastAPI (Python) for high-performance API routing.
- **Frontend:** Streamlit for rapid, interactive, and beautiful UI prototyping.
- **Orchestration:** LangChain for building the multi-step agent workflow.

### AI & Machine Learning Components
- **LLM Engine:** Groq API running `llama-3.3-70b-versatile`. We chose Groq for its blazing-fast inference speeds, and Llama 3.3 70B for its state-of-the-art reasoning capabilities.
- **Vector Database:** FAISS (Facebook AI Similarity Search) running completely in-memory.
- **Embeddings:** `SentenceTransformers` using the `all-MiniLM-L6-v2` model. This allows for free, fast, local embedding generation without relying on external API calls for vectorization.

## 3. The Agentic Workflow
The system utilizes a 3-step LangChain workflow designed for determinism and accuracy:

1. **Intent Classification:** The user's prompt is first sent to the LLM to classify the intent (e.g., *Service Inquiry*, *Pricing*, *Project Timeline*). This step ensures we understand *why* the user is asking the question.
2. **Context Retrieval (RAG):** The prompt is vectorized and checked against the FAISS database. The top 3 most mathematically relevant chunks of the Markdown knowledge base are retrieved.
3. **Response Generation:** The retrieved chunks are injected into a strict system prompt. The LLM is instructed to answer the user's question **only** using the injected context, eliminating hallucination.

## 4. Key Milestones & Experimentation Phase

### Phase 1: The RAG Pipeline Upgrade
Initially, the RAG system was hardcoded to read a single `.txt` file. We upgraded the script (`rag.py`) to dynamically scan a `data/` directory and ingest both `.txt` and `.md` files. We implemented smart chunking logic that splits documents based on Markdown headers (`##`), ensuring that each vector chunk maintains semantic meaning rather than arbitrary character cut-offs.

### Phase 2: Web Scraping & Persona Rebranding
To demonstrate research capabilities, we scraped a real digital agency (Webvory) to understand their services, pricing models, and project timelines. We then synthesized this data into a new Markdown knowledge base (`webcraft_kb.md`), stripping out real contact info and locations to avoid legal/privacy issues. We updated the system prompts to adopt the persona of "WebCraft Digital."

### Phase 3: Frontend UI Polish
We built a Streamlit frontend (`app.py`) and injected custom CSS to match the brand's aesthetic (a modern purple gradient). We added dynamic intent badges, a custom sidebar, and intelligent error handling.

## 5. Challenges Encountered & Solved

- **Dependency Conflicts (Pydantic & Python 3.12):** Encountered a fatal `ModuleNotFoundError` and `ForwardRef` typing error due to incompatibilities between Python 3.12 and older versions of Pydantic used by LangChain. Solved by forcefully unpinning and upgrading the `langchain-core` and `pydantic` ecosystem in the virtual environment.
- **Absolute Import Routing:** Encountered issues running Uvicorn due to absolute imports (`backend.main`). Solved by establishing the correct working directory and exporting the `PYTHONPATH` (`export PYTHONPATH=$PYTHONPATH:.`).
- **IDE Language Server Path Resolution:** The local IDE (Pyright/Pylance) displayed red error lines despite the app running correctly because it was scanning the global Mac Python installation. Solved by injecting absolute hardcoded paths into `pyrightconfig.json` and `.vscode/settings.json`, forcing the IDE to index the `customerenv` virtual environment.

## 6. Conclusion
This prototype successfully demonstrates a complete, end-to-end AI application. It showcases the ability to manage local embedding models, integrate ultra-fast cloud LLMs, handle backend API routing, build consumer-facing frontends, and debug complex Python environment issues.
