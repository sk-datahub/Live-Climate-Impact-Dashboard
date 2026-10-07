import requests
import pandas as pd


# --------------------------------------------------
# Cities
# --------------------------------------------------

cities = [
    "Jalgaon",
    "Dharangaon",
    "Chopda",
    "Amalner",
    "Erandol",
    "Dhule",
    "Pune",
    "Mumbai",
    "Delhi",
    "Nashik"
]


# --------------------------------------------------
# Get coordinates
# --------------------------------------------------

def get_coordinates(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        if "results" in data and len(data["results"]) > 0:

            result = data["results"][0]

            return (
                result["latitude"],
                result["longitude"]
            )

    return None


# --------------------------------------------------
# Get Air Quality
# --------------------------------------------------

def get_air_quality(city):

    location = get_coordinates(city)

    if location is None:
        print(f"❌ Location not found: {city}")
        return None

    latitude, longitude = location

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "us_aqi",
            "pm2_5",
            "pm10",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone",
            "uv_index"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()
        current = data["current"]

        return {
            "City": city,
            "Latitude": latitude,
            "Longitude": longitude,
            "Time": current["time"],
            "US_AQI": current["us_aqi"],
            "PM2_5": current["pm2_5"],
            "PM10": current["pm10"],
            "CO": current["carbon_monoxide"],
            "NO2": current["nitrogen_dioxide"],
            "SO2": current["sulphur_dioxide"],
            "O3": current["ozone"],
            "UV_Index": current["uv_index"]
        }

    print(f"❌ Air Quality API Error: {city}")

    return None


# --------------------------------------------------
# Fetch all cities
# --------------------------------------------------

air_quality_data = []

print("\n🌫️ LIVE AIR QUALITY DATA")
print("=" * 70)


for city in cities:

    result = get_air_quality(city)

    if result:

        air_quality_data.append(result)

        print(
            f"{city}: "
            f"AQI {result['US_AQI']} | "
            f"PM2.5 {result['PM2_5']} | "
            f"PM10 {result['PM10']}"
        )


# --------------------------------------------------
# DataFrame
# --------------------------------------------------

df = pd.DataFrame(air_quality_data)


print("\n")
print("=" * 70)
print("📊 AIR QUALITY DATAFRAME")
print("=" * 70)

print(df)


# --------------------------------------------------
# Save CSV
# --------------------------------------------------

df.to_csv("live_air_quality_data.csv", index=False)

print("\n✅ Air quality data saved successfully!")
print("📁 File: live_air_quality_data.csv")