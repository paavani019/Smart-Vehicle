from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

THRESHOLD = 70  # alert if health_score < 70

@app.route("/", methods=["GET"])
def root():
    return jsonify(status="ok", service="Vehicle Health & Maintenance Prediction Service")

@app.route("/maintenance/predict", methods=["POST"])
def predict():
    """
    JSON body:
    {
      "battery_health": 78,
      "engine_temp": 95,
      "oil_pressure": 30,
      "mileage_since_service": 8000
    }
    """
    data = request.get_json(force=True)

    try:
      features = np.array([[
          float(data["battery_health"]),
          float(data["engine_temp"]),
          float(data["oil_pressure"]),
          float(data["mileage_since_service"]),
      ]])
    except Exception as e:
      return jsonify(error=f"Bad payload: {e}"), 400

    score = float(model.predict(features)[0])
    alert = "ALERT" if score < THRESHOLD else "OK"

    return jsonify(
        health_score=round(score, 2),
        status=alert,
        threshold=THRESHOLD
    )

@app.route("/maintenance/report", methods=["POST"])
def report():
    payload = request.get_json(force=True)
    # In a real system, this would be stored to a DB / queue
    return jsonify(message="Report received", echo=payload), 201

if __name__ == "__main__":
    # 0.0.0.0 so you can hit it from other tools; port 8000 is convenient
    app.run(host="0.0.0.0", port=8000)
