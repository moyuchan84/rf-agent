# SYSTEM_HARNESS.md

## 1. System Topology
- **Client**: Electron/Chrome Extension (사용자 UI, skills.md 업로드).
- **Gateway (Middleware)**: FastAPI 기반 로드밸런서.
  - 요청을 큐잉하고 사내 LLM API의 Rate Limit에 맞춰 요청 분배.
  - 에이전트의 상태(State) 및 결과물(File) 캐싱.
- **Agent Engine**: CrewAI 기반 워크플로우.
  - `BaseModelFactory`: Ollama(개발용) <-> 사내 API(운영용) 어댑터.
  - `SkillManager`: 사용자의 `skills.md`를 런타임에 LangChain Tool로 변환.

## 2. Data Workflow
1. Client -> Gateway: 작업 요청 및 Skill 정의 전달.
2. Gateway -> Agent Engine: 작업 할당.
3. Agent (Researcher): DB/RAG를 통해 컨텍스트 확보.
4. Agent (Writer): 확보된 데이터로 Excel/PPT 생성 (Pandas, python-pptx).
5. Gateway -> Client: 결과 파일 다운로드 링크 또는 데이터 반환.

## 3. Environment Switching
- `LOCAL`: `Ollama` (llama3, mistral) 접속.
- `PROD`: 사내 `GPT-OSS` (OpenAI 규격 API) 접속.


## 4. Client-Server 통신 프로토콜 (API 규격 가이드)

[API Request: POST /agent/run]
클라이언트가 서버로 보낼 데이터 형식입니다.

JSON
{
  "user_query": "지난달 매출 데이터를 DB에서 가져와서 엑셀 보고서 만들어줘",
  "skills_content": "### Skill: Excel_Gen\n- Task: 매출 데이터 요약\n- Action: Excel_Export...", 
  "config": {
    "model": "ollama",
    "temperature": 0.7
  }
}
[API Response]
서버가 작업을 마치고 클라이언트에 돌려줄 형식입니다.

JSON
{
  "status": "success",
  "message": "엑셀 보고서 생성이 완료되었습니다.",
  "output_file_path": "/absolute/path/to/report.xlsx",
  "agent_logs": ["DB 쿼리 완료", "Pandas 데이터 가공 완료", "파일 저장 완료"]
}

# SYSTEM_HARNESS.md (보강)

## 1. Frontend Flow (React + Zustand)
1. **User Input:** 사용자가 UI에서 `skills.md` 작성 및 실행 버튼 클릭.
2. **Store Action:** `useAgentStore`에서 요청 상태를 `loading`으로 변경.
3. **Custom Hook:** `useExecuteAgent` 훅에서 `api/agentService`를 호출.
4. **API Call:** Axios를 통해 Backend FastAPI 엔드포인트(`POST /agent/run`)로 데이터 전송.

## 2. Backend Flow (Clean Architecture)
1. **Interface Layer:** FastAPI가 요청을 받고 DTO로 변환.
2. **Usecase Layer:** `ExecuteAgentUseCase` 실행.
3. **Infrastructure Layer:** - `LLMFactory`를 통해 모델 인스턴스 생성.
   - `SkillParser`를 통해 마크다운을 Tool로 변환.
   - `CrewAI`를 실행하여 결과 도출.
4. **Response:** 최종 결과(파일 경로 등)를 클라이언트로 반환.