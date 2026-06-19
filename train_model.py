from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
import os

# Load Dataset
df = pd.read_csv("dataset/archive (2)/Resume/Resume.csv")

# Professional Job Names
category_map = {
    "INFORMATION-TECHNOLOGY": "Software Developer",
    "ENGINEERING": "Software Engineer",
    "FINANCE": "Data Analyst",
    "BANKING": "Business Analyst",
    "BUSINESS-DEVELOPMENT": "Business Development Executive",
    "HR": "HR Executive",
    "DIGITAL-MEDIA": "Digital Marketing Specialist",
    "CONSULTANT": "Consultant",
    "TEACHER": "Teacher",
    "ARTS": "Creative Artist"
}

df["Category"] = df["Category"].replace(category_map)

# Features and Labels
X = df["Resume_str"]
y = df["Category"]

# TF-IDF
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=8000,
    ngram_range=(1,2)
)

X_vectorized = vectorizer.fit_transform(X)

# Train Model
model = LogisticRegression(max_iter=1000)
model.fit(X_vectorized, y)

# Create Model Folder
if not os.path.exists("model"):
    os.makedirs("model")

# Save Model
pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("✅ Model trained successfully!")
print("📊 Categories:", len(df["Category"].unique()))
print("📄 Total Resumes:", len(df))

print(df["Category"].unique())