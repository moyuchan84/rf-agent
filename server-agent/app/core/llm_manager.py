import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

load_dotenv()

class LLMFactory:
    """
    APP_ENV (LOCAL | PROD)에 따라 적절한 LLM 객체를 생성하는 팩토리 클래스.
    Agnostic LLM Layer 원칙을 준수하여 에이전트 코드는 실제 LLM 종류를 몰라도 동작합니다.
    """
    
    @staticmethod
    def get_llm():
        app_env = os.getenv("APP_ENV", "LOCAL").upper()
        
        if app_env == "LOCAL":
            # 로컬 개발 환경: Ollama 연동 (SYSTEM_HARNESS.md #3 Environment Switching 참고)
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama3")
            print(f"[LLMFactory] Using Local Ollama: {model} at {base_url}")
            return ChatOllama(
                base_url=base_url,
                model=model,
                temperature=0
            )
        
        elif app_env == "PROD":
            # 운영 환경: 사내 GPT-OSS API 연동 (OpenAI 호환 규격)
            api_key = os.getenv("INTERNAL_API_KEY")
            base_url = os.getenv("INTERNAL_API_BASE_URL")
            model = os.getenv("INTERNAL_MODEL_NAME", "gpt-4o")
            print(f"[LLMFactory] Using Internal GPT-OSS: {model}")
            return ChatOpenAI(
                openai_api_key=api_key,
                base_url=base_url,
                model=model,
                temperature=0
            )
        
        else:
            raise ValueError(f"Invalid APP_ENV: {app_env}. Must be 'LOCAL' or 'PROD'.")

# 공용 에이전트 LLM 초기화 (싱글톤 패턴으로 사용 가능)
# llm = LLMFactory.get_llm()
