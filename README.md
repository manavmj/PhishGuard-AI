# 🛡️ PhishGuard-AI

An AI-powered phishing detection system that helps identify malicious URLs, suspicious websites, and phishing attempts using Machine Learning and Cybersecurity techniques.

## 🚀 Overview

Phishing attacks are one of the most common cybersecurity threats today. **PhishGuard-AI** is designed to detect phishing websites and suspicious links using intelligent machine learning models and feature-based URL analysis.

This project combines:

* 🔍 URL feature extraction
* 🤖 Machine Learning classification
* 🛡️ Cybersecurity heuristics
* 🌐 Web-based phishing analysis

The goal is to provide users with a fast and reliable way to determine whether a website is safe or potentially harmful. Similar phishing detection systems use ML-based URL analysis and heuristic detection for identifying malicious websites. ([PhishGuardAI][1])

---

# ✨ Features

* ✅ Detect phishing URLs in real-time
* ✅ Machine Learning-based prediction system
* ✅ URL feature extraction
* ✅ User-friendly interface
* ✅ Fast and lightweight
* ✅ Cybersecurity-focused detection logic
* ✅ Easy to train and extend with new datasets

---

# 🧠 Tech Stack

## Programming Languages

* Python
* HTML/CSS/JavaScript

## Libraries & Frameworks

* Scikit-learn
* Pandas
* NumPy
* Flask (if backend used)
* Joblib/Pickle

## Machine Learning

* Classification Algorithms
* Feature Engineering
* URL-based phishing detection

---

# 📂 Project Structure

```bash
PhishGuard-AI/
│
├── dataset/               # Dataset files
├── model/                 # Trained ML models
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── app.py                 # Main Flask application
├── train_model.py         # Model training script
├── requirements.txt       # Dependencies
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/manavmj/PhishGuard-AI.git
cd PhishGuard-AI
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Project

```bash
python app.py
```

Open your browser and visit:

```bash
http://127.0.0.1:5000
```

---

# 🧪 How It Works

The system analyzes URLs using multiple phishing indicators such as:

* URL length
* Presence of suspicious characters
* HTTPS usage
* Domain-related patterns
* Redirection behavior
* Keyword analysis

The extracted features are then passed into a trained Machine Learning model that predicts whether the URL is:

* ✅ Legitimate
* ⚠️ Suspicious
* ❌ Phishing

Modern phishing detection systems commonly use ML-based feature extraction and ensemble learning techniques for high detection accuracy. ([phish-guard-ai-lac.vercel.app][2])

---

# 📊 Future Improvements

* 🔹 Browser extension integration
* 🔹 Real-time threat intelligence APIs
* 🔹 Deep Learning models
* 🔹 Email phishing detection
* 🔹 User authentication system
* 🔹 Dashboard analytics

---

# 📸 Screenshots

*Add screenshots of your application here.*

Example:

```md
![Home Page](screenshots/home.png)
![Detection Result](screenshots/result.png)
```

---

# 🤝 Contributing

Contributions are welcome!

## Steps to Contribute

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to your branch

```bash
git push origin feature-name
```




# ⭐ Support

If you like this project:

* 🌟 Star the repository
* 🍴 Fork the project
* 📢 Share it with others

---

# 🔐 Disclaimer

This project is developed for **educational and research purposes only**.
Always use cybersecurity tools ethically and responsibly.
