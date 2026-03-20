import json

with open("data/wordlist.json", "r") as f:
    WORDLIST = json.load(f)

def keyword_engine(text: str):
    text = text.lower()

    risk = 0
    reasons = []

    for word in WORDLIST["high_risk"]:
        if word in text:
            risk += 25
            reasons.append(f"High risk keyword: {word}")

    for word in WORDLIST["medium_risk"]:
        if word in text:
            risk += 10
            reasons.append(f"Medium keyword: {word}")

    return risk, reasons