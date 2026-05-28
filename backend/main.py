from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.agent.workflow import run_agent, summarize_conversation
from backend.email_service import send_escalation_email

app = FastAPI(title="Customer Support AI Agent API")


class SupportQuery(BaseModel):
    query: str


class AgentResponse(BaseModel):
    intent: str
    response: str


class EscalationRequest(BaseModel):
    user_email: str
    messages: list[dict]


class EscalationResponse(BaseModel):
    success: bool
    message: str


@app.post("/api/chat", response_model=AgentResponse)
async def chat_endpoint(request: SupportQuery):
    """Endpoint to interact with the AI agent."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    result = run_agent(request.query)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return AgentResponse(
        intent=result["intent"],
        response=result["response"]
    )


@app.post("/api/escalate", response_model=EscalationResponse)
async def escalate_endpoint(request: EscalationRequest):
    """Escalate conversation to a human agent via email."""
    if not request.user_email.strip():
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    if not request.messages:
        raise HTTPException(status_code=400, detail="No conversation to summarize")

    try:
        # Step 1: Use LLM to summarize the conversation
        summary = summarize_conversation(request.messages)

        # Step 2: Send email to the support team
        send_escalation_email(request.user_email, summary)

        return EscalationResponse(
            success=True,
            message="Your request has been forwarded to our support team. We'll contact you shortly!"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Escalation failed: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
