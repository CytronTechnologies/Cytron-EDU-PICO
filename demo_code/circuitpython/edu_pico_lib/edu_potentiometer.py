import board
import busio
import adafruit_ssd1306
import time
import analogio

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
    # Initialize potentiometer on pin GP28
    global potentio
    potentio = analogio.AnalogIn(board.GP28)
    
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
        oled.text('Potentiometer', 30, 0, 1)
        
        voltage = potentio.value * 3.3 / 65535
        percentage = (voltage / 3.3) * 100
            
        oled.text("Voltage: {:.2f} V".format(voltage), 20, 20, 1)
        oled.text("Percentage: {:.0f} %".format(percentage), 15, 35, 1)
        
        oled.text('(9)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
            
        #Show the written data
        oled.show()

def deinit_module():
    potentio.deinit()
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module()
        while True:
            run_module(0.5, oled)
    finally:
        deinit_module()
        deinit_oled()     