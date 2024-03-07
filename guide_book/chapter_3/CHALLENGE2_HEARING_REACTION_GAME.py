import board
import board, digitalio, time, simpleio, busio
from adafruit_apds9960.apds9960 import APDS9960
import adafruit_ssd1306
import random

FREQ_DO = 262
FREQ_RE = 294
FREQ_MI = 330
FREQ_FA = 350

tone_map = {1: FREQ_DO, 2: FREQ_RE, 3: FREQ_MI, 4: FREQ_FA}

buzzer = board.GP21
button_tone = digitalio.DigitalInOut(board.GP0)
button_start = digitalio.DigitalInOut(board.GP1)
button_tone.direction = digitalio.Direction.INPUT
button_start.direction = digitalio.Direction.INPUT

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

def gamestart():
    oled.fill(0)
    oled.text("Ready", 50, 25, 1)
    oled.show()
    time.sleep(1)
    oled.text("Swipe!", 50, 40, 1)
    oled.show()

while True:
    oled.fill(0)
    oled.text("Button A: Test Tone", 10, 25, 1)
    oled.text("Button B: Play Game", 10, 40, 1)
    oled.show()
    if not button_tone.value:
        oled.fill(0)
        oled.text("Playing Test Tune", 10, 10, 1)
        oled.show()
            
        oled.text("DO", 20, 55, 1)
        oled.show()
        simpleio.tone(buzzer, FREQ_DO, 0.3)
            
        oled.text("RE", 40, 45, 1)
        oled.show()
        simpleio.tone(buzzer, FREQ_RE, 0.3)
            
        oled.text("MI", 60, 35, 1)
        oled.show()
        simpleio.tone(buzzer, FREQ_MI, 0.3)
            
        oled.text("FA", 80, 25, 1)
        oled.show()
        simpleio.tone(buzzer, FREQ_FA, 0.3)
            
    if not button_start.value:
        gamestart()
        tone_code = random.randint(1, 4)
        selected_tone = tone_map[tone_code]
        simpleio.tone(buzzer, selected_tone, 1)
            
        while True:
            prev_tone_code = tone_code
            gesture_value = apds.gesture()
            oled.fill(0)
            oled.text("DO:Up", 50, 25, 1)
            oled.text("RE:Down", 45, 55, 1)
            oled.text("MI:Left", 5, 40, 1)
            oled.text("FA:Right", 75, 40, 1)
            oled.show()
            if gesture_value == tone_code: #1. DO - Up || 2. RE - Down || 3. MI - Left || 4. FA - Right   
                oled.text("Good Job!", 40, 10, 1)
                oled.show()
                for i in range(3):
                    simpleio.tone(buzzer, 1100, 0.1)
                    simpleio.tone(buzzer, 0, 0.1)
                break
            elif gesture_value != 0:                   
                oled.text("Try Again!", 35, 10, 1)
                oled.show()
                for i in range(3):
                    simpleio.tone(buzzer, 100, 0.1)
                    simpleio.tone(buzzer, 0, 0.1)          

