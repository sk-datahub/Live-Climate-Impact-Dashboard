import pandas as pd
import mysql.connector


# ---------------------------------------------
# 1. Load final climate data
# ---------------------------------------------

df = pd.read_csv("climate_final_data.csv")

print("📂 Final climate data loaded!")
print("Rows:", len(df))


# ---------------------------------------------
# 2. Connect to MySQL
# ---------------------------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="969950",
    database="climate_dashboard"
)

cursor = connection.cursor()

print("✅ MySQL connected successfully!")


# ---------------------------------------------
# 3. Insert Query
# ---------------------------------------------

insert_query = """
INSERT IGNORE INTO climate_analysis  (
    City,
    State,
    Country,
    Latitude,
    Longitude,
    Timestamp,
    Temperature_C,
    Feels_Like_C,
    Humidity_Percent,
    Precipitation_mm,
    Rain_Probability_Percent,
    Wind_Speed_kmh,
    Pressure_hPa,
    Weather_Code,
    US_AQI,
    PM2_5,
    PM10,
    CO,
    NO2,
    SO2,
    O3,
    UV_Index,
    Temperature_Score,
    Humidity_Score,
    AQI_Score,
    UV_Score,
    Rain_Probability_Score,
    Climate_Impact_Score,
    Impact_Category,
    Main_Impact_Factors
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""


# ---------------------------------------------
# 4. Handle missing values
# ---------------------------------------------
# Convert NaN values to MySQL NULL
df = df.astype(object).where(pd.notnull(df), None)
# Check remaining missing values
print("\n🔍 Missing values after cleaning:")

print(
    df.isnull().sum()
)


# ---------------------------------------------
# 5. Prepare records
# ---------------------------------------------

records = []

for _, row in df.iterrows():

    records.append((
        row["City"],
        row["State"],
        row["Country"],
        row["Latitude"],
        row["Longitude"],
        row["Timestamp"],
        row["Temperature_C"],
        row["Feels_Like_C"],
        row["Humidity_%"],
        row["Precipitation_mm"],
        row["Rain_Probability_%"],
        row["Wind_Speed_kmh"],
        row["Pressure_hPa"],
        row["Weather_Code"],
        row["US_AQI"],
        row["PM2_5"],
        row["PM10"],
        row["CO"],
        row["NO2"],
        row["SO2"],
        row["O3"],
        row["UV_Index"],
        row["Temperature_Score"],
        row["Humidity_Score"],
        row["AQI_Score"],
        row["UV_Score"],
        row["Rain_Probability_Score"],
        row["Climate_Impact_Score"],
        row["Impact_Category"],
        row["Main_Impact_Factors"]
    ))


# ---------------------------------------------
# 6. Insert into MySQL
# ---------------------------------------------

cursor.executemany(
    insert_query,
    records
)

connection.commit()

print(f"✅ {cursor.rowcount} records inserted into MySQL!")


# ---------------------------------------------
# 7. Close connection
# ---------------------------------------------

cursor.close()
connection.close()

print("🔒 MySQL connection closed.")
print("🎉 Data loading completed successfully!")