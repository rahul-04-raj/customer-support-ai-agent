"""
Customer Support AI Agent Workflow
Uses LangChain + Groq (Llama 3.3 70B) for blazing fast inference.
Multi-step workflow: Intent Classification -> RAG Retrieval -> Response Generation
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.rag import retrieve

load_dotenv()


def get_llm():
    """Initialize the LLM using Groq API (Llama 3.3 70B - free tier)."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or "your_groq_api_key_here" in api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Please set it in the .env file. "
            "Get a free key at: https://console.groq.com/keys"
        )

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=api_key,
    )


def classify_intent(query: str) -> str:
    """Step 1: Classify the customer's intent using LangChain + Groq."""
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """Classify the following customer query for a digital agency into one of these categories:
- Service Inquiry
- Pricing / Quotation
- Project Timeline
- Technical Question
- General Inquiry
- Escalation / Human Requested

Use "Escalation / Human Requested" ONLY when the user is clearly frustrated, angry, dissatisfied with the AI responses, or explicitly asks to speak to a human/real person/manager.

Query: {query}

Return ONLY the category name and nothing else."""
    )

    chain = prompt | llm | StrOutputParser()
    intent = chain.invoke({"query": query})
    return intent.strip()


def generate_response(query: str, context: str) -> str:
    """Step 3: Generate a helpful response using LangChain RAG chain."""
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """You are a helpful and professional customer support assistant for WebCraft Digital, a creative web design, development, and SEO agency.

Answer the user's question based ONLY on the provided context from our knowledge base.
If the context does not contain the answer, politely state that you don't have that specific information and suggest they book a free consultation call for personalized advice.

Keep your response concise, friendly, and professional. Use bullet points when listing multiple items.

Context:
{context}

Customer Question: {question}

Response:"""
    )

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"context": context, "question": query})
    return response.strip()


def run_agent(query: str) -> dict:
    """Orchestrates the full agent workflow: Classification -> RAG Retrieval -> Generation."""

    # Step 1: Classify intent using LangChain
    try:
        intent = classify_intent(query)
    except Exception as e:
        return {"error": f"Classification failed: {str(e)}", "intent": "Error", "response": ""}

    # Step 2: Retrieve relevant context from FAISS vector database
    try:
        context = retrieve(query, top_k=3)
    except Exception as e:
        return {"error": f"Retrieval failed: {str(e)}", "intent": intent, "response": ""}

    # Step 3: Generate response using LangChain RAG chain
    try:
        response = generate_response(query, context)
    except Exception as e:
        return {"error": f"Generation failed: {str(e)}", "intent": intent, "response": ""}

    return {
        "intent": intent,
        "response": response,
    }


def summarize_conversation(messages: list[dict]) -> str:
    """Summarize the conversation history into a concise bullet-point summary for human handoff."""
    llm = get_llm()

    # Build a readable chat log from the messages
    chat_log = "\n".join(
        f"{'Customer' if m['role'] == 'user' else 'AI Agent'}: {m['content']}"
        for m in messages
    )

    prompt = ChatPromptTemplate.from_template(
        """You are summarizing a customer support conversation for a human support agent who will take over.

Create a concise summary with:
- What the customer's main issue or question was
- What the AI agent tried to help with
- Why the customer needs human assistance
- Any important details mentioned (service type, budget, timeline, etc.)

Conversation:
{chat_log}

Summary:"""
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"chat_log": chat_log}).strip()
