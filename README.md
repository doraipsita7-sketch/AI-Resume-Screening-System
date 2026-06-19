# 🤖 AI Resume Screening System

An AI-powered Resume Screening System that automatically analyzes resumes, extracts key skills, and predicts the most suitable job role using Machine Learning and NLP.

---

## 🚀 Features

- 📄 Resume Upload (PDF support)
- 🧠 NLP-based text extraction
- 🔍 Skill extraction from resume
- 🤖 Machine Learning model for job prediction
- 📊 Candidate scoring system
- 💼 Job role matching
- 🗄 Database storage of candidates
- 📈 Clean UI using Streamlit

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 🎨
- Machine Learning 🤖
- NLP (Natural Language Processing)
- Pandas 📊
- SQLite 🗄
- PyPDF2 📄

## 📂 Project Structure

AI-Resume-Screening-System/ │ ├── app.py ├── train_model.py ├── model/ │   ├── model.pkl │   ├── vectorizer.pkl │
├── database/ │   ├── db.py │ ├── dataset/ │   ├── skills.csv │ ├── resume/ ├── utils/ │   ├── extractor.py │ └── README.md

---

## ⚙️ How It Works

1. User uploads resume (PDF)
2. Text is extracted using PyPDF2
3. Skills are extracted using NLP rules
4. ML model predicts job role
5. Scoring system calculates match percentage
6. Result is shown in UI + stored in database

---

## 📊 ML Workflow

- Data Collection
- Data Preprocessing
- Feature Extraction (Skills, Text)
- Model Training
- Model Saved as `.pkl`
- Prediction on new resumes

---

## 🎯 Output Example

- Best Job Role: Python Developer / Data Analyst
- Score: 75%+
- Status: Selected / Rejected

---

## 👨‍💻 Developed By

- Your Name  
- Your Partner Name  

---

## 📌 Note

This project demonstrates real-world application of AI in recruitment automation using NLP and Machine Learning.

---
