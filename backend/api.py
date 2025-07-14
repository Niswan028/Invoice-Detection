import os
import sys
from flask import Flask, request, jsonify
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

ml_path = os.path.join(os.path.dirname(__file__), '..', 'ml', 'predictor.py')
spec = importlib.util.spec_from_file_location("predictor", ml_path)
predictor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(predictor)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Invoice Detection API is running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    required_fields = ['invoice_amount', 'days_late', 'days_to_settle']
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    try:
        prediction = predictor.predict_invoice(data)
        return jsonify({
            "prediction": prediction,
            "meaning": "Disputed" if prediction == 1 else "Not Disputed"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)