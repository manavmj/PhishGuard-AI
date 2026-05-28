# ============================================================
# 🛡️ PHISHGUARD AI — bot.py
# Advanced Telegram Phishing Detection Bot
#
# FEATURES:
# ✅ OCR Screenshot Analysis
# ✅ ML-based Phishing Detection
# ✅ Rule-based URL Detection
# ✅ Banking Scam Detection
# ✅ Lottery Scam Detection
# ✅ PDF Analysis
# ✅ Professional Cybersecurity Reports
#
# Developed By:
# Manav Jain & Manav Golani
# ============================================================

import os
import re
import joblib
import fitz
import pytesseract
import nltk

from PIL import Image
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from nltk.tokenize import word_tokenize

# ============================================================
# DOWNLOAD NLTK DATA
# ============================================================

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# ============================================================
# TESSERACT OCR PATH
# ============================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ============================================================
# LOAD ENV VARIABLES
# ============================================================

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN missing in .env")

# ============================================================
# LOAD ML MODEL
# ============================================================

MODEL_PATH = os.path.join("model", "phishing_model.pkl")
VECTORIZER_PATH = os.path.join("model", "vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("✅ ML Model Loaded Successfully")

# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    text = text.lower()

    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"www\S+", " ", text)

    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    tokens = word_tokenize(text)

    cleaned = [word for word in tokens if len(word) > 2]

    return " ".join(cleaned)

# ============================================================
# URL EXTRACTION
# ============================================================

def extract_urls(text):

    url_pattern = r"(https?://\S+|www\.\S+)"

    return re.findall(url_pattern, text)

# ============================================================
# ADVANCED RULE-BASED DETECTION
# ============================================================

def advanced_phishing_detection(text):

    text = text.lower()

    phishing_score = 0

    reasons = []

    suspicious_keywords = [
        "kyc",
        "verify",
        "urgent",
        "suspend",
        "blocked",
        "winner",
        "lottery",
        "claim",
        "reward",
        "gift",
        "bank",
        "otp",
        "update account",
        "click here",
        "limited time",
        "expire",
        "prize",
        "aadhaar",
        "pan card",
        "cvv",
        "upi",
    ]

    for word in suspicious_keywords:

        if word in text:
            phishing_score += 12
            reasons.append(f"⚠️ Suspicious keyword detected: {word}")

    suspicious_domains = [
        ".xyz",
        ".top",
        ".click",
        ".shop",
        ".live",
        ".buzz",
    ]

    for domain in suspicious_domains:

        if domain in text:
            phishing_score += 30
            reasons.append(f"🚨 Suspicious domain detected: {domain}")

    brands = [
        "paytm",
        "phonepe",
        "gpay",
        "google pay",
        "sbi",
        "hdfc",
        "icici",
        "axis bank",
    ]

    for brand in brands:

        if brand in text:
            phishing_score += 15
            reasons.append(
                f"🏦 Financial brand impersonation detected: {brand}"
            )

    if "http://" in text:
        phishing_score += 25
        reasons.append("🔓 Non-secure HTTP link detected")

    if len(extract_urls(text)) > 0:
        phishing_score += 15
        reasons.append("🔗 URL detected in message")

    phishing_score = min(phishing_score, 100)

    if phishing_score >= 45:
        return True, phishing_score, reasons

    return False, phishing_score, reasons

# ============================================================
# GENERATE PROFESSIONAL REPORT
# ============================================================

def generate_report(message, verdict, score, reasons):

    if verdict == "PHISHING":

        emoji = "🚨"

        advice = (
            "🚫 DO NOT click links or share OTP/bank details.\n"
            "Block the sender immediately.\n"
            "Report to Cyber Crime at cybercrime.gov.in or call 1930."
        )

    else:

        emoji = "✅"

        advice = (
            "✅ No major phishing indicators detected.\n"
            "Still verify unknown senders before sharing sensitive data."
        )

    reasons_text = ""

    if reasons:

        for reason in reasons:
            reasons_text += f"• {reason}\n"

    else:
        reasons_text = "• No suspicious indicators detected\n"

    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ PHISHGUARD AI — ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 INPUT TYPE: TEXT / SCREENSHOT

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 VERDICT: {verdict} {emoji}
📊 THREAT SCORE: {score}/100
━━━━━━━━━━━━━━━━━━━━━━━━━━

🧩 DETECTED SIGNALS:
{reasons_text}

📝 ANALYZED CONTENT:
{message[:700]}

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ SECURITY ADVICE:
{advice}

📣 REPORT THIS SCAM:
• https://cybercrime.gov.in
• National Cyber Helpline: 1930

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ DISCLAIMER:
This is an AI-assisted phishing detection tool.
Always verify through official sources.
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return report

# ============================================================
# MAIN ANALYSIS ENGINE
# ============================================================

def analyze_message(text):

    # RULE-BASED DETECTION
    is_phishing, rule_score, reasons = (
        advanced_phishing_detection(text)
    )

    # ML DETECTION
    cleaned = clean_text(text)

    vector = vectorizer.transform([cleaned])

    prediction = model.predict(vector)[0]

    probabilities = model.predict_proba(vector)[0]

    ml_confidence = int(max(probabilities) * 100)

    # FINAL DECISION
    if is_phishing:

        verdict = "PHISHING"

        final_score = max(rule_score, ml_confidence)

    else:

        if prediction == 1:

            verdict = "PHISHING"

            final_score = ml_confidence

        else:

            verdict = "SAFE MESSAGE"

            final_score = 100 - ml_confidence

    report = generate_report(
        text,
        verdict,
        final_score,
        reasons
    )

    return report

# ============================================================
# START COMMAND
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = """
🛡️ Welcome to PhishGuard AI

━━━━━━━━━━━━━━━━━━━━
🔐 YOUR PERSONAL CYBERSECURITY ASSISTANT
━━━━━━━━━━━━━━━━━━━━

I can detect:

✅ Phishing Links
✅ Fake Banking Messages
✅ Lottery / Prize Scams
✅ UPI & OTP Fraud
✅ Suspicious Screenshots
✅ Fraudulent PDFs
✅ KYC Scams
✅ Impersonation Attacks

━━━━━━━━━━━━━━━━━━━━
📤 WHAT YOU CAN SEND:
━━━━━━━━━━━━━━━━━━━━

📩 Suspicious SMS
🔗 Unknown URLs
📸 Screenshots
📄 PDF Documents

━━━━━━━━━━━━━━━━━━━━
⚡ HOW IT WORKS:
━━━━━━━━━━━━━━━━━━━━

• OCR extracts text from screenshots
• Machine Learning analyzes content
• Rule-based AI detects phishing patterns
• Generates cybersecurity threat reports

━━━━━━━━━━━━━━━━━━━━
🚀 Send any suspicious message to begin analysis.
━━━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(welcome_message)

# ============================================================
# HELP COMMAND
# ============================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = """
📖 PHISHGUARD AI — USER GUIDE

━━━━━━━━━━━━━━━━━━━━
📩 TEXT ANALYSIS
━━━━━━━━━━━━━━━━━━━━

Paste suspicious messages directly.

Example:
"Your account will be blocked.
Click here to verify KYC."

━━━━━━━━━━━━━━━━━━━━
📸 SCREENSHOT ANALYSIS
━━━━━━━━━━━━━━━━━━━━

Send screenshots as images.

OCR will automatically extract and analyze text.

━━━━━━━━━━━━━━━━━━━━
📄 PDF ANALYSIS
━━━━━━━━━━━━━━━━━━━━

Upload suspicious PDFs.

The bot will scan document text for fraud indicators.

━━━━━━━━━━━━━━━━━━━━
🛡️ DETECTION FEATURES
━━━━━━━━━━━━━━━━━━━━

✅ Fake Banking URLs
✅ Scam Keywords
✅ Urgency Detection
✅ Brand Impersonation
✅ Fraud Domains
✅ Financial Threat Analysis

━━━━━━━━━━━━━━━━━━━━
⚠️ EMERGENCY HELPLINE
━━━━━━━━━━━━━━━━━━━━

Cyber Crime Portal:
https://cybercrime.gov.in

National Helpline:
1930
"""

    await update.message.reply_text(help_text)

# ============================================================
# TEXT HANDLER
# ============================================================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    loading = await update.message.reply_text(
        "🔍 Running cybersecurity analysis..."
    )

    try:

        report = analyze_message(text)

        await loading.delete()

        await update.message.reply_text(report)

    except Exception as e:

        await loading.delete()

        await update.message.reply_text(
            f"⚠️ Analysis Error:\n{str(e)}"
        )

# ============================================================
# IMAGE HANDLER
# ============================================================

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    loading = await update.message.reply_text(
        "📸 Extracting text from screenshot..."
    )

    image_path = "temp_image.jpg"

    try:

        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        await file.download_to_drive(image_path)

        image = Image.open(image_path)

        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():

            await loading.delete()

            await update.message.reply_text(
                "⚠️ No readable text found in image."
            )

            return

        report = analyze_message(extracted_text)

        final_response = (
            f"📄 EXTRACTED TEXT:\n\n"
            f"{extracted_text[:1000]}\n\n"
            f"{report}"
        )

        await loading.delete()

        await update.message.reply_text(final_response)

    except Exception as e:

        await loading.delete()

        await update.message.reply_text(
            f"⚠️ Image Analysis Error:\n{str(e)}"
        )

    finally:

        if os.path.exists(image_path):
            os.remove(image_path)

# ============================================================
# PDF HANDLER
# ============================================================

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    document = update.message.document

    if not document.file_name.endswith(".pdf"):

        await update.message.reply_text(
            "⚠️ Only PDF files are supported."
        )

        return

    loading = await update.message.reply_text(
        "📄 Scanning PDF document..."
    )

    pdf_path = "temp.pdf"

    try:

        file = await context.bot.get_file(document.file_id)

        await file.download_to_drive(pdf_path)

        pdf = fitz.open(pdf_path)

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        if not text.strip():

            await loading.delete()

            await update.message.reply_text(
                "⚠️ No readable text found in PDF."
            )

            return

        report = analyze_message(text)

        await loading.delete()

        await update.message.reply_text(report)

    except Exception as e:

        await loading.delete()

        await update.message.reply_text(
            f"⚠️ PDF Analysis Error:\n{str(e)}"
        )

    finally:

        if os.path.exists(pdf_path):
            os.remove(pdf_path)

# ============================================================
# UNKNOWN HANDLER
# ============================================================

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "⚠️ Unsupported message type."
    )

# ============================================================
# CREATE BOT
# ============================================================

def create_bot():

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_image
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            handle_document
        )
    )

    app.add_handler(
        MessageHandler(
            filters.ALL,
            unknown
        )
    )

    print("✅ PhishGuard AI Bot Initialized Successfully")

    return app