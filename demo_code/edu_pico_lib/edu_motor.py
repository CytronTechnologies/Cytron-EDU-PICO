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
    # Initialize motor on pin GP10, GP11, GP12, GP13
    global M1A, M1B, M2A, M2B
    global motor1, motor2
    
    # DC motor setup
    PWM_M1A = board.GP10
    PWM_M1B = board.GP11
    PWM_M2A = board.GP12
    PWM_M2B = board.GP13

    M1A = pwmio.PWMOut(PWM_M1A, frequency=10000)
    M1B = pwmio.PWMOut(PWM_M1B, frequency=10000)
    M2A = pwmio.PWMOut(PWM_M2A, frequency=10000)
    M2B = pwmio.PWMOut(PWM_M2B, frequency=10000)
    motor1 = motor.DCMotor(M1A, M1B)
    motor2 = motor.DCMotor(M2A, M2B)
    
    global motor_index
    motor_index = 0
    
    global interval
    interval = time.monotonic()
        
def run_module(duration, oled):
    global interval
    
    direction_text = ["Forwards slow","Stop",
                      "Forwards","Stop",
                      "Backwards","Stop",
                      "Backwards slow","Stop",]
    def move_motor(direction):
        # Throttle value must be between -1.0 and +1.0
        if direction == 0:
            #print("\nForwards slow")
            motor1.throttle = 0.5
            motor2.throttle = 0.5
        elif direction == 1:
            #print("\nStop")
            motor1.throttle = 0
            motor2.throttle = 0
        elif direction == 2:
            #print("\nForwards")
            motor1.throttle = 1.0
            motor2.throttle = 1.0
        elif direction == 3:
            #print("\nStop")
            motor1.throttle = 0
            motor2.throttle = 0
        elif direction == 4:
            #print("\nBackwards")
            motor1.throttle = -1.0
            motor2.throttle = -1.0
        elif direction == 5:
            #print("\nStop")
            motor1.throttle = 0
            motor2.throttle = 0
        elif direction == 6:
            #print("\nBackwards slow")
            motor1.throttle = -0.5
            motor2.throttle = -0.5
        elif direction == 7:
            #print("\nStop")
            motor1.throttle = 0
            motor2.throttle = 0
    
    global motor_index

    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('Motor', 50, 0, 1)
        
        oled.text("Move Direction:", 25, 20, 1)
        oled.text("{}".format(direction_text[motor_index]), 25, 35, 1)
        
        oled.text('(14)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
            
        #Show the written data
        oled.show()
        
        move_motor(motor_index)
        
        motor_index += 1
        if motor_index > 7:
            motor_index = 0

def deinit_module():
    M1A.deinit()
    M1B.deinit()
    M2A.deinit()
    M2B.deinit()
    
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module()
        while True:
            run_module(2, oled)
    finally:
        deinit_module()
        deinit_oled()      
    

