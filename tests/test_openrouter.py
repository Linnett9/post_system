from pathlib import Path
import os
from dotenv import load_dotenv

from infrastructure.llm.openrouter_client import OpenRouterClient


def load_api_key():
    project_root = Path(__file__).resolve().parents[1]
    env_path = project_root / ".env"

    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY")

    return api_key


def test_openrouter_generate():
    print("TEST STARTED")

    api_key = load_api_key()

    print("KEY LOADED")

    client = OpenRouterClient(
        api_key=api_key,
        model="deepseek/deepseek-chat"
    )

    print("CLIENT CREATED")

    response = client.generate("Say hello in one sentence")

    print("RESPONSE:")
    print(repr(response))


if __name__ == "__main__":
    test_openrouter_generate()