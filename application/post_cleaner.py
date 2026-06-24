DOUBLE_QUOTES = ('"', "\u201c", "\u201d")
WRAPPING_QUOTES = ("'", "\u2018", "\u2019")


def clean_post_content(content: str) -> str:
    cleaned = content.replace('\\"', "").replace("*", "")

    for quote in DOUBLE_QUOTES:
        cleaned = cleaned.replace(quote, "")

    cleaned = "\n".join(" ".join(line.split()) for line in cleaned.splitlines()).strip()

    while cleaned and cleaned[0] in WRAPPING_QUOTES:
        cleaned = cleaned[1:].strip()

    while cleaned and cleaned[-1] in WRAPPING_QUOTES:
        cleaned = cleaned[:-1].strip()

    return "\n".join(" ".join(line.split()) for line in cleaned.splitlines()).strip()
