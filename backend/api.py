import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load ML predictor
ml_path = os.path.join(os.path.dirname(__file__), '..', 'ml', 'predictor.py')
spec = importlib.util.spec_from_file_location("predictor", ml_path)
predictor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(predictor)

# Load PDF extractor
extract_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'extract_invoice.py')
spec2 = importlib.util.spec_from_file_location("extract_invoice", extract_path)
extract_invoice = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(extract_invoice)

app = Flask(__name__)
CORS(app)

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

@app.route("/predict-pdf", methods=["POST"])
def predict_from_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join("data", file.filename)
    file.save(save_path)

    try:
        parsed_data = extract_invoice.extract_invoice_fields(save_path)

        if len(parsed_data) != 3:
            return jsonify({"error": "Failed to extract all required fields from PDF"}), 422

        prediction = predictor.predict_invoice(parsed_data)

        return jsonify({
            "extracted": parsed_data,
            "prediction": prediction,
            "meaning": "Disputed" if prediction == 1 else "Not Disputed"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
