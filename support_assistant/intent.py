def classify_intent(question: str) -> str:
    question = question.lower()

    policy_keywords = [
        "refund",
        "delivery",
        "deliver",
        "cancel",
        "cancellation",
        "payment",
        "pay",
        "return",
        "replacement",
        "replace",
        "account",
        "password",
        "offer",
        "offers",
        "discount"
    ]

    for keyword in policy_keywords:
        if keyword in question:
            return "policy"

    return "general"