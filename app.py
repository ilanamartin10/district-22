import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

file_path = "District-22-meal-log.xlsx"
df = pd.read_excel(file_path)


df.columns = [col.strip() for col in df.columns]
expected_columns = ["Meal Description", "Protein Type", "Meal Category", "Location Served", "Week Served", "EN/FR"]
missing_columns = [col for col in expected_columns if col not in df.columns]
if missing_columns:
    st.error(f"Missing columns in Excel: {missing_columns}")
    st.stop()

# Function to convert a single date string (e.g., '18-Nov') into a datetime object.
def convert_date(date_str, year):
    try:
        return datetime.strptime(date_str.strip(), "%d-%b").replace(year=year)
    except ValueError:
        return None

def get_most_recent_date(date_value):
    # If it's already a datetime, return it directly.
    if isinstance(date_value, datetime):
        return date_value
    # If it's a string, process it.
    if isinstance(date_value, str):
        dates = date_value.splitlines()
        parsed_dates = [convert_date(d, 2024) for d in dates if d.strip()]
        valid_dates = [dt for dt in parsed_dates if dt is not None]
        return max(valid_dates) if valid_dates else None
    # Otherwise, try converting it to string and parse.
    try:
        date_str = str(date_value)
        dates = date_str.splitlines()
        parsed_dates = [convert_date(d, 2024) for d in dates if d.strip()]
        valid_dates = [dt for dt in parsed_dates if dt is not None]
        return max(valid_dates) if valid_dates else None
    except Exception:
        return None

# Streamlit UI
st.title("Random Meal Selector")

# Input filters
meal_type = st.selectbox("Select Meal Type", ["All"] + sorted(df["Meal Category"].dropna().unique()), index=0)
protein_type = st.selectbox("Select Protein Type", ["All"] + sorted(df["Protein Type"].dropna().unique()), index=0)
time_difference = st.number_input("Minimum Weeks Since Last Served", min_value=0, step=1, value=0)

# Calculate date threshold
current_date = datetime.today()
date_threshold = current_date - timedelta(weeks=time_difference)

# Create a new column with the most recent served date
df["Most Recent Served Date"] = df["Week Served"].apply(lambda x: get_most_recent_date(x))

# Apply filters
filtered_df = df.copy()
if meal_type != "All":
    filtered_df = filtered_df[filtered_df["Meal Category"] == meal_type]
if protein_type != "All":
    filtered_df = filtered_df[filtered_df["Protein Type"] == protein_type]
if time_difference > 0:
    filtered_df = filtered_df[filtered_df["Most Recent Served Date"] < date_threshold]

# Select a random meal
if not filtered_df.empty:
    selected_meal = filtered_df.sample(1)
    st.subheader("Meal:")
    st.write(selected_meal[["Meal Description", "Protein Type", "Meal Category", "Week Served"]])
else:
    st.warning("No meals match the criteria. Try adjusting the filters.")
