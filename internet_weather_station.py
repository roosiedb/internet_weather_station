### Internet Weather Station
###
### by Stefan van Roosmalen (C) 2021
###   using PyGame for GUI work
###   using OpenWeatherMap.org for gaining weather data
###

import requests
import json
import pygame
import time
from datetime import datetime
import openweathermap
import moonphase
import rss_feed_reader

display_width = 800
display_height = 480

count_getData     = 9999999999
count_getDataAqi  = 9999999999
count_moonPhase   = 9999999999
count_getDataNews = 9999999999
count_toggle      = 0

degree_symbol = u"\N{DEGREE SIGN}"

color_white       = (255,255,255)
color_gray1       = (192, 192, 192)
color_gray2       = (128, 128, 128)
color_gray3       = (96, 96, 96)
color_gray4       = (51, 51, 51)
color_yellow      = (255, 255, 0)
color_lightblue   = (153, 204, 255)
color_lightred    = (255, 100, 100)
color_lightorange = (255, 204, 153)
color_lightpink   = (255, 153, 204)
color_lightgreen  = (0, 255, 0)
color_aqua        = (0, 255, 255)
color_brown       = (204, 102, 0)
color_red         = (255, 0, 0)

########## HELPER FUNCTIONS ##########

def humanDateTime(tmpUnixTimeStamp):
    return humanDate(tmpUnixTimeStamp) + " " + humanTime(tmpUnixTimeStamp)

def humanDate(tmpUnixTimeStamp):
    return datetime.utcfromtimestamp(tmpUnixTimeStamp + openweathermap.weatherCurrent["offset"]).strftime('%d-%m-%Y')

def humanTime(tmpUnixTimeStamp):
    return datetime.utcfromtimestamp(tmpUnixTimeStamp + openweathermap.weatherCurrent["offset"]).strftime('%H:%M')

def dayOfWeek(tmpUnixTimeStamp):
    day = time.strftime('%A', time.localtime(tmpUnixTimeStamp))
    return day

def showMessage(tmpText, tmpX, tmpY, tmpSize, tmpColor, tmpCenter, tmpFontIdx):
    # to print all font names use: print(pygame.font.get_fonts())
    tmpFontName = "none"
    if (tmpFontIdx == 1):
        tmpFontName = "arialblack"
    tmpFont = pygame.font.SysFont(tmpFontName, tmpSize)
    tmpImg = tmpFont.render(tmpText, True, tmpColor)

    width, height = tmpImg.get_size()
    if tmpCenter == True:
        tmpX = tmpX - width / 2
        tmpY = tmpY - height / 2
    
    screen.blit(tmpImg, (tmpX, tmpY))

def showImage(tmpFilename, tmpX, tmpY, tmpSize):
    image = pygame.image.load(tmpFilename)
    if tmpSize > 0:
        image = pygame.transform.scale(image, (tmpSize, tmpSize))
    screen.blit(image, (tmpX, tmpY))

def drawThings():
    drawBackground()
    drawCurrent()
    drawForecast()

def drawBackground():
    tmpTime = humanTime(openweathermap.weatherCurrent["datetime"])
    if tmpTime >= "18:00:00":
        tmpFilename = "evening.jpg"
    elif tmpTime >= "12:00:00":
        tmpFilename = "afternoon.jpg"
    elif tmpTime >= "06:00:00":
        tmpFilename = "morning.jpg"
    elif tmpTime < "06:00:00":
        tmpFilename = "night.jpg"
    image = pygame.image.load("backgrounds/" + tmpFilename)
    screen.blit(image, (0, 0))

def drawCurrent():
    startX = 10
    startY = 10

    # date, description, time (current & last update)   
    pygame.draw.rect(screen, color_gray4, pygame.Rect(startX, startY, 780, 46))
    showMessage(humanDate(openweathermap.weatherCurrent["datetime"]), startX+10, startY, 30, color_gray1, False, 1)
    showMessage(openweathermap.weatherCurrent["desc"], startX+240, startY+8, 46, color_yellow, False, 0)
    showMessage("current:",     580, 15, 22, color_gray2, False, 0)
    showMessage("last update:", 580, 36, 22, color_gray2, False, 0)
    showMessage(str(datetime.now().strftime('%H:%M:%S')), 680, 5, 22, color_gray1, False, 1)
    showMessage(humanTime(openweathermap.weatherCurrent["datetime"]), 680, 26, 22, color_gray2, False, 1)

    # icon & temperature
    pygame.draw.rect(screen, color_gray4, pygame.Rect(startX, startY+56, 780, 141))
    image = pygame.image.load("icons/" + openweathermap.weatherCurrent["icon"] + "@2x.png")
    screen.blit(image, (startX, startY+45+22-15))
    showMessage(str(round(openweathermap.weatherCurrent["temperature"],1)) + degree_symbol + "C", startX+100, startY+30+12, 80, color_white, False, 1)

    # pressure, humidity, clouds & visibility
    pygame.draw.rect(screen, color_gray3, pygame.Rect(startX+380, startY+60, 96, 80))
    pygame.draw.rect(screen, color_gray3, pygame.Rect(startX+480, startY+60, 96, 80))
    pygame.draw.rect(screen, color_gray3, pygame.Rect(startX+580, startY+60, 96, 80))
    pygame.draw.rect(screen, color_gray3, pygame.Rect(startX+680, startY+60, 96, 80))
    showMessage("pressure",   startX+428, startY+70, 25, color_gray1, True, 0)
    showMessage("humidity",   startX+528, startY+70, 25, color_gray1, True, 0)
    showMessage("clouds",     startX+628, startY+70, 25, color_gray1, True, 0)
    showMessage("visibility", startX+728, startY+70, 25, color_gray1, True, 0)
    showMessage(str(openweathermap.weatherCurrent["pressure"]),        startX+428, startY+98, 36, color_lightred, True, 1)
    showMessage(str(openweathermap.weatherCurrent["humidity"]),        startX+528, startY+98, 36, color_lightblue, True, 1)
    showMessage(str(openweathermap.weatherCurrent["clouds"]),          startX+628, startY+98, 36, color_lightorange, True, 1)
    showMessage(str(openweathermap.weatherCurrent["visibility"]/1000), startX+728, startY+98, 36, color_lightpink, True, 1)
    showMessage("(hPa)", startX+428, startY+126, 25, color_gray1, True, 0)
    showMessage("(%)",   startX+528, startY+126, 25, color_gray1, True, 0)
    showMessage("(%)",   startX+628, startY+126, 25, color_gray1, True, 0)
    showMessage("(km)",  startX+728, startY+126, 25, color_gray1, True, 0)

    # sunrise & sunset
    showMessage("sunrise:", startX+10, startY+147, 25, color_gray2, False, 0)
    showMessage("sunset:",  startX+10, startY+170, 25, color_gray2, False, 0)
    showMessage(humanTime(openweathermap.weatherCurrent["sunrise"]), startX+85, startY+138, 22, color_gray1, False, 1)
    showMessage(humanTime(openweathermap.weatherCurrent["sunset"]),  startX+85, startY+160, 22, color_gray1, False, 1)
    image = pygame.image.load("icons/sunrise.png")
    screen.blit(image, (startX+155, startY+139))
    image = pygame.image.load("icons/sunset.png")
    screen.blit(image, (startX+155, startY+160))

    # wind chill & air quality
    showMessage("feels like:",  startX+210, startY+147, 25, color_gray2, False, 0)
    showMessage("air quality:", startX+210, startY+170, 25, color_gray2, False, 0)
    if openweathermap.weatherCurrent["feelslike"] < 0:
        tmpColor = color_aqua
    elif openweathermap.weatherCurrent["feelslike"] < 10:
        tmpColor = color_lightblue
    elif openweathermap.weatherCurrent["feelslike"] < 20:
        tmpColor = color_lightorange
    elif openweathermap.weatherCurrent["feelslike"] < 30:
        tmpColor = color_lightred
    elif openweathermap.weatherCurrent["feelslike"] >= 30:
        tmpColor = color_red
    showMessage(str(round(openweathermap.weatherCurrent["feelslike"],1)) + degree_symbol + "C", startX+305, startY+138, 22, color_aqua, False, 1)
    if openweathermap.airQuality["aqi_value"] == 1 or openweathermap.airQuality["aqi_value"] == 2:
        tmpColor = color_lightgreen
    elif openweathermap.airQuality["aqi_value"] == 3 or openweathermap.airQuality["aqi_value"] == 4:
        tmpColor = color_lightorange
    elif openweathermap.airQuality["aqi_value"] == 5:
        tmpColor = color_red
    showMessage(openweathermap.airQuality["aqi_description"], startX+305, startY+160, 22, tmpColor, False, 1)

    # wind & direction    
    showMessage("wind:", startX+400, startY+147, 25, color_gray2, False, 0)
    showMessage("dir.:", startX+400, startY+170, 25, color_gray2, False, 0)
    showMessage(str(openweathermap.weatherCurrent["windspeed"]) + " km/h", startX+455, startY+138, 22, color_white, False, 1)
    showMessage(openweathermap.weatherCurrent["winddirection"], startX+455, startY+160, 22, color_white, False, 1)

    # moon phase:
    showImage("moon/" + moonphase.moonDescription + ".png", startX+590, startY+143, 50)
    showMessage(moonphase.moonDescription,   startX+640, startY+150, 22, color_gray1, False, 0)
    showMessage(moonphase.moonRiseAndSetTime, startX+640, startY+172, 22, color_gray1, False, 0)

def drawForecast():
    startX = 10
    startY = 217
    for x in range(7):
        pygame.draw.rect(screen, color_gray4, pygame.Rect(startX+(x*112.4), startY, 106, 255))

        # date, icon, desc & temp
        tmpDate = humanDate(openweathermap.weatherForecast[x]["datetime"])[0:5] + " (" + dayOfWeek(openweathermap.weatherForecast[x]["datetime"])[0:2] + ")"
        showMessage(tmpDate, startX+55+(x*112.4), startY+15, 26, color_gray1, True, 0)
        image = pygame.image.load("icons/" + openweathermap.weatherForecast[x]["icon"] + "@2x.png")
        screen.blit(image, (startX+(112.4*x), startY+10))
        showMessage(openweathermap.weatherForecast[x]["main"], startX+50+(x*112.4), startY+110, 36, color_white, True, 0)
        showMessage(str(round(openweathermap.weatherForecast[x]["temperature"])) + degree_symbol, startX+50+(x*112.4), startY+150, 60, color_white, True, 0)

        if count_toggle >= 5:
            # pressure, humidity & clouds
            showImage("icons/barometer.png", startX+10+(112.4*x), startY+180, 16)
            showMessage(str(openweathermap.weatherForecast[x]["pressure"]), startX+35+(112.4*x), startY+180, 28, color_white, False, 0)
            showImage("icons/humidity.png", startX+10+(112.4*x), startY+203, 16)
            showMessage(str(openweathermap.weatherForecast[x]["humidity"]) + "%", startX+35+(112.4*x), startY+203, 28, color_white, False, 0)
            showImage("icons/clouds.png", startX+10+(112.4*x), startY+226, 16)
            showMessage(str(openweathermap.weatherForecast[x]["clouds"]) + "%", startX+35+(112.4*x), startY+226, 28, color_white, False, 0)
        elif count_toggle < 5:
            # pressure, humidity & clouds
            showImage("icons/thermometer.png", startX+10+(112.4*x), startY+180, 16)
            showMessage(str(round(openweathermap.weatherForecast[x]["temp_min"])) + ".." + str(round(openweathermap.weatherForecast[x]["temp_max"])) + degree_symbol, startX+35+(112.4*x), startY+180, 28, color_white, False, 0)
            showImage("icons/wind.png", startX+10+(112.4*x), startY+203, 16)
            showMessage(str(round(openweathermap.weatherForecast[x]["windspeed"])) + " km/h", startX+35+(112.4*x), startY+203, 28, color_white, False, 0)
            showImage("icons/compass.png", startX+10+(112.4*x), startY+226, 16)
            showMessage(openweathermap.weatherForecast[x]["winddirection"], startX+35+(112.4*x), startY+226, 28, color_white, False, 0)

########## PYGAME MAIN ROUTINE ##########
        
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
#screen = pygame.display.set_mode((display_width, display_height), pygame.NOFRAME)
pygame.display.set_caption('Internet Weather Station')
done = False
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        count_getData = count_getData + 1
        if count_getData > 60*15: # eens per 15 minuten
            try:        openweathermap.getDataWeather()
            except:     print("error in routine getData")
            finally:    count_getData = 0
        
        count_toggle = count_toggle + 1
        if count_toggle > 9:
            count_toggle = 0

        count_getDataAqi = count_getDataAqi + 1
        if count_getDataAqi > 60*60*12: # eens per 12 uur
            try:        openweathermap.getDataAqi()
            except:     print("error in routine getDataAqi")
            finally:    count_getDataAqi = 0

        count_moonPhase = count_moonPhase + 1
        if count_moonPhase > 60*60: # eens per uur
            moonphase.calcMoonPhase()
            count_moonPhase = 0

        count_getDataNews = count_getDataNews + 1
        if count_getDataNews > 60*60: # eens per uur
            try:        rss_feed_reader.downloadRss()
            except:     print("error in routine getDataNews")
            finally:    count_getDataNews = 0

        drawThings()
    
        pygame.display.flip()
        pygame.time.delay(1000) # delay 1 sec
pygame.quit()
exit()
