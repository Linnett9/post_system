from application.context_builder import CreativeBrief


class PromptBuilder:
    """
    Converts structured marketing context into a high-conversion LLM prompt.
    """

    def build(self, brief: CreativeBrief) -> str:
        item = brief.item
        business_root = brief.business
        offer = brief.offer

        # -------------------------
        # Extract structured data safely
        # -------------------------
        business = business_root.get("business", {})
        contact = business_root.get("contact", {})
        trust = business_root.get("trust", {})

        opening_times = business.get("opening_times", {})
        platforms = business.get("platforms", [])

        # -------------------------
        # Offer
        # -------------------------
        offer_text = ""
        if offer:
            offer_text = f"- Offer: {offer['name']} → {offer['description']}"

        # -------------------------
        # Intent rules
        # -------------------------
        intent_rules = self._get_intent_rules(brief.intent)

        # -------------------------
        # Safe formatting (NO placeholders allowed)
        # -------------------------
        name = business.get("name", "Deelicious Eats")
        b_type = business.get("type", "")
        location = business.get("location", "")

        weekdays = opening_times.get("weekdays", "N/A")
        weekends = opening_times.get("weekends", "N/A")

        # IMPORTANT: deterministic formatting
        platform_text = " | ".join(platforms) if platforms else "Just Eat | Uber Eats | Deliveroo"

        reviews = trust.get("reviews", "")
        hygiene = trust.get("hygiene", "")

        phone = contact.get("phone", "")
        email = contact.get("email", "")

        # -------------------------
        # PROMPT
        # -------------------------
        return f"""
You are a senior direct-response food marketing expert.

Your job is to write a Facebook post that generates immediate food orders.

---

BUSINESS CONTEXT
Name: {name}
Type: {b_type}
Location: {location}

Opening Times:
- Weekdays: {weekdays}
- Weekends: {weekends}

Platforms (EXACT - DO NOT MODIFY OR REPHRASE):
{platform_text}

Trust Signals:
- Reviews: {reviews}
- Hygiene: {hygiene}

Contact:
- Phone: {phone}
- Email: {email}

---

PRODUCT
Name: {item.get('name', '')}
Description: {item.get('description', '')}
Category: {item.get('category', '')}
Tags: {", ".join(item.get("tags", []))}

---

{offer_text}

---

INTENT CONTEXT
{brief.intent}

Behaviour Rules:
{intent_rules}

---

COPY REQUIREMENTS

You MUST:
- Start with a strong attention-grabbing hook
- Trigger hunger or craving immediately
- Make it feel local and real (UK takeaway tone)
- Include urgency or scarcity if relevant
- Mention delivery platforms ONLY using the exact Platforms field
- NEVER replace or rewrite Platforms
- NEVER use placeholders like [Location] or [Opening Times]
- NEVER hallucinate missing business data
- Keep under 150 words
- End with a clear CTA

Tone:
- casual
- slightly bold
- appetite-driven
- not corporate

---

OUTPUT FORMAT:
Return ONLY the Facebook post text.
""".strip()

    # -------------------------
    # INTENT RULES
    # -------------------------
    def _get_intent_rules(self, intent: str) -> str:
        rules = {
            "breakfast_focus": """
- Emphasise freshness and morning energy
- Position as the perfect start to the day
- Use words like: fresh, start right, morning fuel
""",

            "lunch_craving": """
- Focus on quick satisfaction
- Emphasise value and convenience
- Use words like: quick bite, fuel up, mid-day fix
""",

            "evening_indulgence": """
- Emphasise indulgence and comfort
- Use rich, heavy food language
- Words like: loaded, dirty, indulgent, proper comfort food
""",

            "payday_friday": """
- Emphasise treating yourself
- Higher emotional tone
- Focus on reward behaviour
""",

            "balanced": """
- Neutral appetite-driven language
- Focus on general craving triggers
"""
        }

        return rules.get(intent, rules["balanced"])