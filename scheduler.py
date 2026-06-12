import time
from main import run


INTERVAL_SECONDS = 30  # for testing


def scheduler_loop():
    print("🚀 Scheduler started (30s interval)")

    while True:
        try:
            print("\n==============================")
            print("🔁 Generating new ad...")
            print("==============================\n")

            run()

        except Exception as e:
            print(f"❌ Error during run: {e}")

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    scheduler_loop()