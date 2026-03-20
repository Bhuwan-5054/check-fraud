from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from analyzer.main_analyzer import analyze
import pytesseract
import io
import re
import json

# load wordlist once (fast)
with open("wordlist.json", "r") as f:
    WORDLIST = json.load(f)
app = FastAPI()

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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# MODELS
class URLRequest(BaseModel):
    url: str

class EmailRequest(BaseModel):
    content: str

class EmailIDRequest(BaseModel):
    email: str


# COMMON ANALYZER
def analyze_text_advanced(text: str):
    text_lower = text.lower()

    risk = 0
    reasons = []
    scam_type = "Unknown"

    # 🔥 PATTERN DETECTION
    if any(word in text_lower for word in ["urgent", "immediately", "act now"]):
        risk += 15
        reasons.append("Urgency pressure detected")

    if any(word in text_lower for word in ["otp", "password", "verify", "login"]):
        risk += 20
        reasons.append("Sensitive info requested")

    if any(word in text_lower for word in ["bank", "account", "payment", "transaction"]):
        risk += 15
        reasons.append("Financial context detected")

    if "click" in text_lower or "link" in text_lower:
        risk += 15
        reasons.append("Action trigger (click link)")

    if any(word in text_lower for word in ["win", "lottery", "prize"]):
        risk += 20
        scam_type = "Lottery Scam"
        reasons.append("Fake reward pattern")

    if any(word in text_lower for word in ["job", "earn", "salary"]):
        risk += 15
        scam_type = "Job Scam"
        reasons.append("Job-related scam pattern")

    if any(word in text_lower for word in ["customer care", "support", "helpline"]):
        risk += 15
        scam_type = "Impersonation Scam"
        reasons.append("Fake support impersonation")

    # 🔥 PHONE DETECTION
    if re.search(r"\\b\\d{10}\\b", text):
        risk += 10
        reasons.append("Phone number detected")

    # 🔥 URL DETECTION
    if "http://" in text_lower or "https://" in text_lower:
        risk += 20
        reasons.append("Suspicious link detected")

    # 🔥 FINAL STATUS
    if risk > 60:
        status = "High Risk ❌"
    elif risk > 30:
        status = "Medium Risk ⚠️"
    else:
        status = "Safe ✅"

    return {
        "status": status,
        "risk": risk,
        "reasons": reasons,
        "scam_type": scam_type
    }

# URL CHECK
@app.post("/check-url")
def check_url(data: URLRequest):
    return analyze(data.url)


# EMAIL CONTENT CHECK
@app.post("/check-email")
def check_email(data: EmailRequest):
    return analyze(data.content)


# EMAIL ID CHECK (NEW 🔥)
@app.post("/check-email-id")
def check_email_id(data: EmailIDRequest):
    email = data.email.lower()
    risk = 0
    reasons = []

    suspicious_domains = ["tempmail", "10minutemail", "fake", "spam"]

    for d in suspicious_domains:
        if d in email:
            risk += 40
            reasons.append(f"Suspicious domain: {d}")

    if re.search(r"\\d{4,}", email):
        risk += 20
        reasons.append("Too many numbers in email")

    if risk > 40:
        status = "High Risk ❌"
    elif risk > 10:
        status = "Medium Risk ⚠️"
    else:
        status = "Safe ✅"

    return {
        "status": status,
        "risk": risk,
        "reasons": reasons
    }


# OCR IMAGE CHECK
@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        text = pytesseract.image_to_string(image)

        if not text.strip():
            return {"status": "No text found", "risk": 0, "reasons": []}

        result = analyze(text)
        result["text"] = text[:500]

        return result

    except Exception as e:
        return {"error": str(e)}


@app.get("/")
def home():
    return {"message": "Backend running 🚀"}