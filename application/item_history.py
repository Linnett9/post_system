import json
import os
from datetime import datetime, timedelta


class ItemHistory:
    def __init__(self, path="item_history.json"):
        # Make path stable relative to project root
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.path = os.path.join(base_dir, path)

        self.data = self._load()

    # -------------------------
    # INTERNAL HELPERS
    # -------------------------
    def _key(self, item_name: str) -> str:
        """
        Normalise item names so matching is consistent.
        Prevents casing/spacing mismatches.
        """
        return item_name.strip().lower()

    # -------------------------
    # LOAD / SAVE
    # -------------------------
    def _load(self):
        try:
            if not os.path.exists(self.path):
                return {}

            with open(self.path, "r") as f:
                content = f.read().strip()

                if not content:
                    return {}

                return json.loads(content)

        except json.JSONDecodeError:
            # corrupted file safety fallback
            return {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    # -------------------------
    # PUBLIC API
    # -------------------------
    def is_recent(self, item_name: str, days: int = 14) -> bool:
        key = self._key(item_name)

        if key not in self.data:
            return False

        last_used = datetime.fromisoformat(self.data[key])
        return datetime.now() - last_used < timedelta(days=days)

    def mark_used(self, item_name: str):
        key = self._key(item_name)
        self.data[key] = datetime.now().isoformat()
        self._save()