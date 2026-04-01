from crewai import Agent, Task, Crew, Process
from app.core.llm_manager import LLMFactory
from typing import Dict, Any

class CrewManager:
    """
    Skill 정의에 따라 Planner, Researcher, Writer 에이전트 간의 
    협업 워크플로우를 구성하고 실행합니다. (AI_INSTRUCTIONS.md #2)
    """
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    def run_workflow(self, skill_def: Dict[str, Any], user_prompt: str) -> str:
        # 1. 에이전트 정의 (Role-Based Collaboration)
        planner = Agent(
            role='Planner',
            goal='사용자의 요청을 분석하고 작업 수행 계획을 세웁니다.',
            backstory='당신은 복잡한 작업을 분석하여 단계별 실행 계획을 수립하는 전문가입니다.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        researcher = Agent(
            role='Researcher',
            goal=f'데이터 소스({skill_def["source"]})에서 필요한 정보를 수집하고 분석합니다.',
            backstory='당신은 방대한 데이터에서 핵심 인사이트를 찾아내는 분석 전문가입니다.',
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

        writer = Agent(
            role='Writer',
            goal=f'수집된 정보를 바탕으로 최종 결과물({skill_def["action"]})의 초안을 작성합니다.',
            backstory='당신은 데이터를 사람이 이해하기 쉬운 보고서나 구조화된 문서로 만드는 문서화 전문가입니다.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # 2. 태스크 정의 (SKILLS_INTERFACE.md의 설정을 태스크로 전환)
        task_planning = Task(
            description=f"사용자 요청: '{user_prompt}'를 분석하고, '{skill_def['task']}'를 수행하기 위한 계획을 작성하세요.",
            agent=planner,
            expected_output="작업 단계별 세부 계획서"
        )

        task_research = Task(
            description=f"계획에 따라 '{skill_def['source']}' 소스에서 데이터를 찾고 분석하세요.",
            agent=researcher,
            expected_output="분석된 원천 데이터 및 인사이트"
        )

        task_writing = Task(
            description=f"최종 보고서를 작성하세요. Action: {skill_def['action']}. 요청사항: {user_prompt}",
            agent=writer,
            expected_output=f"결과물 초안 ({skill_def['action']} 포맷에 최적화된 텍스트)"
        )

        # 3. 크루 구성 및 실행
        crew = Crew(
            agents=[planner, researcher, writer],
            tasks=[task_planning, task_research, task_writing],
            process=Process.sequential, # 순차적 협업
            verbose=True
        )

        result = crew.kickoff()
        return str(result)
