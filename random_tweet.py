import sys
import psutil
import random
from twython import Twython

API_Key = "enter twitter api key"
API_Secret_Key = ""
Token_Key = ""
Token_Secret_Key = ""

api = Twython(API_Key, API_Secret_Key, Token_Key, Token_Secret_Key)

def get_temp():
    temp_string = str(psutil.sensors_temperatures())
    temp = temp_string[43:48]
    tweet = "My CPU temperature is: " + temp + " degrees Celsius."
    return tweet


def get_quote():
    f = open("path to file full of possible tweets", "r")
    quote_list = f.readlines()
    quotes =[]
    for line in quote_list:
        line.strip()
        quotes.append(line)
    rand_int = random.randrange(0, len(quotes))
    tweet = quotes[rand_int]
    return tweet

def get_battery():
    battery_string = str(psutil.sensors_battery())
    battery = battery_string[17:20]
    tweet = "I only have " + battery + "% battery left... hmph. I've seen worse!"
    return tweet

def get_weather():
    a = "Check out the weather!\n" \
        "https://weather.com/weather/today"
    return a


rand_1 = random.randrange(0, 10)

if rand_1 in range(0,3):
    tweet = get_weather()
elif rand_1 == 4:
    tweet = get_temp()
elif rand_1 in range(5,9):
    tweet = get_quote()
else:
    tweet = get_battery()

api.update_status(status=tweet)
