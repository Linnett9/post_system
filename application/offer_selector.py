import random


class OfferSelector:
    def __init__(self, business_data: dict):
        self.offers = business_data.get("offers", [])

    def select_offer(self):
        if not self.offers:
            return None

        return random.choice(self.offers)