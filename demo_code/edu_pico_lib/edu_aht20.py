#Import necessary libraries
import board
import busio
import adafruit_ssd1306
import time
import adafruit_ahtx0

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
        # Initialize potentiometer on pin GP28
        global aht20_sensor
        global interval
        aht20_sensor = adafruit_ahtx0.AHTx0(i2c)
        interval = time.monotonic()
    
def run_module(duration, oled):
    global interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        oled.text('AHT20', 50, 0, 1)
        
        oled.text("Temperature: {:.2f}".format(aht20_sensor.temperature), 10, 20, 1)
        oled.text("Humidity: {:.2f}".format(aht20_sensor.relative_humidity), 10, 35, 1)
        
        oled.text('(3)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
        oled.show()

def deinit_module():
    pass
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module(i2c)
        while True:
            #Run the module with interval 2s
            run_module(2, oled)
    finally:
        deinit_module()
        deinit_oled()        