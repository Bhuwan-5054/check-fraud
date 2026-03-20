from analyzer.keyword_engine import keyword_engine
from analyzer.pattern_engine import pattern_engine

def analyze(text: str):
    k_risk, k_reason = keyword_engine(text)
    p_risk, p_reason = pattern_engine(text)

    total_risk = k_risk + p_risk

    if total_risk > 70:
        status = "High Risk ❌"
    elif total_risk > 30:
        status = "Medium Risk ⚠️"
    else:
        status = "Safe ✅"

    return {
        "status": status,
        "risk": total_risk,
        "reasons": k_reason + p_reason
    }