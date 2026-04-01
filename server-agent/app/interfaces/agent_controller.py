from fastapi import APIRouter, HTTPException
from app.domain.models import AgentRequest, AgentResponse
from app.usecases.execute_agent import ExecuteAgentUseCase

import traceback

router = APIRouter()

@router.post("/run", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    에이전트 작업을 실행하는 엔드포인트.
    """
    try:
        usecase = ExecuteAgentUseCase()
        response = await usecase.execute(request)
        return response
    except Exception as e:
        print(f"Error in /agent/run: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
