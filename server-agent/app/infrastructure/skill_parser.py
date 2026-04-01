import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class SkillDefinition(BaseModel):
    skill_id: str
    task: str
    source: str
    action: str
    params: Dict[str, Any] = {}

class SkillParser:
    """
    SKILLS_INTERFACE.md 파싱 규격에 따라 마크다운을 SkillDefinition 객체로 변환함.
    """
    @staticmethod
    def parse_markdown(content: str) -> List[SkillDefinition]:
        skills = []
        # Skill 섹션별로 분리
        sections = re.split(r"### Skill: ", content)
        
        for section in sections:
            if not section.strip():
                continue
                
            lines = section.split("\n")
            skill_id = lines[0].strip()
            
            task = re.search(r"- \*\*Task\*\*: (.*)", section)
            source = re.search(r"- \*\*Source\*\*: (.*)", section)
            action = re.search(r"- \*\*Action\*\*: (.*)", section)
            params_match = re.search(r"- \*\*Params\*\*: (.*)", section)
            
            params = {}
            if params_match:
                try:
                    import json
                    params = json.loads(params_match.group(1).replace("'", '"'))
                except:
                    params = {}

            skills.append(SkillDefinition(
                skill_id=skill_id,
                task=task.group(1).strip() if task else "",
                source=source.group(1).strip() if source else "",
                action=action.group(1).strip() if action else "",
                params=params
            ))
            
        return skills
