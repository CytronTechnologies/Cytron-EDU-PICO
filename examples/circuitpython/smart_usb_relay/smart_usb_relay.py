"""
DESCRIPTION:
This example code will control
the USB relay and RGB LEDs on EDU PICO
when the sound magnitude reached its threshold.

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io
"""
import busio
import time
import array
import math
import board
import digitalio
import neopixel
import storage
import audiobusio
import random
import adafruit_ssd1306

# Initialize OLED display, RGB LEDs, USB relay and PDM Mic.
i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

pixel = neopixel.NeoPixel(board.GP14, 5)

usb = digitalio.DigitalInOut(board.GP22)
usb.direction = digitalio.Direction.OUTPUT

mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
pixel.brightness = 0.1

# Remove DC bias before computing RMS.
def mean(values):
    return sum(values) / len(values)

def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))

oled.fill(0)
oled.show()
oled.text("Make Sound To Start", 5, 35, 1)
oled.show()

led_on = False
pixel.fill(RED)

while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print((magnitude,))
    time.sleep(0.1)
    
    if  magnitude > 1000 and not led_on:
        usb.value = True
        led_on = True
        print("USB RELAY ON")
        pixel.fill(GREEN)
        oled.fill(0)
        oled.text("USB RELAY ON", 30, 35, 1)
        oled.show()

    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    print((magnitude,))
    time.sleep(0.1)

    if  magnitude > 1000 and led_on:
        usb.value = False
        led_on = False
        print("USB RELAY OFF")
        pixel.fill(RED)
        oled.fill(0)
        oled.text("USB RELAY OFF", 30, 35, 1)
        oled.show()
