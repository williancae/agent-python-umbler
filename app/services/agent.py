# app/services/agent.py

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import Runnable

from app.prompts.ctb_prompt import INSTRUCTION
from app.services.openai_client import get_openai_chat

llm = get_openai_chat()


async def run_agent_with_history(history: list[dict], user_input: str) -> str:
    messages = [SystemMessage(content=INSTRUCTION)]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=user_input))
    response = await llm.ainvoke(messages)
    return response.content
