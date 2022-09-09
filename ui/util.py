def string_to_bool(value: str) -> bool:
    text = (value or "").lower().strip()
    return text in {"1", "yes", "true", "on", "enabled"}
