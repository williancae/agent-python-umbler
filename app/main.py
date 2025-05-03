from contextlib import asynccontextmanager
from pprint import pprint

from fastapi import FastAPI

from app.db import database
from app.services.agent import run_agent_with_history
from app.services.redis import RedisRepository
from app.services.umbler import send_umbler_message
from app.webhook_pydantic import WebhookPayload

redis_repo = RedisRepository()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await database.connect()
    yield
    # Shutdown logic
    await database.disconnect()


# Make sure to update app initialization to use this lifespan
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "API online 🧠"}


@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    content = payload.Payload.Content
    with open("webhook_payload.txt", "w") as f:
        f.write(payload.model_dump_json(indent=4))

    last_msg = content.LastMessage or content.Message

    if not last_msg or last_msg.MessageType != "Text":
        print(f"[LOOP] Ignorando mensagem não textual: {last_msg}")
        return {"ok": True}

    pprint(
        {
            "messsageState": last_msg.MessageState,
            "source": last_msg.Source,
            "message": last_msg.Content.strip(),
        }
    )
    if last_msg.MessageState != "Read":
        print(f"[LOOP] Ignorando mensagem que é enviado pelo próprio bot: {last_msg}")
        return {"ok": True}

    text = last_msg.Content.strip()
    chat_id = content.Id
    phone = content.Contact.PhoneNumber

    if not phone or not chat_id or not text:
        return {"ok": True}

    if chat_id not in "aBZIo4Rs-KKc1yr7":
        print(f"Chat ID {chat_id} não autorizado.")
        return {"ok": True}

    await redis_repo.append_history(phone, "user", text)
    history = await redis_repo.get_history(phone)

    resposta = await run_agent_with_history(history, text)
    await redis_repo.append_history(phone, "ai", resposta)

    await send_umbler_message(chat_id, resposta)

    return {"ok": True}
