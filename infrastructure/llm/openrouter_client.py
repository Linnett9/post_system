import requests

from domain.interfaces.llm import ILLM


class OpenRouterClient(ILLM):

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek/deepseek-chat"
    ):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]