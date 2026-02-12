# tools.py
# This script defines the tools that the AI agent can use to interact with external services.
# Author: Lakshitha Karunaratna

import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool, ToolRuntime

# Load environment variables from a .env file.
# This is typically used for API keys and other sensitive information.
load_dotenv()

# Base URL for the Nominatim Geocoding API. Used to convert city names to geographical coordinates.
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
# Base URL for the Open-Meteo Forecast API. Used to fetch weather data.
OPENMETEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"

def geocode_city(city: str) -> tuple[float, float] | None:
    """
    Converts a city name to latitude and longitude coordinates using the Nominatim API.

    Args:
        city (str): The name of the city to geocode.

    Returns:
        tuple[float, float] | None: A tuple containing (latitude, longitude) if successful,
                                     otherwise None.
    """
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "AI Weather Forecasting Agent" # Nominatim requires a User-Agent header
    }
    try:
        response = requests.get(NOMINATIM_BASE_URL, params=params, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error geocoding city {city}: {e}")
        return None

# Defines a tool that the AI agent can call to get weather information.
@tool
def get_weather_for_location(city: str) -> str:
    """
    Get current weather conditions for a given city.

    Args:
        city (str): The name of the city for which to retrieve weather.

    Returns:
        str: A human-readable string describing the weather conditions and temperature,
             or an error message if the weather could not be retrieved.
    """
    coords = geocode_city(city)
    if not coords:
        return f"Could not find coordinates for {city}. Please try a different location."

    latitude, longitude = coords

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code", # Request current temperature and weather code
        "temperature_unit": "celsius",
        "wind_speed_unit": "ms"
    }
    try:
        response = requests.get(OPENMETEO_BASE_URL, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        weather_data = response.json()

        if "current" in weather_data:
            current = weather_data["current"]
            temperature = current["temperature_2m"]
            weather_code = current["weather_code"]
            # Map Open-Meteo weather codes to a more readable description
            weather_description = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing rime fog",
                51: "Drizzle: Light", 53: "Drizzle: Moderate", 55: "Drizzle: Dense intensity",
                56: "Freezing Drizzle: Light", 57: "Freezing Drizzle: Dense intensity",
                61: "Rain: Slight", 63: "Rain: Moderate", 65: "Rain: Heavy intensity",
                66: "Freezing Rain: Light", 67: "Freezing Rain: Heavy intensity",
                71: "Snow fall: Slight", 73: "Snow fall: Moderate", 75: "Snow fall: Heavy intensity",
                77: "Snow grains",
                80: "Rain showers: Slight", 81: "Rain showers: Moderate", 82: "Rain showers: Violent",
                85: "Snow showers: Slight", 86: "Snow showers: Heavy",
                95: "Thunderstorm: Slight or moderate", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
            }.get(weather_code, "Unknown")
            return f"The weather in {city} is {weather_description} with a temperature of {temperature}°C."
        else:
            return f"Could not retrieve weather for {city}. Error: {weather_data}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather for {city}: {e}"

# Defines a tool that the AI agent can call to get the user's location based on their ID.
# It uses ToolRuntime to access the agent's context, specifically the user_id.
@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """
    Retrieve user's location based on their user ID from the runtime context.
    This is a mock implementation that returns a predefined city based on the user_id.

    Args:
        runtime (ToolRuntime[Context]): The runtime context provided by the agent,
                                        containing user-specific data like `user_id`.

    Returns:
        str: The user's mock location.
    """
    # Access the user_id from the agent's runtime context.
    user_id = runtime.context.user_id
    # A more dynamic mock based on user_id for demonstration purposes.
    if user_id == "1":
        return "London"
    elif user_id == "2":
        return "Tokyo"
    else:
        return "New York"