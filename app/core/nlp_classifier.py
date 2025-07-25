def classify_ticket(query: str) -> str:
    if "payment" in query.lower():
        return "billing"
    elif "error" in query.lower() or "bug" in query.lower():
        return "technical"
    else:
        return "general"
