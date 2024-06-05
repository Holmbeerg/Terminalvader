import requests
import time
import argparse
import ujson as json
from datetime import timedelta, date, datetime
from zoneinfo import ZoneInfo
from tzlocal import get_localzone_name

# https://opendata.smhi.se/apidocs/metfcst/index.html#about

weather_descriptions = {
    1: "Clear sky",
    2: "Nearly clear sky",
    3: "Variable cloudiness",
    4: "Halfclear sky",
    5: "Cloudy sky",
    6: "Overcast",
    7: "Fog",
    8: "Light rain showers",
    9: "Moderate rain showers",
    10: "Heavy rain showers",
    11: "Thunderstorm",
    12: "Light sleet showers",
    13: "Moderate sleet showers",
    14: "Heavy sleet showers",
    15: "Light snow showers",
    16: "Moderate snow showers",
    17: "Heavy snow showers",
    18: "Light rain",
    19: "Moderate rain",
    20: "Heavy rain",
    21: "Thunder",
    22: "Light sleet",
    23: "Moderate sleet",
    24: "Heavy sleet",
    25: "Light snowfall",
    26: "Moderate snowfall",
    27: "Heavy snowfall"
}


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
        end_date = datetime.utcnow() + timedelta(int(days))
        timeseries = 0
        json_length = len(weather_data['timeSeries'])
        local_timezone_name = get_localzone_name()
        print("Timezone: " + local_timezone_name)

        if weather_data:
            while timeseries < json_length:
                timestamp_str = weather_data['timeSeries'][timeseries]['validTime']
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
                if timestamp <= end_date:
                    current_parameter = 0
                    pmedian = None
                    temperature = None
                    wind_speed = None
                    weather_code = None
                    while current_parameter < len(weather_data['timeSeries'][timeseries]['parameters']):
                        parameter = weather_data['timeSeries'][timeseries]['parameters'][current_parameter]
                        if parameter['name'] == "t":
                            temperature = parameter['values'][0]
                        elif parameter['name'] == "ws":
                            wind_speed = parameter['values'][0]
                        elif parameter['name'] == "pmedian":
                            pmedian = parameter['values'][0]
                        elif parameter['name'] == "Wsymb2":
                            weather_code = parameter['values'][0]
                        current_parameter += 1

                    local_timestamp = timestamp.astimezone(ZoneInfo(local_timezone_name))
                    utc_offset = local_timestamp.utcoffset().total_seconds()/60/60
                    adjusted_timestamp = local_timestamp + timedelta(hours=utc_offset)
                    formatted_timestamp = adjusted_timestamp.strftime("%m/%d %H:00")
                    weather_description = weather_descriptions.get(weather_code)
                    print(formatted_timestamp + ", " f"{temperature}°C" + ", " + f"{wind_speed} m/s" + ", " + f"{pmedian}mm" + ", " + weather_description)
                timeseries += 1
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
