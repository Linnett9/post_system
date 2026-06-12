import os
import json
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

from infrastructure.llm.openrouter_client import OpenRouterClient
from application.post_orchestrator import PostOrchestrator
from domain.interfaces.prompt_builder import PromptBuilder
from infrastructure.messaging.telegram_notifier import TelegramNotifier


TARGET_HOUR = 8
TARGET_MINUTE = 0


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
# NEXT RUN CALCULATOR
# ----------------------------
def get_next_run_time():
    now = datetime.now()

    next_run = now.replace(
        hour=TARGET_HOUR,
        minute=TARGET_MINUTE,
        second=0,
        microsecond=0
    )

    # if 8am already passed today → schedule tomorrow
    if next_run <= now:
        next_run += timedelta(days=1)

    return next_run


# ----------------------------
# MAIN LOOP (ZERO POLLING)
# ----------------------------
def run():
    orchestrator, telegram = build_system()

    print("\n🚀 Smart scheduler started (sleep-to-8am mode)\n")

    while True:
        try:
            now = datetime.now()
            next_run = get_next_run_time()

            sleep_seconds = (next_run - now).total_seconds()

            print(f"🕒 Now: {now}")
            print(f"⏳ Next run: {next_run}")
            print(f"💤 Sleeping for {int(sleep_seconds)} seconds...\n")

            time.sleep(max(sleep_seconds, 0))

            # ----------------------------
            # RUN DAILY JOB
            # ----------------------------
            print("\n==============================")
            print("🌅 8AM RUN TRIGGERED")
            print("==============================\n")

            results = orchestrator.generate_posts(3)

            for i, result in enumerate(results, 1):
                ad = result.get("content", "[NO CONTENT]")

                print(f"\n--- AD {i} ---\n")
                print(ad)

                telegram.send_message(ad)

        except Exception as e:
            print(f"❌ Scheduler error: {e}")
            time.sleep(60)  # safety fallback


if __name__ == "__main__":
    run()