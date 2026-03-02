# House Price Predictor

A machine learning web application that predicts California house prices using the California Housing dataset.

## Tech Stack
- Python
- Scikit-learn (Random Forest Regressor)
- Flask
- HTML & CSS

## Project Structure
```
HousePricePrediction/
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── index.html
│   └── result.html
├── feature_engineering.py
├── main.py
├── app.py
├── requirements.txt
└── README.md
```

## How to Run

1. Clone the repository
2. Install dependencies
3. Train the model
4. Run the Flask app

## Commands
```
pip install -r requirements.txt
python main.py
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Model Performance
- Algorithm: Random Forest Regressor
- Cross Validation RMSE: ~$50,615