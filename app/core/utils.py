import httpx
from .exceptions import AppException


class AIServerRequestError(AppException):
    """Raised when a request to an AI server fails."""

async def send_to_ai_server(server_url: str, model: str, prompt: str, api_key: str = None):
    url = f"{server_url}"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("result", data)
    except httpx.RequestError as exc:
        raise AIServerRequestError(f"Request to {server_url} failed: {exc}") from exc
    except httpx.HTTPStatusError as exc:
        raise AIServerRequestError(
            f"Server {server_url} returned status {exc.response.status_code}"
        ) from exc

