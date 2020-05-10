# Covid RGB Flower

This program uses Micropython, a LOLIN RGB Shield and a Wemos D1 Mini (ESP8266) to represent the rise and fall of new daily COVID-19 cases in Canada with color. Each Neopixel on the shield represents a day. If there were less new cases than the day before, the pixel is green. If not, the pixel is red. Uninitialized pixels are displayed in blue. The ESP8266 checks for new data online hourly and will only import the data if it is not already in 'data.txt' and it is occurs on the next day from what's already recorded.

## Wifi Config

User to define a 'secrets.py' file which includes the following:

    ssid = {put your wifi ssid here}
    pwd = {put your wifi password here}

## Tasks

- [x] Connect to wifi.
- [x] Get the latest number of new Covid cases
- [x] Store the previous number of new cases in yesterday's variable
- [x] Shift all pixels back one. Drop the last pixel if > num of pixels
- [x] Compare today to yesterday, if > then set pixel 0 as red. Othwewise green.
- [x] Check again in 24 hrs.
- [ ] Add comments to code.

## Issues

- Occaisonly LED's blank and re-configure. Assuming this is a reboot but not sure the trigger. Potentially memory issue.

## Community Message

If you find this repository and think that you have a better or more interesting way to do something, please feel free to comment. If you may potentially be a first time contributor to a project, please use this project to experiment with that! This is a first project for me where I tried to wrap it up into something useable and am open to any feedback.
