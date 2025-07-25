# app/core/nlp_classifier.py

import joblib
import os

# Load model only once at module level
model_path = os.path.join(os.path.dirname(__file__), "../../model/ticket_classifier.joblib")
model = joblib.load(model_path)

def classify_ticket(query: str) -> str:
    prediction = model.predict([query])  # Query must be in a list
    return prediction[0]
