"""
DESCRIPTION:
This example code will uses Buttons and gestures
sensor on APDS9960 on EDU PICO modules to
send a configurable keycode to the computer.

CONNECTION:
EDU PICO :  Module
GP0      -  Button A (Yellow)
GP1      -  Button B (Blue)
GP4      -  SDA
GP5      -  SCL

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io

Referrence:
https://docs.circuitpython.org/projects/hid/en/latest/api.html
"""
import time
import board
import digitalio
import busio
import adafruit_ssd1306
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import usb_hid

# Initialize Gesture sensor and Buttons
i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
multi_sensor = APDS9960(i2c)
multi_sensor.enable_proximity = True
multi_sensor.enable_gesture = True

buttonA = digitalio.DigitalInOut(board.GP0)
buttonB = digitalio.DigitalInOut(board.GP1)

button_init = False
buttonA_release = True
buttonB_release = True
buttonA_pressed = False
buttonB_pressed = False

# Define keyboard key
buttonA_key = Keycode.SPACE               # Yellow Button
buttonB_key = '0'                         # Blue Button
gestureUp_key = Keycode.UP_ARROW          # Gesture UP
gestureDown_key = Keycode.DOWN_ARROW      # Gesture Down
gestureLeft_key = Keycode.LEFT_ARROW      # Gesture Left
gestureRight_key = Keycode.RIGHT_ARROW    # Gesture Right

# Initialize Keyboard
k = Keyboard(usb_hid.devices)
k_layout = KeyboardLayoutUS(k)

while True:
    # Read Button A when button on release
    if buttonA.value == False and buttonA_release == True:
        buttonA_release = False
    elif buttonA.value == True and buttonA_release == False:
        buttonA_release = True
        buttonA_pressed = True
        k.send(buttonA_key)
        print("Button A Pressed")
        time.sleep(0.1)
    
    # Read Button B when button on release
    if buttonB.value == False and buttonB_release == True:
        buttonB_release = False
    elif buttonB.value == True and buttonB_release == False:
        buttonB_release = True 
        buttonB_pressed = True
        k_layout.write(buttonB_key)
        print("Button B Pressed")
        time.sleep(0.1)
    
    # Read Gesture sensor
    gesture = multi_sensor.gesture()
    if gesture == 1:
        print("UP")
        k.send(gestureUp_key)
        time.sleep(0.1)

    if gesture == 2:
        print("DOWN")
        k.send(gestureDown_key)
        time.sleep(0.1)

    if gesture == 3:
        print("LEFT")
        k.send(gestureLeft_key)
        time.sleep(0.1)

    if gesture == 4:
        print("RIGHT")
        k.send(gestureRight_key)
        time.sleep(0.1)