#Import necessary libraries
import board
import busio
import adafruit_ssd1306
import time
from adafruit_apds9960.apds9960 import APDS9960

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

def init_module(i2c):
    #Initialize the APDS9960 colour
    global apds9960_sensor
    apds9960_sensor = APDS9960(i2c)
    apds9960_sensor.enable_proximity = True
    apds9960_sensor.enable_gesture = True
    
    global current_gesture
    current_gesture = "Move hand"
    
    global interval
    interval = time.monotonic()
    
def run_module(duration, oled):
    global interval
    global current_gesture
    #Read the gesture on specific interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('APDS9960', 40, 0, 1)

        gesture = apds9960_sensor.gesture()
        
        if gesture == 0x01:
            current_gesture = "Up"
        elif gesture == 0x02:
            current_gesture = "Down"
        elif gesture == 0x03:
            current_gesture = "Left"
        elif gesture == 0x04:
            current_gesture = "Right"
            
        oled.text("Gesture: {}".format(current_gesture), 10, 30, 1)
        
        oled.text('(6)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
        oled.show()

def deinit_module():
    apds9960_sensor.enable_proximity = False
    apds9960_sensor.enable_gesture = False
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module(i2c)
        while True:
            #Run the module with interval 0.05s
            run_module(0.05, oled)
    finally:
        deinit_module()
        deinit_oled()       

