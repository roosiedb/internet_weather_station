"""
moonphase.py - Calculate Lunar Phase
based on script by Sean B. Palmer, inamidst.com
Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
"""

import math, decimal, datetime

dec = decimal.Decimal
moonPosition = 0
moonDescription = ""
moonRiseAndSetTime = ""

def position(now=None): 
    if now is None: 
        now = datetime.datetime.now()
    diff = now - datetime.datetime(2001, 1, 1)
    days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
    lunations = dec("0.20439731") + (days * dec("0.03386319269"))
    return lunations % dec(1)

def phase(pos): 
    index = (pos * dec(8)) + dec("0.5")
    index = math.floor(index)
    return {
        0: "New Moon", 
        1: "Waxing Crescent", 
        2: "First Quarter", 
        3: "Waxing Gibbous", 
        4: "Full Moon", 
        5: "Waning Gibbous", 
        6: "Last Quarter", 
        7: "Waning Crescent"
    }[int(index) & 7]

def averageRiseAndSetTime(pos):
    index = (pos * dec(8)) + dec("0.5")
    index = math.floor(index)
    return {
        0: "6:00 - 18:00",
        1: "9:00 - 21:00",
        2: "Noon - Midnight",
        3: "15:00 - 03:00",
        4: "18:00 - 06:00",
        5: "21:00 - 09:00",
        6: "Midnight - Noon",
        7: "03:00 - 15:00"
    }[int(index) & 7]

def calcMoonPhase():
    global moonDescription
    global moonPosition
    global moonRiseAndSetTime
    tmpPosition = position()
    moonDescription = phase(tmpPosition)
    moonPosition = round(float(tmpPosition), 3)
    moonRiseAndSetTime = averageRiseAndSetTime(tmpPosition)
    print("============================================")
    print("moon_position:    " + str(moonPosition))
    print("moon description: " + moonDescription)
