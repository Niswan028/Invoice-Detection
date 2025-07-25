import pandas as pd
import os

def load_and_clean(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), '..', 'data', 'invoices.csv')

    df = pd.read_csv(path)

    for col in ['invoice_date', 'due_date', 'settled_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    df['invoice_amount'] = df.get('invoice_amount', 0)
    df['days_late'] = (df['settled_date'] - df['due_date']).dt.days.clip(lower=0)
    df['days_to_settle'] = (df['settled_date'] - df['invoice_date']).dt.days.clip(lower=0)

    df.fillna(0, inplace=True)

    if 'disputed' in df.columns:
        df['disputed'] = df['disputed'].astype(str).str.strip().str.capitalize().map({'Yes': 1, 'No': 0}).fillna(0)

    print(f"[INFO] Loaded and cleaned {len(df)} rows from {path}")
    return df