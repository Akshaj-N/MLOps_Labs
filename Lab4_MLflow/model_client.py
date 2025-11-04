import requests
import json
import pandas as pd

# Endpoint URL (adjust port if needed)
url = 'http://127.0.0.1:5001/invocations'

# Prepare sample data
sample_data = {
    "dataframe_split": {
        "columns": ["age", "sex", "cp", "trestbps", "chol", "fbs",
                   "restecg", "thalach", "exang", "oldpeak", "slope",
                   "ca", "thal", "age_group", "chol_risk", "bp_risk",
                   "hr_reserve", "risk_score"],
        "data": [[58, 1, 3, 140, 250, 1, 0, 145, 0, 2.5, 2, 0, 7,
                 2, 1, 0, 17, 18.3]]
    }
}

# Make prediction request
response = requests.post(url, json=sample_data)

# Parse response
if response.status_code == 200:
    predictions = response.json()
    print("Prediction:", predictions)
else:
    print("Error:", response.status_code, response.text)
