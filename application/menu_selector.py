import random
from application.item_history import ItemHistory


class MenuSelector:
    def __init__(self, menu_data: dict):
        self.menu_data = menu_data
        self.history = ItemHistory()  # ✅ persistent reuse tracking

    def flatten_menu(self):
        items = []
        for category, category_items in self.menu_data["menu"].items():
            for item in category_items:
                item = item.copy()
                item["category"] = category
                items.append(item)
        return items

    def select_item(self, intent: str):
        items = self.flatten_menu()

        # -------------------------------------------------
        # 1. FILTER OUT RECENT ITEMS (14-day lock)
        # -------------------------------------------------
        available_items = [
            item for item in items
            if not self.history.is_recent(item["name"], days=14)
        ]

        # fallback if everything has been used recently
        if not available_items:
            available_items = items

        # -------------------------------------------------
        # 2. SCORING SYSTEM (unchanged logic)
        # -------------------------------------------------
        def score(item):
            score = 0

            tier = item.get("tier", 3)
            score += {1: 120, 2: 70, 3: 30}.get(tier, 30)

            tags = item.get("tags", [])

            if intent == "breakfast_focus" and "breakfast" in tags:
                score += 100

            if intent == "evening_indulgence" and item["category"] in [
                "burgers", "smashed_burgers", "chicken_burgers"
            ]:
                score += 80

            if "best_seller" in tags:
                score += 60

            return score

        scored = [(score(i), i) for i in available_items]
        scored.sort(key=lambda x: x[0], reverse=True)

        # top candidates
        top = scored[:8]

        selected = random.choice(top)[1]

        # -------------------------------------------------
        # 3. MARK AS USED (CRITICAL)
        # -------------------------------------------------
        self.history.mark_used(selected["name"])

        return selected