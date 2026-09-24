import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Page title
st.title("ExtraaLearn Lead Conversion Predictor App")
st.write(
    "Enter the Lead's details below to predict whether the lead is likely to convert into a Customer."
)

# Collect Lead details
Age = st.selectbox(
    "What is age of Lead?",
    options=range(1, 101)
)

Profile_completed = st.selectbox(
    "How much of the profile did the Lead complete?",
    ["High >75%", "Medium 50-75%", "Low < 50%"]
)
if Profile_completed == "High >75%":
    Profile_completed = 2
elif Profile_completed == "Medium 50-75%":
    Profile_completed = 1
else:  # Handles "Low < 50%" or any other fallback
    Profile_completed = 0


Website_visits = st.number_input(
    "How many times did the Lead visit the website?",
    min_value=0,
    max_value=30
)

Page_views_per_visit = st.number_input(
    "Please specify pages viewed per visit by Lead",
    min_value=0,
    max_value=20
)

Print_media_type1 = st.selectbox(
    "Did Lead see the ad of ExtraaLearn in the Newspaper?",
    ["Yes", "No"]
)
if Print_media_type1 == "Yes":
  Print_media_type1 = 1
else: #Handles "No"
  Print_media_type1 = 0

Print_media_type2 = st.selectbox(
    "Did Lead see the ad of ExtraaLearn in the Magazine?",
    ["Yes", "No"]
)
if Print_media_type2 == "Yes":
  Print_media_type2 = 1
else: #Handles "No"
  Print_media_type2 = 0

Digital_media = st.selectbox(
   "Did Lead see the ad of ExtraaLearn in the digital platform?",
    ["Yes", "No"]
)
if Digital_media == "Yes":
    Digital_media = 1
else:  # Handles "No" or any other fallback
    Digital_media = 0


Educational_channels = st.selectbox(
    "Did Lead hear about ExtraaLearn in the education channels like online forums, discussion threads, educational websites, or others?",
    ["Yes", "No"]
)

if Educational_channels == "Yes":
    Educational_channels = 1
else:  # Handles "No" or any other fallback
    Educational_channels = 0

Referral = st.selectbox(
    "Did Lead hear about ExtraaLearn through a reference?",
    ["Yes", "No"]
)

if Referral == "Yes":
    Referral = 1
else:  # Handles "No" or any other fallback
    Referral = 0

Updated_time_spent_on_web_in_min = st.number_input(
    "Please share total time spent by Lead on website (in minutes)",
    min_value=0,
    max_value=50
)

Current_occupation = st.selectbox(
    "Please select Lead's current occupation?",
    ["Student", "Professional", "Unemployed"]
)

Current_occupation_Student = 0
Current_occupation_Unemployed = 0

if Current_occupation == "Student":
    Current_occupation_Student = 1
    Current_occupation_Unemployed = 0
elif Current_occupation == "Unemployed":
    Current_occupation_Student = 0
    Current_occupation_Unemployed = 1
else:  # Handles "Professional" or any other fallback
    Current_occupation_Student = 0
    Current_occupation_Unemployed = 0


First_interaction = st.selectbox(
    "Lead's First Interaction is through:",
    ["Website", "Mobile App"]
)

First_interaction_Website = 0
if First_interaction == "Website":
    First_interaction_Website = 1
else: # Handles "Mobile App" or any other fallback
    First_interaction_Website = 0


Last_activity = st.selectbox(
    "Lead's Last Activity is through:",
    ["Phone Activity", "Website Activity", "Email Activity"]
)

Last_activity_Phone_Activity = 0
Last_activity_Website_Activity = 0

if Last_activity == "Phone Activity":
    Last_activity_Phone_Activity = 1
    Last_activity_Website_Activity = 0
elif Last_activity == "Website Activity":
    Last_activity_Phone_Activity = 0
    Last_activity_Website_Activity = 1
else:  # Handles "Email Activity" or any other fallback
    Last_activity_Phone_Activity = 0
    Last_activity_Website_Activity = 0


# Create JSON payload
lead_data = {
    "age": Age,
    "profile_completed": Profile_completed,
    "website_visits": Website_visits,
    "page_views_per_visit": Page_views_per_visit,
    "print_media_type1": Print_media_type1,
    "print_media_type2": Print_media_type2,
    "digital_media": Digital_media,
    "educational_channels": Educational_channels,
    "referral": Referral,
    "updated_time_spent_on_web_in_min": Updated_time_spent_on_web_in_min,
    "current_occupation_Student": Current_occupation_Student,
    "current_occupation_Unemployed": Current_occupation_Unemployed,
    "first_interaction_Website": First_interaction_Website,
    "last_activity_Phone Activity": Last_activity_Phone_Activity,
    "last_activity_Website Activity": Last_activity_Website_Activity

}

# Single Prediction
if st.button("Predict", type="primary"):

    response = requests.post(
        f"{BACKEND_URL}/v1/lead",
        json=lead_data
    )

    if response.status_code == 200:
        result = response.json()

        if result["Prediction"] == "Converted":
            st.error("⚠️ The Lead is likely to convert and become a customer.")
        else:
            st.success("✅ The Lead is unlikely to convert and become a customer.")

    else:
        st.error("Unable to connect to the prediction API.")
