from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load trained model and encoders
model = joblib.load("models/random_forest.pkl")
encoders = joblib.load("models/encoders.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Check if file is uploaded
    if "file" not in request.files:
        return "No file uploaded."

    file = request.files["file"]

    if file.filename == "":
        return "Please choose a CSV file."

    try:
        # Read uploaded CSV
        df = pd.read_csv(file)

        # Encode categorical columns
        for col in ["protocol_type", "service", "flag"]:
            if col in df.columns:
                df[col] = encoders[col].transform(df[col])

        # Predict
        predictions = model.predict(df)

        # Count predictions
        attack_count = int((predictions == 1).sum())
        normal_count = int((predictions == 0).sum())

        # Create charts folder
        os.makedirs("static/charts", exist_ok=True)

        # Generate Pie Chart
        plt.figure(figsize=(5, 5))

        plt.pie(
            [normal_count, attack_count],
            labels=["Normal", "Attack"],
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Network Traffic Analysis")

        plt.savefig("static/charts/pie_chart.png")

        plt.close()

        # Show result page
        return render_template(
            "result.html",
            attack=attack_count,
            normal=normal_count
        )

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)