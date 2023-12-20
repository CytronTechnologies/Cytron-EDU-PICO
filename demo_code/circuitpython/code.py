"""
DESCRIPTION:
Demo-Code for EDU PICO
This demo code is written in CircuitPython and it serves
as an easy quality check when you first receive the board.

You need to use the buttons on the EDU PICO module to navigate
the functionality between each modules.

AUTHOR  : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io

MORE INFO:
https://www.cytron.io/p-edu-project-and-innovation-kits-for-pico-w
https://circuitpython.org/board/raspberry_pi_pico_w
"""
import board
import busio
import adafruit_ssd1306
import time
from edu_pico_lib import edu_splash_screen
from edu_pico_lib import edu_buttons
from edu_pico_lib import edu_neopixel
from edu_pico_lib import edu_aht20
from edu_pico_lib import edu_apds9960_proximity
from edu_pico_lib import edu_apds9960_light
from edu_pico_lib import edu_apds9960_gesture
from edu_pico_lib import edu_apds9960_colour
from edu_pico_lib import edu_pdm_microphone
from edu_pico_lib import edu_potentiometer
from edu_pico_lib import edu_audio_buzzer
from edu_pico_lib import edu_sd_card
from edu_pico_lib import edu_pico_log_switch
from edu_pico_lib import edu_servo
from edu_pico_lib import edu_motor
from edu_pico_lib import edu_usb_relay
import gc


def init_i2c():
    global i2c
    i2c = busio.I2C(board.GP5, board.GP4)
    
def init_oled(i2c):
    global oled
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

def deinit_oled():
    # Clear the OLED display
    print("deinit I2C")
    i2c.deinit()
        
def update_module():
    global module, button
    button = edu_buttons.check_button_press()
    if button == 'A':
        print("Button A pressed")
        edu_audio_buzzer.init_custom_tone('back')
        
        deinit_module(module)
        module -= 1
        if module < 1:
            module = 15
        init_module(module)
        
        print("Module: {}".format(module))
        button = ''
        
    elif button == 'B':
        print("Button B pressed")
        edu_audio_buzzer.init_custom_tone('next')
        
        deinit_module(module)
        module += 1
        if module > 15:
            module = 1
        init_module(module)
        
        print("Module: {}".format(module))
        button = ''

def init_module(module):
    edu_splash_screen.run_module(module)
    if module == 1:
       edu_buttons.init_module(oled)
    elif module == 2:
        edu_neopixel.init_module()
    elif module == 3:
        edu_aht20.init_module(i2c)
    elif module == 4:
        edu_apds9960_proximity.init_module(i2c)
    elif module == 5:
        edu_apds9960_light.init_module(i2c)
    elif module == 6:
        edu_apds9960_gesture.init_module(i2c)
    elif module == 7:
        edu_apds9960_colour.init_module(i2c)
    elif module == 8:
        edu_pdm_microphone.init_module()
    elif module == 9:
        edu_potentiometer.init_module()
    elif module == 10:
        edu_audio_buzzer.init_module(oled)
    elif module == 11:
        edu_sd_card.init_module()
    elif module == 12:
        edu_pico_log_switch.init_module()
    elif module == 13:
        edu_servo.init_module()
    elif module == 14:
        edu_motor.init_module()
    elif module == 15:
        edu_usb_relay.init_module()    
    
def deinit_module(module):
    if module == 1:
       # No need to deinit buttons
        pass
    elif module == 2:
        edu_neopixel.deinit_module()
    elif module == 3:
        edu_aht20.deinit_module()
    elif module == 4:
        edu_apds9960_proximity.deinit_module()
    elif module == 5:
        edu_apds9960_light.deinit_module()
    elif module == 6:
        edu_apds9960_gesture.deinit_module()
    elif module == 7:
        edu_apds9960_colour.deinit_module()
    elif module == 8:
        edu_pdm_microphone.deinit_module()
    elif module == 9:
        edu_potentiometer.deinit_module()
    elif module == 10:
        edu_audio_buzzer.deinit_module()
    elif module == 11:
        edu_sd_card.deinit_module()
    elif module == 12:
        edu_pico_log_switch.deinit_module()
    elif module == 13:
        edu_servo.deinit_module()
    elif module == 14:
        edu_motor.deinit_module()
    elif module == 15:
        edu_usb_relay.deinit_module()
    
module = 1

try:
    init_i2c()
    edu_audio_buzzer.init_custom_tone('intro')
    edu_splash_screen.init_module(i2c)
    edu_splash_screen.run_module(0)

    init_oled(i2c)
    init_module(module)
    time.sleep(0.1)
    
    while True:
        # Free up memory
        gc.collect()
        
        # Check button & update module
        update_module()

        if module == 1:
            # Read the buttons always running
            pass
        elif module == 2:
            edu_neopixel.run_module(0.8, oled)
        elif module == 3:
            edu_aht20.run_module(2, oled)
        elif module == 4:
            edu_apds9960_proximity.run_module(0.8, oled)
        elif module == 5:
            edu_apds9960_light.run_module(1, oled)
        elif module == 6:
            edu_apds9960_gesture.run_module(0.05, oled)
        elif module == 7:
            edu_apds9960_colour.run_module(1, oled)
        elif module == 8:
            edu_pdm_microphone.run_module(0.02, oled)
        elif module == 9:
            edu_potentiometer.run_module(0.8, oled)
        elif module == 10:
            edu_audio_buzzer.run_module()
        elif module == 11:
            edu_sd_card.run_module(oled)
        elif module == 12:
            edu_pico_log_switch.run_module(0.8, oled)
        elif module == 13:
            edu_servo.run_module(0.8, oled)
        elif module == 14:
            edu_motor.run_module(2, oled)
        elif module == 15:
            edu_usb_relay.run_module(1.5, oled)
        
# If error occured display on oled 
except Exception as e:
    print(e)
    oled.fill(0)
    oled.text('Error Occur!', 30, 0, 1)
    error_msg = str(e)
    num_line = round(len(error_msg)/20)
    char_start = 0
    for i in range(num_line):
        char_end = (i+1)*20
        oled.text("{}".format(error_msg[char_start:char_end]), 0, (i+1)*10+10, 1)
        char_start = char_end
    oled.show()
    time.sleep(10)
    
finally:
    edu_splash_screen.deinit_module()
    edu_buttons.deinit_module()
    deinit_module(module)
    deinit_oled()
