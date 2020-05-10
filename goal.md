# Micropython RGB Covid Reporting
This program will 7 neopixels. If the current days new Covid cases are less than the day before it will show green. Otherwise red. It will shift the colors back one each day to the latest is always the first pixel.

## Tasks
1. Connect to wifi.
2. Get the latest number of new Covid cases
3. Store the previous number of new cases in yesterday's variable
4. Shift all pixels back one. Drop the last pixel if > num of pixels
5. Compare today to yesterday, if > then set pixel 0 as red. Othwewise green.
6. Check again in 24 hrs.