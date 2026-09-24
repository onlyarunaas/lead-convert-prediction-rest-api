import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name
app = Flask("ExtraaLearn Lead Conversion Predictor")

# Load the trained churn prediction model
model = joblib.load("ExtraaLearn_LeadConversion_model_v1_0.joblib")

# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the ExtraaLearn Lead Conversion Predictor API"

# Define an endpoint to predict churn for a single customer
@app.post('/v1/lead')
def predict_conversion():
    # Get JSON data from the request
    lead_data = request.get_json()

    # Extract relevant customer features from the input data
    sample = {
        'Age': lead_data['age'],
        'Profile_completed': lead_data['profile_completed'],
        'Website_visits': lead_data['website_visits'],
        'Page_views_per_visit': lead_data['page_views_per_visit'],
        'Print_media_type1': lead_data['print_media_type1'],
        'Print_media_type2': lead_data['print_media_type2'],
        'Digital_media': lead_data['digital_media'],
        'Educational_channels': lead_data['educational_channels'],
        'Referral': lead_data['referral'],
        'Updated_time_spent_on_web_in_min': lead_data['updated_time_spent_on_web_in_min'],
        'Current_occupation_Student': lead_data['current_occupation_Student'],
        'Current_occupation_Unemployed': lead_data['current_occupation_Unemployed'],
        'First_interaction_Website': lead_data['first_interaction_Website'],
        'Last_activity_Phone Activity': lead_data['last_activity_Phone Activity'],
        'Last_activity_Website Activity': lead_data['last_activity_Website Activity']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a Lead prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Map prediction result to a human-readable label
    prediction_label = "Lead Converted to Customer" if prediction == 1 else "Lead Not Converted to Customer"

    # Return the prediction as a JSON response
    return jsonify({'Prediction': prediction_label})

'''# Define an endpoint to predict churn for a batch of customers
@app.post('/v1/Leadbatch')
def predict_lead_batch_conversion():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data and convert raw predictions into a readable format
    predictions = [
        'Lead Converted' if x == 1
        else "Lead Not Converted"
        for x in model.predict(input_data.drop("customerID",axis=1)).tolist()
    ]

    lead_id_list = input_data.customerID.values.tolist()
    output_dict = dict(zip(lead_id_list, predictions))

    return output_dict'''

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
