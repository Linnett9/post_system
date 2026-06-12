from application.intent_engine import IntentEngine
from application.menu_selector import MenuSelector
from application.offer_selector import OfferSelector
from application.context_builder import ContextBuilder


class PostOrchestrator:
    def __init__(self, menu_data, business_data, llm_client=None, prompt_builder=None):
        self.intent_engine = IntentEngine()
        self.menu_selector = MenuSelector(menu_data)
        self.offer_selector = OfferSelector(business_data)
        self.context_builder = ContextBuilder(business_data)

        self.llm_client = llm_client
        self.prompt_builder = prompt_builder

    # -----------------------------------
    # SINGLE POST (existing behaviour)
    # -----------------------------------
    def generate_post(self):
        intent = self.intent_engine.get_intent()
        item = self.menu_selector.select_item(intent)
        offer = self.offer_selector.select_offer()

        brief = self.context_builder.build(intent, item, offer)

        if self.prompt_builder and self.llm_client:
            prompt = self.prompt_builder.build(brief)
            content = self.llm_client.generate(prompt)
        else:
            content = f"[MOCK POST]\n{brief.item['name']} - {brief.intent}"

        return {
            "title": brief.item["name"],
            "intent": brief.intent,
            "content": content
        }

    # -----------------------------------
    # BATCH POSTS (NEW)
    # -----------------------------------
    def generate_posts(self, count: int = 3):
        posts = []

        for _ in range(count):
            intent = self.intent_engine.get_intent()
            item = self.menu_selector.select_item(intent)
            offer = self.offer_selector.select_offer()

            brief = self.context_builder.build(intent, item, offer)

            if self.prompt_builder and self.llm_client:
                prompt = self.prompt_builder.build(brief)
                content = self.llm_client.generate(prompt)
            else:
                content = f"[MOCK POST]\n{brief.item['name']} - {brief.intent}"

            posts.append({
                "title": brief.item["name"],
                "intent": brief.intent,
                "content": content
            })

        return posts