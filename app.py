import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Load Data
data = "District-22-meal-log.xlsx"

df = pd.DataFrame(data, columns=["Meal Description", "Protein Type", "Meal Category", "Location Served", "Week Number Served", "EN/FR"])

# Convert "Week Number Served" to a datetime format for filtering by time difference
week_mapping = {
    "Week of Dec 9": datetime(2024, 12, 9),
    "Week of Dec 2": datetime(2024, 12, 2),
    "Week of Nov 25": datetime(2024, 11, 25),
    "Week of Nov 18": datetime(2024, 11, 18),
}
df["Week Date"] = df["Week Number Served"].map(week_mapping)

# Streamlit UI
st.title("Random Meal Selector")

# Input filters
meal_type = st.selectbox("Select Meal Type", ["All"] + sorted(df["Meal Category"].unique()), index=0)
protein_type = st.selectbox("Select Protein Type", ["All"] + sorted(df["Protein Type"].unique()), index=0)
time_difference = st.number_input("Minimum Weeks Since Last Served", min_value=0, step=1, value=0)

# Calculate date threshold
current_date = datetime.today()
date_threshold = current_date - timedelta(weeks=time_difference)

# Apply filters
filtered_df = df.copy()
if meal_type != "All":
    filtered_df = filtered_df[filtered_df["Meal Category"] == meal_type]
if protein_type != "All":
    filtered_df = filtered_df[filtered_df["Protein Type"] == protein_type]
if time_difference > 0:
    filtered_df = filtered_df[filtered_df["Week Date"] <= date_threshold]

# Select a random meal
if not filtered_df.empty:
    selected_meal = filtered_df.sample(1)
    st.subheader("Your Random Meal:")
    st.write(selected_meal[["Meal Description", "Protein Type", "Meal Category", "Week Number Served"]])
else:
    st.warning("No meals match the criteria. Try adjusting the filters.")

