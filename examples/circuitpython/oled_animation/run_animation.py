"""
DESCRIPTION:
This example code will uses:
EDU PICO to display animation on the OLED.

CONNECTION:
EDU PICO : OLED Display SSD1315
GP4   -  SDA
GP5   -  SCL

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io

REFERENCE:
Code adapted from educ8s.tv:
https://educ8s.tv/oled-animation/
"""
import board, busio, displayio, time
import adafruit_displayio_ssd1306
import adafruit_imageload

cytron_intro_img = "intro_cytron_20_frames.bmp"

SPRITE_SIZE = (128, 64)

cytron_intro_frames= 20

# Define the i2c GPIOs on SCL=GP5 and SDA=GP4
i2c = busio.I2C(board.GP5, board.GP4)
    
displayio.release_displays()

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

def group_animate(IMAGE_FILE, SPRITE_SIZE, frame, invert, duration): 
    #  load the spritesheet
    icon_bit, icon_pal = adafruit_imageload.load(IMAGE_FILE,
                                                    bitmap=displayio.Bitmap,
                                                    palette=displayio.Palette)
    if invert:
        temp = icon_pal[0]
        icon_pal[0] = icon_pal[1]
        icon_pal[1] = temp

    icon_grid = displayio.TileGrid(icon_bit, pixel_shader=icon_pal,
                                     width=1, height=1,
                                     tile_height=SPRITE_SIZE[1], tile_width=SPRITE_SIZE[0],
                                     default_tile=0,
                                     x=0, y=0)

    group = displayio.Group()
    group.append(icon_grid)
    
    try:
        display.show(group)
    except AttributeError:
        # For Circuitpython 9.x.x and above
        display.root_group = group
    interval = 0
    pointer = 0
    running = True
    while running:
        if time.monotonic() > interval:
            icon_grid[0] = pointer
            pointer += 1
            interval = time.monotonic() + duration
            if pointer > frame-1:
                pointer = 0
                running =  False
    time.sleep(0.1)
    group.remove(icon_grid)
    
while True:    
    group_animate(cytron_intro_img, SPRITE_SIZE, cytron_intro_frames, invert=False, duration=0.1)
    time.sleep(1)
