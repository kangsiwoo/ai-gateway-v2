import httpx

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

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("result", data)
