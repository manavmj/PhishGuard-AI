# PhishGuard-AI 🔐

### AI-Based Phishing Detection System for Email and Messaging Platforms

PhishGuard-AI is an intelligent phishing detection system that uses **Machine Learning** and **Natural Language Processing (NLP)** to identify malicious messages in emails and messaging platforms.

The project aims to improve cybersecurity awareness by helping users detect phishing attempts before interacting with suspicious content, links, or fraudulent messages.

---

# 🚀 Features

* 🔍 Detects phishing messages using Machine Learning
* 📩 Supports Email and Messaging-style text analysis
* 🧠 NLP-based text preprocessing
* ⚡ Real-time phishing prediction
* 📊 Risk-based classification system
* 🖥️ Dynamic and user-friendly interface
* 📁 Message history storage
* 🔐 Cybersecurity-focused architecture

---

# 🧠 How It Works

```text
User Message Input
        ↓
Text Preprocessing
        ↓
TF-IDF Vectorization
        ↓
Machine Learning Model
        ↓
Risk Analysis
        ↓
Prediction Result
```

The system analyzes textual patterns commonly found in phishing attacks and predicts whether the message is:

* ✅ Safe
* ⚠️ Suspicious
* ❌ Phishing

---

# 🛠️ Tech Stack

| Technology        | Purpose                   |
| ----------------- | ------------------------- |
| Python            | Core Programming Language |
| Flask             | Backend Framework         |
| Scikit-learn      | Machine Learning          |
| NLTK              | NLP & Text Preprocessing  |
| TF-IDF Vectorizer | Feature Extraction        |
| Naive Bayes       | Text Classification       |
| SQLite            | Database Management       |
| HTML/CSS          | Frontend Design           |
| Bootstrap         | Responsive UI             |
| JavaScript        | Dynamic UI Interactions   |
| Git & GitHub      | Version Control           |

---

# 🤖 Machine Learning Workflow

### 1️⃣ Dataset Collection

The dataset contains phishing and legitimate messages labeled for supervised learning.

### 2️⃣ Text Preprocessing

* Lowercasing
* Stopword removal
* Tokenization
* Stemming

### 3️⃣ Feature Extraction

TF-IDF Vectorization converts text into numerical vectors based on word importance.

### 4️⃣ Model Training

A Naive Bayes classifier is trained to identify phishing patterns in messages.

### 5️⃣ Prediction

The trained model predicts whether a message is phishing or legitimate.

---

# 📷 Project Screenshots

## 🏠 Start

<img width="2157" height="1520" alt="Screenshot 2026-04-23 114545" src="https://github.com/user-attachments/assets/dedb9ba3-516d-4516-b810-738913e2937d" />


## 🔍 Message Detection 

<img width="2164" height="1529" alt="Screenshot 2026-04-23 114726" src="https://github.com/user-attachments/assets/6b3ff832-64bf-480b-87f3-185c7e320a8d" />


## ⚠️ Phishing Detection Result

<img width="2162" height="1532" alt="Screenshot 2026-04-23 114752" src="https://github.com/user-attachments/assets/65b15f26-7a4e-4a9e-a535-191ce922c80f" />


---

# 🎯 Why Naive Bayes?

Naive Bayes was selected because:

* It performs efficiently for text classification
* Requires low computational resources
* Provides fast prediction
* Works well with TF-IDF features

---

# 🌍 Social Impact

Phishing attacks are one of the most common cyber threats affecting students, employees, and non-technical users.

PhishGuard-AI helps:

* Prevent online fraud
* Improve cybersecurity awareness
* Reduce chances of credential theft
* Promote safer digital communication

---

# 🔮 Future Scope

* Telegram Bot Integration
* Browser Extension Support
* Real-time URL Scanning
* Multilingual Phishing Detection
* Image-based Phishing Analysis
* Advanced Deep Learning Models

---

# ⚙️ Installation & Setup

## Clone the Repository

```bash
git clone https://github.com/manavmj/PhishGuard-AI.git
cd PhishGuard-AI
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Visit:

```text
http://localhost:5000
```

---

# 📂 Project Structure

```text
PhishGuard-AI/
│
├── app.py
├── model/
├── static/
├── templates/
├── dataset/
├── requirements.txt
└── README.md
```

---

# 👨‍💻 Contributors

* Manav Jain
* Manav Golani

---

# 📜 License

This project is developed for educational and research purposes.

---

# ⭐ Conclusion

PhishGuard-AI demonstrates how Machine Learning and NLP can be applied to solve real-world cybersecurity challenges through intelligent phishing detection and user awareness systems.
