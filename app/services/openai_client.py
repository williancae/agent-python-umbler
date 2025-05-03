from langchain.chat_models.openai import ChatOpenAI

from app.config.config import settings


def get_openai_chat(model: str = "gpt-4o-mini", temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=settings.OPENAI_API_KEY,
    )
