import joblib

# Saved model and vectorizer loading
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def classify_message(text):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)
    return prediction[0]

if __name__ == "__main__":
    test_messages = [
        "hi there",
        "bye see you later",
        "what is a neural network",
        "remind me to call mom",
        "that was really helpful",
        "how are you doing",
        "do you remember what i told you",
        "who made you",
        "thank you so much",
        "that's not what i meant",
        "this is not working properly",
        "help me fix this code",
        "how's the weather today",
    ]
    for msg in test_messages:
        print(msg, "->", classify_message(msg))