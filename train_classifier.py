import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Step 1: Load data
df = pd.read_csv("/Users/satheeswaranharikrishnan/Desktop/SmartTicket/tickets.csv")

# Step 2: Create pipeline (TF-IDF + Logistic Regression)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# Step 3: Train the model
pipeline.fit(df['query'], df['category'])

# Step 4: Save the model
joblib.dump(pipeline, "model/ticket_classifier.joblib")
print("✅ Model saved at model/ticket_classifier.joblib")
