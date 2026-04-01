from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.interfaces.agent_controller import router as agent_router
import uvicorn

app = FastAPI(
    title="RFGO Agent Engine",
    description="CrewAI 기반의 기업용 에이전트 서비스"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(agent_router, prefix="/agent", tags=["Agent"])

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "rfgo-agent-engine"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
