from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.agent.graph import app_agent

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    success: bool
    intent: str
    answer: str

@router.post("/query", response_model=QueryResponse)
async def query_bot(request: QueryRequest):
    try:
        # Invoke the LangGraph agent
        result = app_agent.invoke({"question": request.question})
        
        return {
            "success": result.get("success", True),
            "intent": result.get("intent", "unknown"),
            "answer": result.get("answer", "I'm sorry, I couldn't find an answer.")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))