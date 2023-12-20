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
    #Initialize the APDS9960 proximity
    global apds9960_sensor
    apds9960_sensor = APDS9960(i2c)
    apds9960_sensor.enable_proximity = True
    
    global interval
    interval = time.monotonic()
    print(interval)

def run_module(duration, oled):
    global interval
    #Read the proximity on specific interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('APDS9960', 40, 0, 1)
            
        oled.text("Proximity: {:.0f}".format(apds9960_sensor.proximity), 25, 30, 1)
        
        oled.text('(4)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
        oled.show()

def deinit_module():
    apds9960_sensor.enable_proximity = False
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module(i2c)
        while True:
            #Run the module with interval 0.5s
            run_module(0.5, oled)
    finally:
        deinit_module()
        deinit_oled()