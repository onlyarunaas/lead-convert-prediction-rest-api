import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name
app = Flask("ExtraaLearn Lead Conversion Predictor")

# Load the trained churn prediction model
model = joblib.load("ExtraaLearn_LeadConversion_model_v1_0.joblib")
print(model.feature_names_in_)

# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the ExtraaLearn Lead Conversion Predictor API"

# Define an endpoint to predict churn for a single customer
@app.post('/v1/lead')
def predict_conversion():
    # Get JSON data from the request
    lead_data = request.get_json()
    
    # Convert dictionary into DataFrame matching model features
    df = pd.DataFrame(lead_data)

    # Reorder columns to match the exact order expected by the trained model
    df = df[model.feature_names_in_]  # Optional: safety check
        
    # Generate prediction
    prediction = model.predict(df)[0]
    
    # Map prediction result to a human-readable label
    prediction_label = "Converted" if prediction == 1 else "Not_Converted"

    # Return the prediction as a JSON response
    return jsonify({'Prediction': prediction_label})

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
