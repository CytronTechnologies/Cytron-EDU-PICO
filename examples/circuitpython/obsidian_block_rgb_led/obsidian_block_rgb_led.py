"""
DESCRIPTION:
This example code for obsidian block RGB LEDs using
EDU PICO. The brightness and colour can be controlled
using potentiometer and the buttons.

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io
"""
import time
import board
import neopixel
import digitalio
from analogio import AnalogIn

# Initialize buttons, potentio and RGB LEDs pins
buttonA = digitalio.DigitalInOut(board.GP0)
buttonA.switch_to_input(pull=digitalio.Pull.UP)  # Set pull-up resistor

buttonB = digitalio.DigitalInOut(board.GP1)
buttonB.switch_to_input(pull=digitalio.Pull.UP)  # Set pull-up resistor

potentio = AnalogIn(board.GP28)

pixels = neopixel.NeoPixel(board.GP14, 5, auto_write=False)
pixels.brightness = 1

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 69, 0)
PINK = (255, 105, 180)
TEAL = (0, 128, 128)

colour_name = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "PURPLE", "WHITE", "ORANGE", "PINK", "TEAL"]
colour_array = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE, ORANGE, PINK, TEAL]
num_colors = len(colour_array)
current_color_index = 0

def fade_to_color(target_color, duration=1.0):
    current_color = pixels[0]
    steps = 100
    delay = duration / steps

    for i in range(steps):
        new_color = tuple(int(current_color[j] + (target_color[j] - current_color[j]) * (i / steps)) for j in range(3))
        pixels.fill(new_color)
        pixels.show()
        time.sleep(delay)

def fade_loop():
    while True:
        if buttonB.value:  # Check if button B is released
            return  # Exit the function if button B is released
        for color in colour_array:
            fade_to_color(color)

print("Adjust the Potentiometer to control the Brightness")
print("Press button A to change the colour")
print("Press button B to run Fade Animation")

while True:
    voltage = (potentio.value * 3.3) / 65536
    bright = voltage / 3.3
    pixels.brightness = bright 

    # Check button A
    if not buttonA.value:
        current_color_index = (current_color_index + 1) % num_colors
        pixels.fill(colour_array[current_color_index])
        print(colour_name[current_color_index])
        while not buttonA.value:
            pass  # Wait for button release

    # Check button B
    if not buttonB.value:
        print("Fade Animation")
        fade_loop()
        
    pixels.show()
