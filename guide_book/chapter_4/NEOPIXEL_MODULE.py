import board, time, neopixel

num_pixels = 5
pixel_pin = board.GP14
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)

while True:
    pixels.fill((0,0,255))
    time.sleep(1)
    pixels.fill((0,0,0))
    time.sleep(1)






