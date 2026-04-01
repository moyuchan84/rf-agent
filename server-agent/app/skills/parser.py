import re
import os
from typing import Dict, Any, Optional

class SkillParser:
    """
    SKILLS_INTERFACE.md 파일을 읽어 에이전트 실행에 필요한 
    Task, Source, Action 정보를 추출합니다.
    """
    @staticmethod
    def get_skill_definition(skill_id: str) -> Optional[Dict[str, Any]]:
        # 루트 폴더의 SKILLS_INTERFACE.md 경로 (현재 server-agent/app/skills/ 위치 기준)
        file_path = os.path.join(os.getcwd(), "..", "SKILLS_INTERFACE.md")
        if not os.path.exists(file_path):
            file_path = os.path.join(os.getcwd(), "SKILLS_INTERFACE.md") # Fallback

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 마크다운 섹션 찾기: ### Skill: [ID] ... 다음 ### 전까지
            pattern = rf"### Skill: {re.escape(skill_id)}\n(.*?)(?=\n### Skill:|\Z)"
            match = re.search(pattern, content, re.DOTALL)

            if not match:
                return None

            section = match.group(1)
            
            # 필드 추출 (Task, Source, Action, Params)
            skill_def = {
                "skill_id": skill_id,
                "task": re.search(r"- \*\*Task\*\*: (.*)", section).group(1) if re.search(r"- \*\*Task\*\*: (.*)", section) else "",
                "source": re.search(r"- \*\*Source\*\*: (.*)", section).group(1) if re.search(r"- \*\*Source\*\*: (.*)", section) else "",
                "action": re.search(r"- \*\*Action\*\*: (.*)", section).group(1) if re.search(r"- \*\*Action\*\*: (.*)", section) else "",
                "params": {} # Params는 복잡한 JSON일 수 있으므로 필요 시 추가 파싱
            }
            return skill_def

        except Exception as e:
            print(f"[SkillParser] Error: {e}")
            return None
