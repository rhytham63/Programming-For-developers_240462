# weather_api.py
import requests

def fetch_weather(city, api_key, base_url):
    try:
        params = {
            "key": api_key,
            "q": city,
            "aqi": "no"
        }

        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()

        # DEBUG (optional)
        print(city, "→", data)

        if "error" in data:
            return (city, "-", "-", "-", "Error")

        temp = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        pressure = data["current"]["pressure_mb"]

        return (city, temp, humidity, pressure, "OK")

    except Exception as e:
        print("Exception:", e)
        return (city, "-", "-", "-", "Failed")