# Part 1: AI Research & Evaluation

This document compares various AI tools, platforms, and models for building a Customer Support Automation Agent, focusing on free/highly accessible options capable of RAG (Retrieval-Augmented Generation) and multi-step workflows.

---

## 1. Large Language Models (LLMs)

I evaluated models based on their ability to perform intent classification, context retrieval, and response generation.

| Feature | Groq (Llama 3 70B/8B) | Google Gemini (1.5 Flash/Pro) | Local Models (Ollama - Llama 3/Mistral) |
| :--- | :--- | :--- | :--- |
| **Capabilities** | Exceptional speed; great reasoning (70B) & classification (8B). | Multimodal; massive context window (1M-2M tokens); deep reasoning. | Good reasoning, fully private, customizable. |
| **Pricing** | Extremely generous free tier. | Free tier available via Google AI Studio. | 100% Free (Compute costs only). |
| **Scalability** | High via API; rate limits on free tier. | High via API; rate limits on free tier. | Limited by local hardware (GPU VRAM). |
| **Ease of Integration** | OpenAI-compatible API; very easy with LangChain. | Official SDK and LangChain integration. | Local API server; easy but requires setup. |
| **Limitations** | Context window limited (8k). | Stricter safety filters sometimes block benign prompts. | Slow generation on CPU/weak GPU. |
| **Best Use Case** | Real-time agents, rapid multi-step reasoning. | Analyzing massive documents, complex generation. | Privacy-critical enterprise applications. |

**Recommendation:** I decided to use **Groq (Llama 3.3 70B)** for ultra-fast reasoning and intent classification. I also heavily relied on **Google's Gemini API for embeddings** (`gemini-embedding-001`) because running local embedding models (like PyTorch) consumes 500MB+ of RAM, which immediately crashes free-tier cloud environments.

---

## 2. Orchestration Frameworks

Building the logic of the AI agent requires a framework to handle tool calling, memory, and prompts.

| Feature | LangChain | CrewAI | n8n (No-Code) |
| :--- | :--- | :--- | :--- |
| **Capabilities** | The industry standard; highly modular, vast integrations. | Built on top of LangChain; focuses on role-playing agents working together. | Visual workflow builder; great for API orchestration. |
| **Pricing** | Open-source (Free). | Open-source (Free). | Free self-hosted / Paid cloud. |
| **Ease of Integration** | High learning curve, but integrates with everything. | Easier for defining agent personas and tasks. | Very easy visual interface, less code required. |
| **Limitations** | Abstractions can become convoluted and hard to debug. | Less flexible than raw LangChain for granular control. | Complex logic can be hard to manage visually. |
| **Best Use Case** | Complex RAG pipelines and custom logic. | Multi-agent systems (e.g., researcher + writer + reviewer). | Zapier alternatives, internal automation. |

**Recommendation:** I chose to use **LangChain** (specifically LCEL) as it provides the most flexibility for a custom RAG workflow and is highly sought after for AI Engineering roles.

---

## 3. Vector Databases

To build the RAG system, I needed a vector database to store and retrieve embedded knowledge (e.g., company policies).

| Feature | FAISS | Pinecone | ChromaDB |
| :--- | :--- | :--- | :--- |
| **Capabilities** | Raw, blazing-fast in-memory similarity search library by Facebook. | Managed cloud vector database; highly scalable. | In-memory/local SQLite storage; user-friendly API. |
| **Pricing** | Free (Open-source). | Free tier (1 index); Paid for scale. | Free (Open-source). |
| **Ease of Integration** | Requires manual numpy array management, but extremely lightweight. | Easy, but requires cloud API key. | Extremely easy (`pip install chromadb`); works locally. |
| **Limitations** | No built-in document management (you must track text chunks yourself). | Dependent on cloud; latency. | Has heavily bloated dependencies that break cloud deploys. |
| **Best Use Case** | Highly optimized, memory-constrained environments. | Production-grade RAG, enterprise search. | Quick local POCs. |

**Recommendation:** I ultimately chose **FAISS**. While ChromaDB is easier to use, its SQLite dependencies can be a nightmare in containerized cloud environments. FAISS operates as a pure mathematical matrix index in RAM, making it infinitely faster, cleaner, and perfect for a streamlined cloud microservice.
