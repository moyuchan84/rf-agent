# AI_INSTRUCTIONS.md

## 1. Persona & Goal
- Role: 전문 MAS(Multi-Agent System) 엔지니어.
- Stack: LangChain, CrewAI, FastAPI, SQLAlchemy.
- Goal: 사용자가 정의한 `skills.md`를 기반으로 DB 연동, RAG, 문서 생성을 수행하는 에이전트 시스템 구축.

## 2. Architecture Principles
- **Agnostic LLM Layer**: 모든 LLM 호출은 `app/core/llm_manager.py`의 `LLMFactory`를 거치며, `APP_ENV` (local/prod)에 따라 Ollama와 사내 GPT-OSS API를 자동 전환함.
- **Middleware-First**: 클라이언트는 직접 LLM을 호출하지 않고, FastAPI로 구성된 'Agent Gateway' 서버를 통해 통신함. 이 서버는 로드밸런싱과 토큰 관리를 담당함.
- **Role-Based Collaboration**: 단일 에이전트가 모든 일을 하지 않고, CrewAI를 활용해 Planner, Researcher(DB/RAG), Writer(Excel/PPT) 에이전트로 역할을 분리함.

## 3. Implementation Rules
- **Schema-Driven**: 모든 데이터 교환은 Pydantic 모델을 사용하여 타입을 엄격히 제한함.
- **Async I/O**: 서버와 에이전트 간 통신, DB 쿼리는 `async/await`를 사용하여 처리 성능을 최적화함.
- **Security**: SQL Injection 방지를 위해 Raw Query 대신 SQLAlchemy Expression 혹은 Text Clause(Bind params)를 사용함.

## 4. Proejct folder tree
/my-agent-project (Root)
├── AI_INSTRUCTIONS.md       <-- (유지) 전체 개발 원칙
├── SYSTEM_HARNESS.md        <-- (유지) 시스템 흐름 및 통신 규격
├── SKILLS_INTERFACE.md      <-- (유지) Skills.md 파싱 규격
│
├── /server-agent (Backend)  <-- Python 에이전트 엔진
│   ├── app/
│   │   ├── main.py          # FastAPI 엔드포인트
│   │   ├── core/            # LLMFactory (Ollama/GPT-OSS)
│   │   ├── agents/          # CrewAI 로직
│   │   └── tools/           # DB/Excel/PPT 실제 기능
│   └── requirements.txt
│
└── /client-electron (Frontend) <-- 사용자 UI 및 브라우저 제어
    ├── src/
    │   ├── main.js          # Electron 메인 프로세스
    │   └── renderer.js      # UI 로직 및 서버 API 호출
    └── package.json


## 5. Architecture & Tech Stack Rules

### [Backend: Clean Architecture]
- **Layers:** - `domain/`: Business Logic & Entities (Framework 독립적)
  - `usecases/`: Application Business Rules (에이전트 시나리오)
  - `infrastructure/`: DB, API Clients, External Tools (Ollama/GPT-OSS)
  - `interfaces/`: FastAPI Controllers, DTOs
- **Rule:** 의존성은 외부에서 내부(Domain)로만 향해야 함.

### [Frontend: Feature-Based React]
- **Stack:** Vite + TypeScript + React + Tailwind CSS
- **State Management:** Zustand (Store)
- **Directory Structure:**
  - `features/`: 기능 단위(Agent, Skills, History)로 분리
    - `components/`, `hooks/`, `services/`, `store/` 포함
  - `shared/`: 공통 컴포넌트(UI), 유틸리티
  - `api/`: Axios 인스턴스 및 중앙화된 API 호출 로직