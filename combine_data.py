import pandas as pd
import os


# ==================================================
# 1. LOAD CURRENT WEATHER DATA
# ==================================================

weather = pd.read_csv("live_weather_data.csv")

print("\n🌦️ CURRENT WEATHER DATA")
print(weather.head())


# ==================================================
# 2. LOAD CURRENT AIR QUALITY DATA
# ==================================================

air_quality = pd.read_csv("live_air_quality_data.csv")

print("\n🌫️ CURRENT AIR QUALITY DATA")
print(air_quality.head())


# ==================================================
# 3. COMBINE WEATHER + AIR QUALITY
# ==================================================

master_data = pd.merge(
    weather,
    air_quality,
    on=["City", "Latitude", "Longitude"],
    how="inner",
    suffixes=("_Weather", "_Air")
)


# ==================================================
# 4. RENAME TIME COLUMN
# ==================================================

if "Time_Weather" in master_data.columns:

    master_data.rename(
        columns={
            "Time_Weather": "Timestamp"
        },
        inplace=True
    )

    if "Time_Air" in master_data.columns:

        master_data.drop(
            columns=["Time_Air"],
            inplace=True
        )


# ==================================================
# 5. CHECK RAIN PROBABILITY
# ==================================================

if "Rain_Probability_%" in master_data.columns:

    print(
        "\n🌧️ Rain Probability successfully included!"
    )

else:

    print(
        "\n⚠️ Rain Probability column not found!"
    )


# ==================================================
# 6. CONVERT CURRENT TIMESTAMP
# ==================================================

master_data["Timestamp"] = pd.to_datetime(
    master_data["Timestamp"],
    errors="coerce"
)


# ==================================================
# 7. LOAD EXISTING HISTORICAL DATA
# ==================================================

history_file = "climate_master_data.csv"


if os.path.exists(history_file):

    old_data = pd.read_csv(
        history_file
    )

    print(
        f"\n📚 Existing history found: "
        f"{len(old_data)} rows"
    )

    # Convert old Timestamp
    old_data["Timestamp"] = pd.to_datetime(
        old_data["Timestamp"],
        errors="coerce"
    )

    # Remove old corrupted rows
    # where Timestamp is missing
    old_data = old_data.dropna(
        subset=["Timestamp"]
    )

else:

    old_data = pd.DataFrame()

    print(
        "\n📚 No previous history found."
    )


# ==================================================
# 8. APPEND NEW DATA TO HISTORY
# ==================================================

if not old_data.empty:

    master_data = pd.concat(
        [
            old_data,
            master_data
        ],
        ignore_index=True
    )


# ==================================================
# 9. REMOVE RECORDS WITH MISSING TIMESTAMP
# ==================================================

master_data = master_data.dropna(
    subset=["Timestamp"]
)


# ==================================================
# 10. REMOVE DUPLICATE RECORDS
# ==================================================

master_data.drop_duplicates(
    subset=[
        "City",
        "Timestamp"
    ],
    keep="last",
    inplace=True
)


# ==================================================
# 11. SORT DATA
# ==================================================

master_data.sort_values(
    by=[
        "Timestamp",
        "City"
    ],
    inplace=True
)


# ==================================================
# 12. RESET INDEX
# ==================================================

master_data.reset_index(
    drop=True,
    inplace=True
)


# ==================================================
# 13. DISPLAY HISTORICAL DATA
# ==================================================

print("\n")
print("=" * 80)

print(
    "🌍 CLIMATE MASTER HISTORICAL DATA"
)

print("=" * 80)

print(
    master_data.tail(20)
)

print(
    "\nTotal Rows:",
    len(master_data)
)


# ==================================================
# 14. CHECK MISSING VALUES
# ==================================================

print("\n🔍 Missing Values")

print(
    master_data.isnull().sum()
)


# ==================================================
# 15. SAVE HISTORICAL DATA
# ==================================================

master_data.to_csv(
    history_file,
    index=False
)


# ==================================================
# 16. FINAL MESSAGE
# ==================================================

print("\n")
print("=" * 80)

print(
    "✅ HISTORICAL CLIMATE DATA UPDATED SUCCESSFULLY!"
)

print("=" * 80)

print(
    f"📁 File: {history_file}"
)

print(
    f"📊 Total historical records: "
    f"{len(master_data)}"
)

print(
    f"🕒 Latest Timestamp: "
    f"{master_data['Timestamp'].max()}"
)

print(
    "🚫 Blank Timestamp records removed."
)

print(
    "🔄 Duplicate City + Timestamp records removed."
)

print(
    "🎉 New live data added to historical data!"
)