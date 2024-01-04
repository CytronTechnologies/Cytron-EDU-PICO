# Raspberry Pi Pico: http://educ8s.tv/part/RaspberryPiPico
# OLED DISPLAY: https://educ8s.tv/part/OLED096

import board, busio, displayio, time
import adafruit_displayio_ssd1306
import adafruit_imageload

cytron_intro_img = "images/cytron_intro_30_frames.bmp"
edu_pico_img = "images/edu_pico_24_frames.bmp"
push_button_img = "images/push_button_9_frames.bmp"
rgb_img = "images/rgb_7_frames.bmp"
temp_img = "images/temp_humidity_14_frames.bmp"
proximity_img = "images/proximity_6_frames.bmp"
light_img = "images/light_6_frames.bmp"
gesture_img = "images/gesture_10_frames.bmp"
colour_img = "images/colour_7_frames.bmp"
mic_img = "images/mic_10_frames.bmp"
potentio_img = "images/potentio_9_frames.bmp"
music_img = "images/music_10_frames.bmp"
sd_card_img = "images/sd_card_8_frames.bmp"
log_img = "images/log_7_frames.bmp"
servo_img = "images/servo_11_frames.bmp"
motor_img = "images/motor_8_frames.bmp"
usb_img = "images/usb_6_frames.bmp"

SPRITE_SIZE = (128, 64)

cytron_intro_frames= 30
edu_pico_frames = 24
push_button_frames = 9
rgb_frames = 7
temp_frames = 14
proximity_frames = 6
light_frames = 6
gesture_frames = 10
colour_frames = 7
mic_frames = 10
potentio_frames = 9
music_frames = 10
sd_card_frames = 8
log_frames = 7
servo_frames = 11
motor_frames = 8
usb_frames = 6


def init_i2c():
    # Define the i2c GPIOs on SCL=GP5 and SDA=GP4
    global i2c
    i2c = busio.I2C(board.GP5, board.GP4)
    
def init_module(i2c):
    global display
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
    
def run_module(module):
    if module == 0:
        group_animate(cytron_intro_img, SPRITE_SIZE, cytron_intro_frames, invert=False, duration=0.1)
        group_animate(edu_pico_img, SPRITE_SIZE, edu_pico_frames, invert=False, duration=0.1)
    elif module == 1:
        group_animate(push_button_img, SPRITE_SIZE, push_button_frames, invert=False, duration=0.2)
    elif module == 2:
        group_animate(rgb_img, SPRITE_SIZE, rgb_frames, invert=False, duration=0.4)
    elif module == 3:
        group_animate(temp_img, SPRITE_SIZE, temp_frames, invert=False, duration=0.02)
    elif module == 4:
        group_animate(proximity_img, SPRITE_SIZE, proximity_frames, invert=False, duration=0.2)
    elif module == 5:
        group_animate(light_img, SPRITE_SIZE, light_frames, invert=False, duration=0.2)
    elif module == 6:
        group_animate(gesture_img, SPRITE_SIZE, gesture_frames, invert=False, duration=0.2)
    elif module == 7:
        group_animate(colour_img, SPRITE_SIZE, colour_frames, invert=False, duration=0.2)
    elif module == 8:
        group_animate(mic_img, SPRITE_SIZE, mic_frames, invert=False, duration=0.1)
    elif module == 9:
        group_animate(potentio_img, SPRITE_SIZE, potentio_frames, invert=False, duration=0.1)
    elif module == 10:
        group_animate(music_img, SPRITE_SIZE, music_frames, invert=False, duration=0.15)
    elif module == 11:
        group_animate(sd_card_img, SPRITE_SIZE, sd_card_frames, invert=False, duration=0.2)
    elif module == 12:
        group_animate(log_img, SPRITE_SIZE, log_frames, invert=False, duration=0.2)
    elif module == 13:
        group_animate(servo_img, SPRITE_SIZE, servo_frames, invert=False, duration=0.3)
    elif module == 14:
        group_animate(motor_img, SPRITE_SIZE, motor_frames, invert=False, duration=0.3)
    elif module == 15:
        group_animate(usb_img, SPRITE_SIZE, usb_frames, invert=False, duration=0.3)        

def deinit_module():
    display.sleep()
    displayio.release_displays()
    
if __name__ == "__main__":
    try:
        init_i2c()
        init_module(i2c)
        module = 0
        while True:
            
            run_module(module)
            time.sleep(1)
            
            if module > 15:
                module = 0
            else:
                module += 1

    finally:
        deinit_module()
        i2c.deinit()