import board
import busio
import adafruit_ssd1306
import time
import digitalio

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
    # Initialize Log Data to Pico's Flash Switch pin GP15
    global log_switch
    log_switch = digitalio.DigitalInOut(board.GP15)
    log_switch.direction = digitalio.Direction.INPUT
    
    global interval
    interval = time.monotonic()
        
def run_module(duration, oled):
    global interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text("Log Data to", 34, 0, 1)
        oled.text("Pico's Flash", 30, 10, 1)
        
        if log_switch.value == False:
            #print("Enable")
            oled.text("Switch: Enable", 18, 30, 1)
        else:
            #print("Disable")
            oled.text("Switch: Disable", 18, 30, 1)
        
        oled.text('(12)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
            
        #Show the written data
        oled.show()

def deinit_module():
    log_switch.deinit()
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module()
        while True:
            run_module(0.3, oled)
    finally:
        deinit_module()
        deinit_oled()        