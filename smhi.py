import requests
import time
import argparse
import ujson as json
from datetime import timedelta, date, datetime


def fetch_weather(location):
    latitude, longitude = location
    url = f"https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}, maybe you entered a place outside the nordics ;)")
        return None


def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    headers = {"User-Agent": "Terminalvader"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            lat, lon = float(data[0]['lat']), float(data[0]['lon'])
            lat = round(lat, 6)
            lon = round(lon, 6)
            return lat, lon
        else:
            print("Coordinates not found for the specified location.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting coordinates: {e}")
        return None


def display_weather(weather_data, days):
    try:
        end_date = datetime.today() + timedelta(int(days))
        timeseries = 0
        json_length = len(weather_data['timeSeries'])
        if weather_data:
            while timeseries < json_length:
                timestamp_str = weather_data['timeSeries'][timeseries]['validTime']
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                if timestamp <= end_date:
                    current_parameter = 0
                    while current_parameter < len(weather_data['timeSeries'][timeseries]['parameters']):
                        if weather_data['timeSeries'][timeseries]['parameters'][current_parameter]['name'] == "t":
                            temperature = weather_data['timeSeries'][timeseries]['parameters'][current_parameter]['values'][0]
                            formatted_timestamp = timestamp.strftime("%m/%d %H:00")
                            print(formatted_timestamp, f"{temperature}°C")
                            break
                        current_parameter += 1
                    timeseries += 1
                else:
                    break
        else:
            print("No weather data available.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("city")
    parser.add_argument("days")
    args = parser.parse_args()

    location = args.city
    days = args.days
    coordinates = get_coordinates(location)
    if coordinates:
        print(f"Coordinates for {location}: {coordinates}")
    else:
        print(f"Coordinates not found for {location}")
    weather_data = fetch_weather(coordinates)
    display_weather(weather_data, days)


if __name__ == "__main__":
    main()
