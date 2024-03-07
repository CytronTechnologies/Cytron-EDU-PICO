import board, digitalio, time, simpleio, neopixel, busio, random
from adafruit_apds9960.apds9960 import APDS9960
import adafruit_ssd1306

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_color = True
apds.enable_proximity = True

buzzer = board.GP21
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

button_start = digitalio.DigitalInOut(board.GP0)
button_start.direction = digitalio.Direction.INPUT

num_pixels = 5
pixel_pin = board.GP14
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)

MELODY_NOTE = [523, 659, 784, 0, 659, 784]
MELODY_DURATION = [0.12, 0.12, 0.12, 0.1, 0.12, 0.2]

oled.fill(0)
oled.text("Press A to", 35, 25, 1)
oled.text("Start a New Game", 15, 35, 1)
oled.show()

prev_colour = None  # Initialize prev_colour

def get_random_colour():
    colours = ["Red", "Green", "Blue", "Yellow", "Purple"]
    x = random.choice(colours)
    while x == prev_colour:
        x = random.choice(colours)
    return x

while True:
    pixels.fill((0,0,0))
    while button_start.value:
        pass
    oled.fill(0)
    oled.show()
    random_colour = get_random_colour()
    prev_colour = random_colour

    oled.text("Find this colour:", 10, 10, 1)
    oled.text(f"{random_colour}", 20, 25, 1)
    oled.show()
    time.sleep(2)
    pixels.fill((255,255,255))
    oled.text("Time left:   seconds", 5, 50, 1)
    
    for countdown in range(5, -1, -1):
        oled.fill_rect(70, 50, 10, 7, 0)
        oled.text(f"{countdown}", 70, 50, 1)
        oled.show()
        time.sleep(1)
        
    if apds.proximity < 10:
        oled.fill(0)
        oled.text("No object detected", 10, 15, 1)
        oled.text("Press A to", 35, 35, 1)
        oled.text("Start a New Game", 15, 45, 1)
        oled.show()
        for i in range(3):
            simpleio.tone(buzzer, 100, 0.1)
            simpleio.tone(buzzer, 0, 0.1) 
    else:
        r, g, b, c = apds.color_data
        print(f"red: {r}, green: {g}, blue: {b}, clear: {c}")
        if r > g and r > b:
            if g > b:
                detected_colour = "Yellow"
            else:
                detected_colour = "Red"
        elif b > r and b > g:
            if r > g:
                detected_colour = "Purple"
            else:
                detected_colour = "Blue"
        elif g > r and g > b:
            detected_colour = "Green"
        
        oled.fill(0)
        oled.text(f"Detected: {detected_colour}", 20, 5, 1)
        oled.show()
        
        if detected_colour == random_colour:
            oled.text("Well Done!", 35, 25, 1)
            oled.text("Press A to", 35, 45, 1)
            oled.text("Start a New Game", 15, 55, 1)
            oled.show()
            for i in range(len(MELODY_NOTE)):
                simpleio.tone(buzzer, MELODY_NOTE[i], MELODY_DURATION[i])
        else:
            oled.text("Try Again.", 35, 25, 1)
            oled.text("Press A to", 35, 45, 1)
            oled.text("Start a New Game", 15, 55, 1)
            oled.show()
            for i in range(3):
                simpleio.tone(buzzer, 100, 0.1)
                simpleio.tone(buzzer, 0, 0.1)
