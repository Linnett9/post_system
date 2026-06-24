import requests

from domain.interfaces.llm import ILLM


class OpenRouterClient(ILLM):
    def __init__(
        self,
        api_key: str,
        model: str = "openrouter/auto",
        timeout: int = 60,
    ):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, prompt: str) -> str:
        print(f"OpenRouter requested model: {self.model}")

        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/Linnett9/post_system",
                "X-OpenRouter-Title": "Deelicious Eats Post System",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
            timeout=self.timeout,
        )

        if not response.ok:
            raise RuntimeError(
                f"OpenRouter API error {response.status_code}: {response.text}"
            )

        data = response.json()

        served_model = data.get("model", self.model)
        print(f"OpenRouter served model: {served_model}")

        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError(f"OpenRouter returned no choices: {data}")

        message = choices[0].get("message", {})
        content = message.get("content")

        if not content:
            raise RuntimeError(f"OpenRouter returned no content: {data}")

        return content