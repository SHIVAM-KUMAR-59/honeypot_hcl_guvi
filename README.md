# 👴 Ramesh: The Agentic Honeypot

An intelligent, multi-layered honeypot system designed to engage scammers through a realistic persona ("Ramesh") while autonomously extracting and reporting fraudulent intelligence (UPI IDs, phishing links, bank details) to security authorities.

---

## 🚀 Overview

This honeypot acts as a **social engineering trap**. It uses high-tier LLMs (Google Gemini) to play the role of a technically confused, polite clerk. While the scammer thinks they are manipulating a victim, a background **Security Analyst Engine** is forensicly analyzing the chat to extract actionable intelligence and trigger automatic reporting when specific criteria are met.

---

## ✨ Key Features

### 1. **The Dual-Agent System**
- **The "Prey" Agent (Ramesh):** A 62-year-old retired clerk from Guwahati. Polite, anxious, and technically slow. He uses "baiting" tactics like asking for text-based UPI IDs when "QR codes won't scan" or reporting "connection timeouts" on phishing links to force scammers into revealing more infrastructure.
- **The "Analyst" Agent:** A background cybersecurity expert that monitors the live transcript. It extracts structured intelligence without the scammer's knowledge.

### 2. **Intelligence Extraction**
Automatically extracts and validates:
- **UPI IDs:** Detects bank-specific VPAs, wallet-based IDs, and generic UPI strings.
- **Phishing Links:** Identifies suspicious domains and harvesting URLs.
- **Bank Details:** captures account numbers and IFSC codes provided in plain text.
- **Tactic Detection:** Monitors for urgency, fear, or impersonation tactics.

### 3. **Automatic Reporting logic**
The system autonomously decides when it has "won" the engagement. It triggers a callback to the GUVI security endpoint only when:
- **Jackpot:** 2+ pieces of concrete intelligence are found.
- **Sufficient Engagement:** 1 intelligence point found + 6+ turns of conversation.
- **Max Safety:** Automatic closure after 8+ turns to conserve resources.

---

## 🛠️ Technology Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **AI Core:** [Google Gemini API](https://aistudio.google.com/) (using models like Gemini 2.0 Flash)
- **Frontend:** Vanilla HTML5, CSS3, and JavaScript
- **Data Validation:** Pydantic
- **Security:** Secret Key Auth & CORS Middleware

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.9+
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the `.env.example` file to `.env` and fill in your keys:
```bash
cp .env.example .env
```

Required variables:
- `GEMINI_API_KEY`: Your Google AI API key.
- `GUVI_CALLBACK_URL`: The target reporting URL.
- `SECRET_API_KEY`: The key Ramesh's UI uses to talk to the backend.

---

## 🏃 How to Run

### 1. Start the Backend
```bash
python -m fastapi dev main.py
```
The server will start at `http://127.0.0.1:8000`.

### 2. Launch the Interface
Simply open `index.html` in any modern web browser.

---

## 🧪 Testing
The project includes audit scripts for payload verification:
- `python test_payload.py`: Validates that the internal data structures meet the reporting requirements.
- `python audit_payload.py`: Performs a schema-level audit of the final JSON callback structure.

---

## 🛡️ Security
This system is designed for **defensive intelligence gathering**.
- **CORS Enabled:** Allows secure local testing.
- **Background Tasks:** Intelligence extraction and reporting do not slow down the AI's response time.
- **Encryption:** All communication is handled via JSON over HTTP.

---
*Created for the GUVI Agentic AI Hackathon.*
