import board
import busio
import adafruit_ssd1306
import time
import pwmio
from adafruit_motor import servo, motor

def init_oled():
    # Define the i2c GPIOs on SCL=GP5 and SDA=GP4
    global i2c
    i2c = busio.I2C(board.GP5, board.GP4)

    # Define the OLED display using the above pins
    global oled
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

def deinit_oled():
    #Clear the OLED display
    oled.fill(0)
    oled.show()
    print("deinit I2C")
    i2c.deinit()
    
def init_module():
    # Initialize servos on pin GP6, GP7, GP8, GP9
    # create a PWMOut object on the control pin.
    global pwm1, pwm2, pwm3, pwm4
    pwm1 = pwmio.PWMOut(board.GP6, duty_cycle=0, frequency=50)
    pwm2 = pwmio.PWMOut(board.GP7, duty_cycle=0, frequency=50)
    pwm3 = pwmio.PWMOut(board.GP8, duty_cycle=0, frequency=50)
    pwm4 = pwmio.PWMOut(board.GP9, duty_cycle=0, frequency=50)

    # You might need to calibrate the min_pulse (pulse at 0 degrees) and max_pulse (pulse at 180 degrees) to get an accurate servo angle.
    # The pulse range is 750 - 2250 by default (if not defined).
    # Initialize Servo objects.
    global servo1, servo2, servo3, servo4
    servo1 = servo.Servo(pwm1, min_pulse=750, max_pulse=2250)
    servo2 = servo.Servo(pwm2, min_pulse=750, max_pulse=2250)
    servo3 = servo.Servo(pwm3, min_pulse=750, max_pulse=2250)
    servo4 = servo.Servo(pwm4, min_pulse=750, max_pulse=2250)
    
    global angle
    angle = 0
    
    global interval
    interval = time.monotonic()
        
def run_module(duration, oled):
    global interval
    global angle
    global add_angle
    
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('Servo', 50, 0, 1)
        
        # Condition to add angle
        if angle <= 0:
            add_angle = True
        if angle >= 180:
            add_angle = False
            
        # Add angle increment or decrement    
        if add_angle:
            angle += 5
        else:
            angle -= 5

        # Update servo angles.
        servo1.angle = servo2.angle = servo3.angle = servo4.angle = angle
            
        oled.text("Servo Angle:", 30, 20, 1)
        oled.text("{:.0f} Degree".format(angle), 35, 35, 1)
        
        oled.text('(13)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
            
        #Show the written data
        oled.show()

def deinit_module():
    pwm1.deinit()
    pwm2.deinit()
    pwm3.deinit()
    pwm4.deinit()

if __name__ == "__main__":
    try:
        init_oled()
        init_module()
        while True:
            run_module(0.5, oled)
    finally:
        deinit_module()
        deinit_oled()      