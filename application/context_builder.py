from dataclasses import dataclass


@dataclass
class CreativeBrief:
    intent: str
    item: dict
    business: dict
    offer: dict | None


class ContextBuilder:
    def __init__(self, business_data: dict):
        self.business_data = business_data

    def build(self, intent: str, item: dict, offer: dict | None):
        # ✅ Use full business object (not nested ["business"])
        return CreativeBrief(
            intent=intent,
            item=item,
            business=self.business_data,
            offer=offer
        )