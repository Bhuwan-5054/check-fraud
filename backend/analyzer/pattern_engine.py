import re

def pattern_engine(text: str):
    text = text.lower()

    risk = 0
    reasons = []

    if "http" in text:
        risk += 20
        reasons.append("Link detected")

    if re.search(r"\d{10}", text):
        risk += 10
        reasons.append("Phone number detected")

    return risk, reasons