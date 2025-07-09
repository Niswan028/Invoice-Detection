import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from preprocess import load_and_clean

def prepare_features(df):
    """
    Convert date columns to integer timestamps.
    This prepares data for scikit-learn compatibility.
    """
    date_cols = ['invoice_date', 'due_date', 'settled_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce').astype('int64', errors='ignore')
    return df

def train_model():
    # Step 1: Load and preprocess the data
    print("[INFO] Starting data load and preprocessing...")
    df = load_and_clean()
    df = prepare_features(df)

    # Step 2: Split into features and target
    X = df[['invoice_date', 'due_date', 'settled_date']]
    y = df['disputed']

    # Step 3: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Step 4: Initialize and train the model
    print("[INFO] Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 5: Evaluate performance
    print("[INFO] Evaluating model performance:")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    return model

if __name__ == "__main__":
    trained_model = train_model()