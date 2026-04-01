from crewai import Agent, Task, Crew, Process
from app.domain.models import AgentRequest, AgentResponse
from app.infrastructure.llm_factory import LLMFactory
from app.infrastructure.skill_parser import SkillParser
import os

class ExecuteAgentUseCase:
    """
    CrewAI를 사용하여 에이전트 작업을 실행함.
    """
    async def execute(self, request: AgentRequest) -> AgentResponse:
        # 1. LLM 초기화
        llm = LLMFactory.get_llm(
            model_type=request.config.model,
            temperature=request.config.temperature
        )
        
        # 2. Skill 파싱
        skills = SkillParser.parse_markdown(request.skills_content)
        logs = ["Skills parsed successfully."]
        
        # 3. 에이전트 정의 (Role-Based Collaboration)
        planner = Agent(
            role='Planner',
            goal='사용자 쿼리와 Skill을 분석하여 최적의 실행 계획을 수립함.',
            backstory='당신은 복잡한 작업을 작은 단위로 쪼개는 전문가입니다.',
            llm=llm,
            verbose=True
        )
        
        researcher = Agent(
            role='Researcher',
            goal='DB나 RAG를 통해 필요한 데이터를 수집함.',
            backstory='당신은 정확한 데이터를 찾아내는 데이터 분석가입니다.',
            llm=llm,
            verbose=True
        )
        
        writer = Agent(
            role='Writer',
            goal='수집된 데이터를 기반으로 최종 보고서(Excel/PPT)를 작성함.',
            backstory='당신은 데이터를 시각화하고 정리하는 문서화 전문가입니다.',
            llm=llm,
            verbose=True
        )
        
        # 4. Task 생성
        plan_task = Task(
            description=f"사용자 요청: {request.user_query}. 사용 가능한 Skill: {[s.skill_id for s in skills]}",
            agent=planner,
            expected_output="작업을 수행하기 위한 단계별 실행 계획"
        )
        
        research_task = Task(
            description="플래너의 계획에 따라 필요한 데이터를 DB나 문서에서 검색하십시오.",
            agent=researcher,
            expected_output="수집된 원천 데이터 및 요약본"
        )
        
        write_task = Task(
            description="수집된 데이터를 바탕으로 최종 결과물을 생성하십시오.",
            agent=writer,
            expected_output="최종 결과물에 대한 설명 및 파일 생성 여부"
        )
        
        # 5. Crew 실행
        crew = Crew(
            agents=[planner, researcher, writer],
            tasks=[plan_task, research_task, write_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        logs.append("Crew execution completed.")
        
        return AgentResponse(
            status="success",
            message=str(result),
            agent_logs=logs
        )
