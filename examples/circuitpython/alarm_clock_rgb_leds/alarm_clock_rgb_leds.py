"""
DESCRIPTION:
This example code will demonstrate how to grab time from the internet
through Network Time Protocol (NTP) and display on OLED Display SS1306.
You can set the alarm time and snooze time.
RGB LEDs and buzzer ON when alarm triggered.

AUTHOR   : Cytron Technologies Sdn Bhd.
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io

REFERENCE:
Code adapted from 2022 Carter Nelson for Adafruit Industries:
https://learn.adafruit.com/super-simple-sunrise-lamp/code
"""
import os
import time
import board
import rtc
import socketpool
import wifi
import adafruit_ntp
import neopixel
import adafruit_ssd1306
import busio as io
import digitalio
import simpleio

# Time zone offset in hours from UTC
# Malaysia/Singapore GMT = +8
# Thailand GMT = +7
# Vietnam GMT = +7
# Germany GMT = +2
# United Kingdom GMT = +1
# Find your country GMT through this link:
# https://greenwichmeantime.com/time-zone/world/


TZ_OFFSET = +8  # time zone offset in hours from UTC
ALARM_HOUR = 9  # alarm time hour (24hr)
ALARM_MIN = 55  # alarm time minute
SNOOZE = 5  # your snooze time in minute

# Initialize OLED
i2c = io.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize buttons
btn0 = digitalio.DigitalInOut(board.GP0)
btn1 = digitalio.DigitalInOut(board.GP1)
btn0.direction = digitalio.Direction.INPUT
btn1.direction = digitalio.Direction.INPUT
btn0.pull = digitalio.Pull.UP
btn1.pull = digitalio.Pull.UP

MELODY_NOTE =     [200, 1000, 10, 1000, 200, -10]
MELODY_DURATION = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

# Define pin connected to piezo buzzer
PIEZO_PIN = board.GP21

# Set up NeoPixels
pixels = neopixel.NeoPixel(board.GP14, 5)

pixels.fill(0)

# Connect to local network
# Retrive your Wifi SSID and password from settings.toml file
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print("Wifi connected.")

# Get current time using NTP
print("Fetching time from NTP.")
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET, socket_timeout=20)
rtc.RTC().datetime = ntp.datetime

# Wait for wake up time
now = time.localtime()
print("Current time: {:2}:{:02}".format(now.tm_hour, now.tm_min))
print("Waiting for alarm {:2}:{:02}".format(ALARM_HOUR, ALARM_MIN))

def display_time():
    global now
    now = time.localtime()
    # Print current time in format hh:mm:ss
    #print("Current time: {:2}:{:02}:{:02}".format(now.tm_hour, now.tm_min, now.tm_sec))
    # Clear all pixels
    oled.fill(0)
    oled.text("Time: ", 0, 10, 1)
    oled.text("{:2}:{:02}:{:02}".format(now.tm_hour, now.tm_min, now.tm_sec), 60, 10, 1)
    oled.text("Alarm: ", 0, 30, 1)
    oled.text("{:2}:{:02}".format(ALARM_HOUR, ALARM_MIN), 60, 30, 1)
    # Show on OLED
    oled.show()
    
color_red = 0xFF0000    
def blink():
    pixels.fill(color_red)
    time.sleep(0.05)
    pixels.fill((0, 0, 0))
    time.sleep(0.05)
    pixels.fill(color_red)
    time.sleep(0.05)
    pixels.fill((0, 0, 0))
    time.sleep(0.05)
    
# Running the clock with the alarm state ON
alarm_state = True
while alarm_state:
    
    display_time()
    
    if (now.tm_hour < 8):
        pixels.brightness = 0.2
    elif (now.tm_hour > 11):
        pixels.brightness = 1

    if(now.tm_hour == ALARM_HOUR and now.tm_min == ALARM_MIN):
        # Execute Alarm
        alarm_on = True
        while alarm_on:
            print("Waking up!")
            display_time()
            oled.text("Waking up!", 30, 50, 1)
            # Show on OLED
            oled.show()
            # Play alarm tone
            for i in range(len(MELODY_NOTE)):
                simpleio.tone(PIEZO_PIN, MELODY_NOTE[i], duration=MELODY_DURATION[i])
            blink()
            
            # Check GP0, snooze if button A pressed
            if not btn0.value: 
                print("Snooze!")
                display_time()
                oled.text("Snooze!", 35, 50, 1)
                # Show on OLED
                oled.show()
                ALARM_MIN += SNOOZE
                time.sleep(1)
                alarm_on = False
                pixels.fill(0)

            # Check GP1, turn off alarm if button B pressed    
            elif not btn1.value: 
                print("Alarm Off!")
                display_time()
                oled.text("Alarm Off!", 30, 50, 1)
                # Show on OLED
                oled.show()
                time.sleep(1)
                alarm_on = False
                alarm_state = False
                pixels.fill(0)
                break
            
# Running the clock with the alarm state OFF
# Push Reset Button if want to ON the alarm state
while True:
    display_time() 

