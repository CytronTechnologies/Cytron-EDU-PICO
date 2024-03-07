import board, time, busio, adafruit_ssd1306
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_motor import servo
from pwmio import PWMOut

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_proximity = True

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

PWM_Servo = PWMOut(board.GP6, frequency=50)
servo = servo.Servo(PWM_Servo, min_pulse=500, max_pulse=2500)
servo.angle = 0

def show_lid_close():
    oled.fill(0)
    oled.text("Status: Lid Close", 10, 10, 1)
    oled.text("Place hand above", 10, 30, 1)
    oled.text("proximity sensor", 10, 40, 1)
    oled.text("to open lid", 10, 50, 1)
    oled.show()

def show_lid_open():
    oled.fill(0)
    oled.text("Status: Lid Open", 10, 10, 1)
    oled.text("Please throw", 10, 30, 1)
    oled.text("the rubbish into", 10, 40, 1)
    oled.text("the bin.", 10, 50, 1)
    oled.show()

show_lid_close()

while True:
    proximity = apds.proximity
    
    if proximity > 20:
        servo.angle = 90
        show_lid_open()
        time.sleep(5)

        servo.angle = 0
        show_lid_close()
        