#Import necessary libraries
import board
import busio
import adafruit_ssd1306
import time
import neopixel

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
    # Initialize Neopixel RGB LED on pin GP18
    global pixel
    pixel = neopixel.NeoPixel(board.GP14, 5)
    # Clear Neopixel RGB LED
    pixel.fill(0)
    # Set pixel brightness
    pixel.brightness = 0.1

    # Define each colour codes in RGB decimal format
    global RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE 
    RED = (255, 0, 0)
    ORANGE = (255,180,0)
    YELLOW = (80, 80, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (100, 100, 100)

    # Group all the colours in an array
    global colour, colour_name, rgb_count
    colour = [RED,ORANGE,YELLOW,GREEN,CYAN,BLUE,PURPLE,WHITE]
    colour_name = ["RED","ORANGE","YELLOW","GREEN","CYAN","BLUE","PURPLE","WHITE"]

    rgb_count = 0
    
    global interval
    interval = time.monotonic()

def run_module(duration, oled):
    global interval
    global rgb_count
    
    #Change the rgb colour on specific interval
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('Neopixel RGB', 25, 0, 1)
        
        pixel.fill(colour[rgb_count])
        
        oled.text('Colour:', 20, 25, 1)
        oled.text(colour_name[rgb_count], 70, 25, 1)
        
        oled.text('(2)', 0, 0, 1)
        
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
        oled.show()
        
        if rgb_count >= len(colour)-1:
            rgb_count = 0
        else:
            rgb_count += 1

def deinit_module():
    #Off neopixel
    pixel.fill(0)
    pixel.deinit()


if __name__ == "__main__":
    try:
        init_oled()
        init_module()
        while True:
            #Run the module with interval 0.5s
            run_module(0.5, oled)
    finally:
        deinit_module()
        deinit_oled()
