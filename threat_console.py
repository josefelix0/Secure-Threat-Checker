# threat_console.py
# Simple console to test the threat model.

from pathlib import Path
import joblib

model_path = Path("models") / "threat_model.joblib"

if not model_path.exists():
    print("Model file not found. Run train_threat_model.py first.")
    raise SystemExit(1)

print("Loading model...")
model = joblib.load(model_path)
print("Model loaded.")

print("\nSecure Cyber Threat Console")
print("Type a line of text to analyze.")
print("Type 'quit' to exit.\n")

while True:
    text = input("Enter message: ").strip()
    if text.lower() == "quit":
        print("Goodbye.")
        break

    if not text:
        print("Please enter some text.")
        continue

    # The model expects a list as input.
    label = model.predict([text])[0]

    print(f"Predicted label: {label}")
    print("-" * 40)
