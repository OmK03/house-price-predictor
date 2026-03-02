import joblib
import pandas as pd
from flask import Flask, request, render_template
from feature_engineering import FeatureEngineering

app = Flask(__name__)

try:
    model = joblib.load("model.pkl")
    pipeline = joblib.load("pipeline.pkl")
except FileNotFoundError:
    model = None
    pipeline = None
    print("Warning: model.pkl or pipeline.pkl not found. Run main.py first.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or pipeline is None:
        return render_template("result.html", prediction="Model not loaded. Run main.py first.")

    try:
        input_data = pd.DataFrame([{
            "longitude":          float(request.form["longitude"]),
            "latitude":           float(request.form["latitude"]),
            "housing_median_age": float(request.form["housing_median_age"]),
            "total_rooms":        float(request.form["total_rooms"]),
            "total_bedrooms":     float(request.form["total_bedrooms"]),
            "population":         float(request.form["population"]),
            "households":         float(request.form["households"]),
            "median_income":      float(request.form["median_income"]),
            "ocean_proximity":    request.form["ocean_proximity"]
        }])

        if input_data["total_bedrooms"][0] > input_data["total_rooms"][0]:
            return render_template("result.html", prediction="Error: Total bedrooms cannot exceed total rooms.")

        if input_data["households"][0] <= 0 or input_data["total_rooms"][0] <= 0:
            return render_template("result.html", prediction="Error: Households and total rooms must be greater than 0.")

        transformed = pipeline.transform(input_data)
        prediction = model.predict(transformed)[0]
        result = f"${prediction:,.2f}"
        return render_template("result.html", prediction=result)

    except ValueError:
        return render_template("result.html", prediction="Error: Please enter valid numeric values.")
    except Exception as e:
        return render_template("result.html", prediction=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
