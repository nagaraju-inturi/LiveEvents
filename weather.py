
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

def getTemperature(location):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "hourly": "temperature_2m",
        "temperature_unit": "fahrenheit"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    # print (hourly_dataframe)
    return hourly_dataframe



# def getTemperature_openweathermap(zipcode, evdate):
#     try:
#         url = 'http://api.openweathermap.org/data/2.5/weather'
#         query_string = {
#             'zip': zipcode,
#             'units': 'imperial',
#             'appid': open_weather
#         }
#         response = requests.request("GET", url, params=query_string).json()

#         time_epoch = response['dt']
#         time_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_epoch))

#         weather_data = {
#             'city': response['name'],
#             'date': time_datetime,
#             'temperature': response['main']['temp'],
#             'description': response['weather'][0]['description']
#         }
#         return weather_data, 200
#     except:
#         return {"error": "No weather information found"}, 404
