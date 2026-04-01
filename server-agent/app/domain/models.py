from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AgentConfig(BaseModel):
    model: str = "ollama"
    temperature: float = 0.7

class AgentRequest(BaseModel):
    user_query: str = Field(..., description="사용자의 작업 요청 쿼리")
    skills_content: str = Field(..., description="skills.md에서 파싱된 마크다운 내용")
    config: AgentConfig = Field(default_factory=AgentConfig)

class AgentResponse(BaseModel):
    status: str = "success"
    message: str
    output_file_path: Optional[str] = None
    agent_logs: List[str] = Field(default_factory=list)
