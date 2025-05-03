# app/services/umbler.py

from pprint import pprint

import httpx

from app.config.config import settings

BASE_URL = "https://app-utalk.umbler.com/api/v1"


async def send_umbler_message(chat_id: str, text: str):
    url = f"{BASE_URL}/messages"
    payload = {
        "chatId": chat_id,
        "message": text,
        "organizationId": settings.ORGANIZATION_ID,
    }
    headers = {
        "Authorization": f"Bearer " + settings.UMBLER_TALk_API_KEY,
        "Content-Type": "application/json",
    }
    pprint(payload)
    pprint(headers)

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
