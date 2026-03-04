# worker.py

from weather_api import fetch_weather

def weather_worker(city, api_key, base_url, result_queue):
    result = fetch_weather(city, api_key, base_url)
    result_queue.put(result)