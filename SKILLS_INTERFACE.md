# SKILLS_INTERFACE.md

## 1. Skill Markdown Structure
모든 사용자의 Skill 정의는 아래 형식을 준수해야 파서(Parser)가 인식함.

```markdown
### Skill: [Unique_ID]
- **Task**: [무엇을 해야 하는가? 에이전트의 Task 설명으로 주입됨]
- **Source**: [DB 테이블명 또는 RAG 대상 문서 경로]
- **Action**: [Excel_Export | PPT_Export | DB_Update]
- **Params**: { "header_color": "blue", "font_size": 12 }


## 1. Skill Rendering
- 클라이언트 UI는 `skills.md`를 편집할 수 있는 **Monaco Editor** 또는 **Markdown Editor** 컴포넌트를 제공함.
- `Zustand Store`에서 현재 편집 중인 Skill의 상태를 실시간으로 관리함.

## 2. Dynamic Tool Loading
- 서버는 전달받은 마크다운을 파싱하여 `langchain.tools`로 동적 등록함.
- **Validation:** React 프런트엔드에서 서버 전송 전, 규격에 맞는 마크다운인지 일차적으로 검증(Regex/Parser).