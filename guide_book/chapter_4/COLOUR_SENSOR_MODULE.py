import board, time, busio, neopixel
from adafruit_apds9960.apds9960 import APDS9960

num_pixels = 5
pixel_pin = board.GP14
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_color = True

while True:
    pixels.fill((255,255,255))
    r, g, b, c = apds.color_data
    print(f"red: {r}, green: {g}, blue: {b}, clear: {c}")
    time.sleep(1)

