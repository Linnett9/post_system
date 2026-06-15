import os
import json
from dotenv import load_dotenv

from infrastructure.llm.openrouter_client import OpenRouterClient
from application.post_orchestrator import PostOrchestrator
from domain.interfaces.prompt_builder import PromptBuilder
from infrastructure.messaging.telegram_notifier import TelegramNotifier


# ----------------------------
# BUILD SYSTEM (same as before)
# ----------------------------
def build_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY")

    return OpenRouterClient(
        api_key=api_key,
        model="deepseek/deepseek-chat"
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

    llm = build_llm()
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
        ad = result.get("content", "[NO CONTENT]")

        print(f"\n--- AD {i} ---\n")
        print(ad)

        telegram.send_message(ad)

    print("\nDone. Sent 3 ads to Telegram.\n")


if __name__ == "__main__":
    run()
