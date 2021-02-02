import requests
import json
from datetime import datetime

api_key = "fill in your own api key here!"
lat = "52.000000" # fill in your LAT en LON details here
lon = "5.000000"  # fill in your LAT en LON details here
url_weather    = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)
url_airquality = "http://api.openweathermap.org/data/2.5/air_pollution?lat=%s&lon=%s&appid=%s" % (lat, lon, api_key)

weatherCurrent = {}
weatherForecast = []
airQuality = {}

def windDegreesToDirection(tmpDegreesDeg):
    tmpSectors = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    tmpIndex = round(tmpDegreesDeg / (360. / len(tmpSectors)))
    return tmpSectors[tmpIndex % len(tmpSectors)]

def aqiToDesc(tmpAqi):
    tmpResult = "unknown"
    if tmpAqi == 1:
        tmpResult = "good"
    if tmpAqi == 2:
        tmpResult = "fair"    
    if tmpAqi == 3:
        tmpResult = "moderate"    
    if tmpAqi == 4:
        tmpResult = "poor"    
    if tmpAqi == 5:
        tmpResult = "very poor"    
    return tmpResult

def getDataWeather():
    response = requests.get(url_weather)
    data = json.loads(response.text)
    #print(data)
    weatherCurrent["main"]          = data["current"]["weather"][0]["main"]
    weatherCurrent["desc"]          = data["current"]["weather"][0]["description"]
    weatherCurrent["icon"]          = data["current"]["weather"][0]["icon"]
    weatherCurrent["temperature"]   = data["current"]["temp"]
    weatherCurrent["feelslike"]     = data["current"]["feels_like"]
    weatherCurrent["datetime"]      = data["current"]["dt"]
    weatherCurrent["offset"]        = data["timezone_offset"]
    weatherCurrent["sunrise"]       = data["current"]["sunrise"]
    weatherCurrent["sunset"]        = data["current"]["sunset"]
    weatherCurrent["pressure"]      = data["current"]["pressure"]
    weatherCurrent["humidity"]      = data["current"]["humidity"]
    weatherCurrent["clouds"]        = data["current"]["clouds"]
    weatherCurrent["visibility"]    = data["current"]["visibility"]
    weatherCurrent["windspeed"]     = data["current"]["wind_speed"]
    weatherCurrent["winddirection"] = windDegreesToDirection(data["current"]["wind_deg"])

    print("============================================")
    print("Date & time:    " + str(weatherCurrent["datetime"]))
    print("Main:           " + weatherCurrent["main"])
    print("Description:    " + weatherCurrent["desc"])
    print("Icon:           " + weatherCurrent["icon"])
    print("Temperature:    " + str(weatherCurrent["temperature"])) 
    print("Feels like      " + str(weatherCurrent["feelslike"]))
    print("Sunrise:        " + str(weatherCurrent["sunrise"]))
    print("Sunset:         " + str(weatherCurrent["sunset"]))
    print("Pressure:       " + str(weatherCurrent["pressure"]))
    print("Humidity:       " + str(weatherCurrent["humidity"]))
    print("Clouds:         " + str(weatherCurrent["clouds"]))
    print("Visibility:     " + str(weatherCurrent["visibility"]))
    print("Wind speed:     " + str(weatherCurrent["windspeed"]))
    print("Wind direction: " + str(weatherCurrent["winddirection"]))

    weatherForecast.clear();
    for x in range(7):
        tmpDaily = data["daily"][x]
        weatherForecast.append(
            {"datetime":      tmpDaily["dt"],
             "icon":          tmpDaily["weather"][0]["icon"],
             "main":          tmpDaily["weather"][0]["main"],
             "temperature":   tmpDaily["temp"]["day"],
             "temp_min":      tmpDaily["temp"]["min"],
             "temp_max":      tmpDaily["temp"]["max"],
             "pressure":      tmpDaily["pressure"],
             "humidity":      tmpDaily["humidity"],
             "clouds":        tmpDaily["clouds"],
             "windspeed":     tmpDaily["wind_speed"],
             "winddirection": windDegreesToDirection(tmpDaily["wind_deg"])
            }
        ) 

def getDataAqi():
    response = requests.get(url_airquality)
    data = json.loads(response.text)
    airQuality["aqi_value"]       = data["list"][0]["main"]["aqi"]
    airQuality["aqi_description"] = aqiToDesc(airQuality["aqi_value"])
    print("============================================")
    print("Aqi value:      " + str(airQuality["aqi_value"]))
    print("Aqi desc:       " + str(airQuality["aqi_description"]))
