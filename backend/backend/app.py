from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
DATA_PATH = "latest.csv"

@app.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    file.save(DATA_PATH)
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route("/kpis", methods=["GET"])
def get_kpis():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": "No data uploaded yet"}), 404
        df = pd.read_csv(DATA_PATH)
        kpis = {
            "total_weight": df["weight"].sum(),
            "truck_count": df["truck_id"].nunique(),
            "avg_load": df["weight"].mean()
        }
        return jsonify(kpis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
