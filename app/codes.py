import random

CHARSET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
PREFIX = "IF"


def random_item_code() -> str:
    segment = "".join(random.choice(CHARSET) for _ in range(6))
    return f"{PREFIX}-{segment}"


def normalize_code(raw: str) -> str:
    if not raw or not isinstance(raw, str):
        return ""
    return raw.strip().upper()
