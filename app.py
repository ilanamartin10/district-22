import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

file_path = "District-22-meal-log.xlsx"
df = pd.read_excel(file_path, dtype={"Week Number Served": str})  # Read as string to prevent formatting issues

expected_columns = ["Meal Description", "Protein Type", "Meal Category", "Location Served", "Week Number Served", "EN/FR"]
df.columns = [col.strip() for col in df.columns]  # Remove accidental whitespace

# Check if all expected columns are present
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    st.error(f"Missing columns in Excel: {missing_columns}")
    st.stop()

# Convert "Week Number Served" into an actual datetime object
df["Week Date"] = pd.to_datetime(df["Week Number Served"], format="%Y-%m-%d", errors="coerce")

# Remove rows where Week Date could not be parsed
df = df.dropna(subset=["Week Date"])

# Streamlit UI
st.title("Random Meal Selector")

# Input filters
meal_type = st.selectbox("Select Meal Type", ["All"] + sorted(df["Meal Category"].dropna().unique()), index=0)
protein_type = st.selectbox("Select Protein Type", ["All"] + sorted(df["Protein Type"].dropna().unique()), index=0)
time_difference = st.number_input("Minimum Weeks Since Last Served", min_value=0, step=1, value=0)

# Calculate date threshold
current_date = datetime.today()
date_threshold = current_date - timedelta(weeks=time_difference)

# Debugging: Show what date we're filtering against
st.write(f"Filtering for meals served before: {date_threshold.strftime('%Y-%m-%d')}")

# Apply filters
filtered_df = df.copy()
if meal_type != "All":
    filtered_df = filtered_df[filtered_df["Meal Category"] == meal_type]
if protein_type != "All":
    filtered_df = filtered_df[filtered_df["Protein Type"] == protein_type]
if time_difference > 0:
    filtered_df = filtered_df[filtered_df["Week Date"] < date_threshold]  # Fix: Ensure filtering correctly

# Select a random meal
if not filtered_df.empty:
    selected_meal = filtered_df.sample(1)
    st.subheader("Meal:")
    st.write(selected_meal[["Meal Description", "Protein Type", "Meal Category", "Week Number Served"]])
else:
    st.warning("No meals match the criteria. Try adjusting the filters.")
