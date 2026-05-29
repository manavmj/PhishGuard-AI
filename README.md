# 🛡️ PhishGuard AI

## Hybrid Cybersecurity Phishing Detection System

PhishGuard AI is an advanced cybersecurity-focused Telegram bot designed to detect phishing attacks, banking scams, malicious URLs, fake KYC messages, lottery frauds, and suspicious screenshots using a hybrid detection architecture.

The system combines:

* 🤖 Machine Learning
* 🔍 Rule-Based Threat Intelligence
* 📸 OCR Screenshot Analysis
* 📄 PDF Scam Detection

to generate professional cybersecurity threat reports in real time.

---

# 🚀 Features

✅ Phishing URL Detection
✅ Banking Scam Detection
✅ KYC Fraud Detection
✅ OTP & UPI Scam Detection
✅ Screenshot OCR Analysis
✅ PDF Scam Analysis
✅ Threat Score Generation
✅ Financial Brand Impersonation Detection
✅ Telegram Bot Integration
✅ Real-Time Cybersecurity Reports

---

# 🧠 Hybrid Detection Architecture

PhishGuard AI uses a hybrid cybersecurity architecture instead of relying only on AI APIs.

```text
User Input
   ↓
OCR Text Extraction
   ↓
Text Preprocessing
   ↓
Rule-Based Threat Detection
   ↓
Machine Learning Classification
   ↓
Threat Score Calculation
   ↓
Cybersecurity Report Generation
```

---

# 🔍 Detection Techniques Used

## 1️⃣ Machine Learning Detection

The system uses:

* Logistic Regression
* TF-IDF Vectorization
* NLP Text Processing

to classify messages into:

* ✅ Safe
* 🚨 Phishing

---

## 2️⃣ Rule-Based Threat Intelligence

The system detects:

* Suspicious keywords
* Fake KYC requests
* Banking impersonation
* Fraud domains (`.xyz`, `.top`, `.click`)
* HTTP links
* Lottery scam patterns
* OTP/CVV/PAN requests

---

## 3️⃣ OCR Screenshot Analysis

Using Tesseract OCR, the bot extracts text from screenshots and analyzes phishing content automatically.

Example:

```text
"Your account will be blocked.
Verify KYC immediately."
```

---

## 4️⃣ PDF Scam Detection

The bot scans PDF documents and extracts suspicious content using PyMuPDF.

---

# 🛠️ Tech Stack

## Backend

* Python

## Machine Learning

* scikit-learn
* NLTK
* joblib

## OCR & Image Processing

* Tesseract OCR
* pytesseract
* Pillow

## PDF Processing

* PyMuPDF

## Bot Framework

* python-telegram-bot

---

# 📂 Project Structure

```text
telegram_phishing_bot/
│
├── bot.py
├── main.py
├── .env
├── requirements.txt
│
├── model/
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
└── screenshots/
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/manavmj/PhishGuard-AI.git
cd PhishGuard-AI
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Install Tesseract OCR

Download:

```text
https://github.com/UB-Mannheim/tesseract/wiki
```

Install and update path inside `bot.py`:

```python
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
```

---

## 4️⃣ Create `.env`

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

---

## 5️⃣ Run the Bot

```bash
python main.py
```

---

# 📸 Supported Inputs

| Input Type    | Supported |
| ------------- | --------- |
| Text Messages | ✅         |
| URLs          | ✅         |
| Screenshots   | ✅         |
| PDFs          | ✅         |

---

# 📊 Example Detection Report

```text
🛡️ PHISHGUARD AI — ANALYSIS REPORT

🔍 VERDICT: PHISHING 🚨
📊 THREAT SCORE: 92/100

🧩 DETECTED SIGNALS:
• Suspicious domain detected
• Banking impersonation detected
• Urgency language detected

⚡ SECURITY ADVICE:
Do not click links or share OTP/bank details.
```

---

# 🎯 Real-World Use Cases

* Banking Scam Detection
* Fake KYC Alerts
* UPI Fraud Detection
* Telegram Scam Detection
* Screenshot Scam Analysis
* Fraudulent PDF Identification

---

# 🌍 Social Impact

PhishGuard AI aims to improve cybersecurity awareness and help users identify phishing attacks and online scams in real time.

The project focuses on protecting users from:

* Financial fraud
* Banking scams
* Identity theft
* OTP scams
* Fake reward scams

---

# 🔮 Future Scope

* WhatsApp Integration
* Browser Extension
* Android Application
* Real-Time SMS Detection
* Voice Phishing Detection
* Deep Learning Models
* Multilingual Scam Detection

---
# screenshots:
<img width="2157" height="1520" alt="Screenshot 2026-04-23 114545" src="https://github.com/user-attachments/assets/56e4d68f-3b2b-46a0-8872-57679066f9c7" />

<img width="2164" height="1529" alt="Screenshot 2026-04-23 114726" src="https://github.com/user-attachments/assets/9079b120-ac53-4ae7-a3a6-1416497f2894" />

<img width="2162" height="1532" alt="Screenshot 2026-04-23 114752" src="https://github.com/user-attachments/assets/07772352-de46-4dcd-9ac0-684322726ef8" />




# 👨‍💻 Developed By

Manav Jain & Manav Golani

---

# ⚠️ Disclaimer

This project is developed for educational and cybersecurity awareness purposes.

The generated analysis is advisory and should not replace official cybersecurity verification procedures.
