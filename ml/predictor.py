import pandas as pd
import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = joblib.load(model_path)

def predict_invoice(data):
    df = pd.DataFrame([data])
    return int(model.predict(df)[0])