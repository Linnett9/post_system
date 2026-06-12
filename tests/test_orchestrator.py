import pytest
from application.post_orchestrator import PostOrchestrator


# ----------------------------
# FIXTURES
# ----------------------------

@pytest.fixture
def sample_menu():
    return {
        "menu": {
            "burgers": [
                {
                    "name": "Dirty Smash",
                    "description": "2 patties, bacon, cheese, fries",
                    "tags": ["best_seller", "premium"],
                    "tier": 1
                },
                {
                    "name": "Cheese Burger",
                    "description": "beef patty, cheese",
                    "tags": [],
                    "tier": 2
                }
            ],
            "breakfast": [
                {
                    "name": "Full English",
                    "description": "bacon, sausage, eggs",
                    "tags": ["breakfast"],
                    "tier": 2
                }
            ]
        }
    }


@pytest.fixture
def sample_business():
    return {
        "business": {
            "name": "Deelicous Eats",
            "type": "cafe",
            "location": "Hinckley",
            "opening_times": {"weekdays": "9am-2pm"}
        },
        "offers": [
            {
                "name": "Tuesday Deal",
                "description": "20% off"
            }
        ],
        "trust": {
            "reviews": "5 star reviews",
            "hygiene": "5 star hygiene"
        }
    }


@pytest.fixture
def orchestrator(sample_menu, sample_business):
    return PostOrchestrator(
        menu_data=sample_menu,
        business_data=sample_business,
        llm_client=None  # mock mode
    )


# ----------------------------
# TEST 1: Intent generation is valid
# ----------------------------

def test_intent_is_valid(orchestrator):
    intent = orchestrator.get_intent()

    valid = {
        "breakfast_focus",
        "lunch_craving",
        "evening_indulgence",
        "payday_friday",
        "balanced"
    }

    assert intent in valid


# ----------------------------
# TEST 2: Menu flattening works
# ----------------------------

def test_flatten_menu(orchestrator):
    items = orchestrator.flatten_menu()

    assert isinstance(items, list)
    assert len(items) == 3

    names = [i["name"] for i in items]
    assert "Dirty Smash" in names
    assert "Full English" in names


# ----------------------------
# TEST 3: Item selection returns valid item
# ----------------------------

def test_select_item_returns_valid(orchestrator):
    item = orchestrator.select_item("evening_indulgence")

    assert "name" in item
    assert "description" in item
    assert "tier" in item


# ----------------------------
# TEST 4: Prompt builder contains key info
# ----------------------------

def test_prompt_contains_business_and_item(orchestrator):
    item = orchestrator.select_item("evening_indulgence")
    brief = orchestrator.build_brief("evening_indulgence", item)
    prompt = orchestrator.build_prompt(brief)

    assert "Deelicous Eats" in prompt
    assert item["name"] in prompt
    assert "Task:" in prompt


# ----------------------------
# TEST 5: Mock LLM fallback works
# ----------------------------

def test_llm_fallback(orchestrator):
    output = orchestrator.generate_with_llm("test prompt")

    assert isinstance(output, str)
    assert len(output) > 0


# ----------------------------
# TEST 6: Full pipeline runs
# ----------------------------

def test_generate_post_pipeline(orchestrator):
    post = orchestrator.generate_post()

    assert post.title is not None
    assert post.intent is not None
    assert post.content is not None
    assert isinstance(post.timestamp, str)