import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score , classification_report
import joblib

df = pd.read_csv("data/intent_dataset.csv")

X = df['text']
Y = df['label']

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)
print("Train size:", len(X_train))
print("test size:", len(X_test))

vectorizer = TfidfVectorizer()

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Shape after TF-IPF:", X_train_vec.shape)

model = LogisticRegression()
model.fit(X_train_vec, Y_train)

Y_pred = model.predict(X_test_vec)

print("Accuracy:", accuracy_score(Y_test, Y_pred))
print("\nDetailed Report:\n", classification_report(Y_test , Y_pred))

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model and vectorizer saved successfully!")



