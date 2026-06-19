import pickle

# ================= LOAD MODEL =================
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# ================= PREDICT FUNCTION =================
def predict_job(text):

    # Empty check
    if not text or len(text.strip()) < 20:
        return "No Relevant Skills Found"

    try:
        # Convert text to vector
        text_vector = vectorizer.transform([text])

        # Prediction
        prediction = model.predict(text_vector)[0]

        # ================= SAFETY FIX =================
        # Avoid unwanted categories for demo/project
        if prediction in ["Consultant", "Arts", "BPO", "Agriculture"]:
            prediction = "Software / IT Related"

        return prediction

    except Exception as e:
        print("Prediction Error:", e)
        return "Prediction Failed"