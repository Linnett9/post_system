from datetime import datetime


class IntentEngine:
    def get_intent(self) -> str:
        hour = datetime.now().hour
        weekday = datetime.now().weekday()

        if weekday == 4:
            return "payday_friday"

        if 5 <= hour <= 10:
            return "breakfast_focus"

        if 11 <= hour <= 15:
            return "lunch_craving"

        if 16 <= hour <= 22:
            return "evening_indulgence"

        return "balanced"