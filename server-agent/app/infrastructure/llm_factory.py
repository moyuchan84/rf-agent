import os
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from typing import Union

class LLMFactory:
    """
    APP_ENV (LOCAL | PROD)에 따라 LLM 인스턴스를 생성함.
    """
    @staticmethod
    def get_llm(model_type: str = "ollama", temperature: float = 0.7) -> Union[str, ChatOpenAI]:
        app_env = os.getenv("APP_ENV", "LOCAL").upper()
        
        if app_env == "LOCAL":
            model = os.getenv("OLLAMA_MODEL", "llama3")
            # CrewAI 1.x uses LiteLLM, which supports "ollama/model_name" string format
            return f"ollama/{model}"
        else:
            api_key = os.getenv("INTERNAL_API_KEY")
            base_url = os.getenv("INTERNAL_API_BASE_URL")
            model = os.getenv("INTERNAL_MODEL_NAME", "gpt-4o")
            return ChatOpenAI(
                openai_api_key=api_key,
                base_url=base_url,
                model=model,
                temperature=temperature
            )
