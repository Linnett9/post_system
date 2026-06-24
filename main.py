import os
import json
import yaml
from dotenv import load_dotenv

from infrastructure.llm.openrouter_client import OpenRouterClient
from application.post_cleaner import clean_post_content
from application.post_orchestrator import PostOrchestrator
from domain.interfaces.prompt_builder import PromptBuilder
from infrastructure.messaging.telegram_notifier import TelegramNotifier


# ----------------------------
# CONFIG
# ----------------------------
def load_settings(path="settings.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


# ----------------------------
# BUILD SYSTEM
# ----------------------------
def build_llm(settings):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY")

    llm_settings = settings.get("llm", {})
    provider = llm_settings.get("provider", "openrouter")
    model = llm_settings.get("model", "openrouter/auto")

    if provider != "openrouter":
        raise ValueError(f"Unsupported LLM provider: {provider}")

    return OpenRouterClient(
        api_key=api_key,
        model=model
    )


def build_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

    return TelegramNotifier(
        bot_token=token,
        chat_id=chat_id
    )


def build_system():
    load_dotenv()

    settings = load_settings()

    llm = build_llm(settings)
    telegram = build_telegram()
    prompt_builder = PromptBuilder()

    with open("menu.json", "r") as f:
        menu_data = json.load(f)

    business_data = {
        "business": {
            "name": "Deelicious Eats",
            "type": "Cafe / Takeaway",
            "location": "Hinckley",
            "opening_times": {
                "weekdays": "9am - 2pm"
            },
            "reviews": "5 star hygiene rating",
            "hygiene": "Food Standards Agency rated"
        }
    }

    orchestrator = PostOrchestrator(
        menu_data=menu_data,
        business_data=business_data,
        llm_client=llm,
        prompt_builder=prompt_builder
    )

    return orchestrator, telegram


# ----------------------------
# MAIN JOB
# ----------------------------
def run():
    orchestrator, telegram = build_system()

    print("\n==============================")
    print("Generating daily ads")
    print("==============================\n")

    results = orchestrator.generate_posts(3)

    for i, result in enumerate(results, 1):
        ad = clean_post_content(result.get("content", "[NO CONTENT]"))

        print(f"\n--- AD {i} ---\n")
        print(ad)

        telegram.send_message(ad)

    print("\nDone. Sent 3 ads to Telegram.\n")


if __name__ == "__main__":
    run()