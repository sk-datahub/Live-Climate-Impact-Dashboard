import pandas as pd
import numpy as np


# --------------------------------------------------
# Load Master Data
# --------------------------------------------------

df = pd.read_csv("climate_master_data.csv")

print("\n🌍 CLIMATE IMPACT ANALYSIS")
print("=" * 80)


# --------------------------------------------------
# Convert numeric columns
# --------------------------------------------------

numeric_columns = [
    "Temperature_C",
    "Feels_Like_C",
    "Humidity_%",
    "Precipitation_mm",
    "Rain_Probability_%",
    "Wind_Speed_kmh",
    "US_AQI",
    "PM2_5",
    "PM10",
    "UV_Index"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# --------------------------------------------------
# Temperature Score - Maximum 30
# --------------------------------------------------

def temperature_score(temp):

    if pd.isna(temp):
        return 0

    if temp <= 25:
        return 0
    elif temp <= 30:
        return 10
    elif temp <= 35:
        return 20
    elif temp <= 40:
        return 25
    else:
        return 30


# --------------------------------------------------
# Humidity Score - Maximum 20
# --------------------------------------------------

def humidity_score(humidity):

    if pd.isna(humidity):
        return 0

    if humidity <= 50:
        return 0
    elif humidity <= 65:
        return 5
    elif humidity <= 75:
        return 10
    elif humidity <= 85:
        return 15
    else:
        return 20


# --------------------------------------------------
# AQI Score - Maximum 30
# --------------------------------------------------

def aqi_score(aqi):

    if pd.isna(aqi):
        return 0

    if aqi <= 50:
        return 0
    elif aqi <= 100:
        return 10
    elif aqi <= 150:
        return 20
    elif aqi <= 200:
        return 25
    else:
        return 30


# --------------------------------------------------
# UV Score - Maximum 20
# --------------------------------------------------

def uv_score(uv):

    if pd.isna(uv):
        return 0

    if uv <= 2:
        return 0
    elif uv <= 5:
        return 5
    elif uv <= 7:
        return 10
    elif uv <= 10:
        return 15
    else:
        return 20


# --------------------------------------------------
# Rain Probability Score - Maximum 15
# --------------------------------------------------

def rain_probability_score(probability):

    if pd.isna(probability):
        return 0

    if probability <= 20:
        return 0
    elif probability <= 40:
        return 5
    elif probability <= 60:
        return 10
    elif probability <= 80:
        return 12
    else:
        return 15


# --------------------------------------------------
# Calculate individual scores
# --------------------------------------------------

df["Temperature_Score"] = df[
    "Temperature_C"
].apply(temperature_score)

df["Humidity_Score"] = df[
    "Humidity_%"
].apply(humidity_score)

df["AQI_Score"] = df[
    "US_AQI"
].apply(aqi_score)

df["UV_Score"] = df[
    "UV_Index"
].apply(uv_score)

df["Rain_Probability_Score"] = df[
    "Rain_Probability_%"
].apply(
    rain_probability_score
)


# --------------------------------------------------
# Calculate Climate Impact Score
# --------------------------------------------------

max_possible_score = 30 + 20 + 30 + 20 + 15

raw_score = (
    df["Temperature_Score"]
    + df["Humidity_Score"]
    + df["AQI_Score"]
    + df["UV_Score"]
    + df["Rain_Probability_Score"]
)

df["Climate_Impact_Score"] = (
    raw_score
    / max_possible_score
    * 100
)

df["Climate_Impact_Score"] = df[
    "Climate_Impact_Score"
].round(1)


# --------------------------------------------------
# Impact Category
# --------------------------------------------------

def impact_category(score):

    if score <= 30:
        return "Low"

    elif score <= 60:
        return "Moderate"

    elif score <= 80:
        return "High"

    else:
        return "Very High"


df["Impact_Category"] = df[
    "Climate_Impact_Score"
].apply(impact_category)


# --------------------------------------------------
# Identify Main Factors
# --------------------------------------------------

def get_factors(row):

    factors = []

    if row["Temperature_Score"] >= 20:
        factors.append("Temperature")

    if row["Humidity_Score"] >= 10:
        factors.append("Humidity")

    if row["AQI_Score"] >= 20:
        factors.append("Air Quality")

    if row["UV_Score"] >= 10:
        factors.append("UV")

    if row["Rain_Probability_Score"] >= 10:
        factors.append("Rain Probability")

    if len(factors) == 0:
        return "No major factors"

    return ", ".join(factors)


df["Main_Impact_Factors"] = df.apply(
    get_factors,
    axis=1
)


# --------------------------------------------------
# Display Results
# --------------------------------------------------

print("\n📊 CITY CLIMATE IMPACT")
print("=" * 100)

result_columns = [
    "City",
    "Temperature_C",
    "Humidity_%",
    "Rain_Probability_%",
    "US_AQI",
    "PM2_5",
    "UV_Index",
    "Climate_Impact_Score",
    "Impact_Category",
    "Main_Impact_Factors"
]

print(
    df[result_columns].to_string(index=False)
)


# --------------------------------------------------
# Save Final Dataset
# --------------------------------------------------

df.to_csv(
    "climate_final_data.csv",
    index=False
)


print("\n")
print("=" * 80)
print("✅ CLIMATE IMPACT ANALYSIS COMPLETE")
print("📁 File created: climate_final_data.csv")
print("=" * 80)