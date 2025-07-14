import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from preprocess import load_and_clean

def train_model():
    print("[INFO] Loading and preparing data...")
    df = load_and_clean()

    X = df[['invoice_amount', 'days_late', 'days_to_settle']]
    y = df['disputed']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("[INFO] Training Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print("[INFO] Model Evaluation:")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(model, 'ml/model.pkl')
    print("Model saved successfully to ml/model.pkl")
if __name__ == "__main__":
    train_model()