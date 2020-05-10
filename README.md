# Covid RGB Flower

This program uses Micropython, a LOLIN RGB Shield and a Wemos D1 Mini (ESP8266) to represent the rise and fall of new daily COVID-19 cases in Canada with color. Each Neopixel on the shield represents a day. If there were less new cases than the day before, the pixel is green. If not, the pixel is red. Uninitialized pixels are displayed in blue. The ESP8266 checks for new data online hourly and will only import the data if it is not already in 'data.txt' and it is occurs on the next day from what's already recorded.

## Wifi Config

User to define a 'secrets.py' file which includes the following:

    ssid = {put your wifi ssid here}
    pwd = {put your wifi password here}
