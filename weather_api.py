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
# Get city coordinates
# --------------------------------------------------

def get_coordinates(city):

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(geocoding_url, params=params)

    if response.status_code == 200:

        data = response.json()

        if "results" in data and len(data["results"]) > 0:

            result = data["results"][0]

            return (
                result["latitude"],
                result["longitude"],
                result.get("country", ""),
                result.get("admin1", "")
            )

    return None


# --------------------------------------------------
# Get live weather + rain probability
# --------------------------------------------------

def get_weather(city):

    location = get_coordinates(city)

    if location is None:
        print(f"❌ Location not found: {city}")
        return None

    latitude, longitude, country, state = location

    weather_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,

        # Current weather
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "surface_pressure"
        ],

        # Hourly rain probability
        "hourly": [
            "precipitation_probability"
        ],

        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(weather_url, params=params)

    if response.status_code == 200:

        data = response.json()

        current = data["current"]

        # Find current hour
        current_time = current["time"]

        hourly_times = data["hourly"]["time"]
        hourly_rain_probability = data["hourly"]["precipitation_probability"]

        # Find the closest hourly forecast time
        current_datetime = pd.to_datetime(current_time)

        hourly_datetime = pd.to_datetime(hourly_times)

        time_difference = abs(hourly_datetime - current_datetime)

        index = time_difference.argmin()

        rain_probability = hourly_rain_probability[index]


        return {
            "City": city,
            "State": state,
            "Country": country,
            "Latitude": latitude,
            "Longitude": longitude,

            "Time": current_time,

            "Temperature_C": current["temperature_2m"],
            "Feels_Like_C": current["apparent_temperature"],
            "Humidity_%": current["relative_humidity_2m"],

            "Precipitation_mm": current["precipitation"],

            "Rain_Probability_%": rain_probability,

            "Wind_Speed_kmh": current["wind_speed_10m"],
            "Pressure_hPa": current["surface_pressure"],
            "Weather_Code": current["weather_code"]
        }

    print(f"❌ Weather API error for {city}")

    return None


# --------------------------------------------------
# Fetch weather for all cities
# --------------------------------------------------

weather_data = []

print("\n🌍 LIVE WEATHER DATA")
print("=" * 75)


for city in cities:

    result = get_weather(city)

    if result:

        weather_data.append(result)

        print(
            f"{city}: "
            f"{result['Temperature_C']}°C | "
            f"Humidity {result['Humidity_%']}% | "
            f"Rain Probability {result['Rain_Probability_%']}% | "
            f"Wind {result['Wind_Speed_kmh']} km/h"
        )


# --------------------------------------------------
# Convert to DataFrame
# --------------------------------------------------

df = pd.DataFrame(weather_data)


print("\n")
print("=" * 75)
print("📊 WEATHER DATAFRAME")
print("=" * 75)

print(df)


# --------------------------------------------------
# Save data
# --------------------------------------------------

df.to_csv("live_weather_data.csv", index=False)

print("\n✅ Live weather data saved successfully!")
print("📁 File: live_weather_data.csv")

df.to_csv("live_weather_data.csv", index=False)