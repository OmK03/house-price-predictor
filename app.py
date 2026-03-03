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

CITY_DATA = {
    "San Francisco":    {"longitude": -122.42, "latitude": 37.77, "ocean_proximity": "NEAR BAY"},
    "Oakland":          {"longitude": -122.27, "latitude": 37.80, "ocean_proximity": "NEAR BAY"},
    "San Jose":         {"longitude": -121.89, "latitude": 37.33, "ocean_proximity": "NEAR BAY"},
    "Sacramento":       {"longitude": -121.49, "latitude": 38.58, "ocean_proximity": "INLAND"},
    "Los Angeles":      {"longitude": -118.24, "latitude": 34.05, "ocean_proximity": "<1H OCEAN"},
    "San Diego":        {"longitude": -117.16, "latitude": 32.72, "ocean_proximity": "NEAR OCEAN"},
    "Santa Barbara":    {"longitude": -119.70, "latitude": 34.42, "ocean_proximity": "NEAR OCEAN"},
    "San Luis Obispo":  {"longitude": -120.66, "latitude": 35.28, "ocean_proximity": "NEAR OCEAN"},
    "Fresno":           {"longitude": -119.79, "latitude": 36.74, "ocean_proximity": "INLAND"},
    "Bakersfield":      {"longitude": -119.02, "latitude": 35.37, "ocean_proximity": "INLAND"},
    "Modesto":          {"longitude": -120.99, "latitude": 37.64, "ocean_proximity": "INLAND"},
    "Stockton":         {"longitude": -121.29, "latitude": 37.96, "ocean_proximity": "INLAND"},
    "Redding":          {"longitude": -122.39, "latitude": 40.58, "ocean_proximity": "INLAND"},
    "Santa Rosa":       {"longitude": -122.71, "latitude": 38.44, "ocean_proximity": "<1H OCEAN"},
    "San Rafael":       {"longitude": -122.53, "latitude": 37.97, "ocean_proximity": "NEAR BAY"},
    "Santa Cruz":       {"longitude": -122.03, "latitude": 36.97, "ocean_proximity": "NEAR OCEAN"},
    "Salinas":          {"longitude": -121.65, "latitude": 36.67, "ocean_proximity": "NEAR OCEAN"},
    "Merced":           {"longitude": -120.48, "latitude": 37.30, "ocean_proximity": "INLAND"},
    "Visalia":          {"longitude": -119.29, "latitude": 36.33, "ocean_proximity": "INLAND"},
    "Eureka":           {"longitude": -124.16, "latitude": 40.80, "ocean_proximity": "NEAR OCEAN"},
    "Napa":             {"longitude": -122.29, "latitude": 38.29, "ocean_proximity": "NEAR BAY"},
    "Vallejo":          {"longitude": -122.26, "latitude": 38.10, "ocean_proximity": "NEAR BAY"},
    "Riverside":        {"longitude": -117.37, "latitude": 33.98, "ocean_proximity": "<1H OCEAN"},
    "San Bernardino":   {"longitude": -117.29, "latitude": 34.10, "ocean_proximity": "<1H OCEAN"},
    "Santa Ana":        {"longitude": -117.87, "latitude": 33.74, "ocean_proximity": "<1H OCEAN"},
    "Anaheim":          {"longitude": -117.91, "latitude": 33.83, "ocean_proximity": "<1H OCEAN"},
    "Marysville":       {"longitude": -121.59, "latitude": 39.14, "ocean_proximity": "INLAND"},
    "Yuba City":        {"longitude": -121.62, "latitude": 39.14, "ocean_proximity": "INLAND"},
    "Woodland":         {"longitude": -121.77, "latitude": 38.67, "ocean_proximity": "INLAND"},
    "Fairfield":        {"longitude": -122.04, "latitude": 38.25, "ocean_proximity": "INLAND"},
    "Redwood City":     {"longitude": -122.23, "latitude": 37.48, "ocean_proximity": "NEAR BAY"},
    "Hollister":        {"longitude": -121.40, "latitude": 36.85, "ocean_proximity": "INLAND"},
    "Madera":           {"longitude": -120.06, "latitude": 36.96, "ocean_proximity": "INLAND"},
    "Hanford":          {"longitude": -119.64, "latitude": 36.32, "ocean_proximity": "INLAND"},
    "Crescent City":    {"longitude": -124.20, "latitude": 41.75, "ocean_proximity": "NEAR OCEAN"},
    "Yreka":            {"longitude": -122.63, "latitude": 41.73, "ocean_proximity": "INLAND"},
    "Alturas":          {"longitude": -120.54, "latitude": 41.49, "ocean_proximity": "INLAND"},
    "Susanville":       {"longitude": -120.65, "latitude": 40.41, "ocean_proximity": "INLAND"},
    "Quincy":           {"longitude": -120.94, "latitude": 39.93, "ocean_proximity": "INLAND"},
    "Oroville":         {"longitude": -121.55, "latitude": 39.51, "ocean_proximity": "INLAND"},
    "Ukiah":            {"longitude": -123.21, "latitude": 39.15, "ocean_proximity": "INLAND"},
    "Lakeport":         {"longitude": -122.91, "latitude": 39.04, "ocean_proximity": "INLAND"},
    "Colusa":           {"longitude": -122.01, "latitude": 39.21, "ocean_proximity": "INLAND"},
    "Willows":          {"longitude": -122.19, "latitude": 39.52, "ocean_proximity": "INLAND"},
    "Auburn":           {"longitude": -121.07, "latitude": 38.89, "ocean_proximity": "INLAND"},
    "Placerville":      {"longitude": -120.79, "latitude": 38.72, "ocean_proximity": "INLAND"},
    "Jackson":          {"longitude": -120.77, "latitude": 38.35, "ocean_proximity": "INLAND"},
    "Sonora":           {"longitude": -120.38, "latitude": 37.98, "ocean_proximity": "INLAND"},
    "Bridgeport":       {"longitude": -119.23, "latitude": 38.25, "ocean_proximity": "INLAND"},
    "Independence":     {"longitude": -118.20, "latitude": 36.80, "ocean_proximity": "INLAND"},
    "Mariposa":         {"longitude": -119.96, "latitude": 37.48, "ocean_proximity": "INLAND"},
    "Weaverville":      {"longitude": -122.94, "latitude": 40.73, "ocean_proximity": "INLAND"},
    "Red Bluff":        {"longitude": -122.23, "latitude": 40.17, "ocean_proximity": "INLAND"},
    "Martinez":         {"longitude": -122.13, "latitude": 37.99, "ocean_proximity": "NEAR BAY"},
    "Downieville":      {"longitude": -120.82, "latitude": 39.55, "ocean_proximity": "INLAND"},
    "Nevada City":      {"longitude": -121.01, "latitude": 39.26, "ocean_proximity": "INLAND"},
    "Markleeville":     {"longitude": -119.78, "latitude": 38.69, "ocean_proximity": "INLAND"},
    "San Buenaventura": {"longitude": -119.23, "latitude": 34.27, "ocean_proximity": "NEAR OCEAN"},
    "El Centro":        {"longitude": -115.56, "latitude": 32.79, "ocean_proximity": "INLAND"},
}

RMSE = 50615

@app.route("/")
def home():
    cities = sorted(CITY_DATA.keys())
    city_coords = {city: {"lat": data["latitude"], "lng": data["longitude"]} for city, data in CITY_DATA.items()}
    return render_template("index.html", cities=cities, city_coords=city_coords)

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or pipeline is None:
        return render_template("result.html", prediction="Model not loaded. Run main.py first.", city="", low="", high="", summary={})

    try:
        city = request.form["city"]
        city_info = CITY_DATA[city]

        housing_median_age = float(request.form["housing_median_age"])
        total_rooms        = float(request.form["total_rooms"])
        total_bedrooms     = float(request.form["total_bedrooms"])
        population         = float(request.form["population"])
        households         = float(request.form["households"])
        median_income      = float(request.form["median_income"])

        input_data = pd.DataFrame([{
            "longitude":          city_info["longitude"],
            "latitude":           city_info["latitude"],
            "housing_median_age": housing_median_age,
            "total_rooms":        total_rooms,
            "total_bedrooms":     total_bedrooms,
            "population":         population,
            "households":         households,
            "median_income":      median_income,
            "ocean_proximity":    city_info["ocean_proximity"]
        }])

        if total_bedrooms > total_rooms:
            return render_template("result.html", prediction="Error: Total bedrooms cannot exceed total rooms.", city=city, low="", high="", summary={})

        if households <= 0 or total_rooms <= 0:
            return render_template("result.html", prediction="Error: Households and total rooms must be greater than 0.", city=city, low="", high="", summary={})

        transformed = pipeline.transform(input_data)
        prediction  = model.predict(transformed)[0]

        low    = max(0, prediction - RMSE)
        high   = prediction + RMSE
        result = f"${prediction:,.0f}"
        low    = f"${low:,.0f}"
        high   = f"${high:,.0f}"

        summary = {
            "City":                city,
            "Housing Median Age":  f"{int(housing_median_age)} years",
            "Total Rooms":         int(total_rooms),
            "Total Bedrooms":      int(total_bedrooms),
            "Population":          int(population),
            "Households":          int(households),
            "Median Income":       f"${median_income * 10000:,.0f}",
            "Ocean Proximity":     city_info["ocean_proximity"],
        }

        return render_template("result.html", prediction=result, city=city, low=low, high=high, summary=summary)

    except ValueError:
        return render_template("result.html", prediction="Error: Please enter valid numeric values.", city="", low="", high="", summary={})
    except Exception as e:
        return render_template("result.html", prediction=f"Unexpected error: {str(e)}", city="", low="", high="", summary={})

if __name__ == "__main__":
    app.run(debug=True)