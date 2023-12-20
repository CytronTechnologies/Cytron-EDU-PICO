#Import necessary libraries
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

button_init = False
def init_module(oled):
    global button_init
    
    #Just initialize button once
    if button_init != True:
        # Global variables
        global buttonA_release, buttonB_release
        global buttonA_pressed, buttonB_pressed
        global buttonA, buttonB
        
        buttonA_release = True
        buttonB_release = True
        buttonA_pressed = False
        buttonB_pressed = False

        #Initialize button pins
        buttonA = digitalio.DigitalInOut(board.GP0)
        buttonB = digitalio.DigitalInOut(board.GP1)
        
        button_init = True
    
    #Clear the OLED display
    oled.fill(0)
    
    #Write the data: ('text', x , y, pixel colour)
    #Pixel colour: 0 = false, 1 = true
    oled.text('Buttons', 40, 0, 1)
    oled.text('Press', 0, 20, 1)
    oled.text('Button A to Back', 0, 30, 1)
    oled.text('Button B to Next', 0, 40, 1)
    
    oled.text('(1)', 0, 0, 1)
    
    oled.text('BACK (A)', 0, 57, 1)
    oled.text('(B) NEXT', 80, 57, 1)
    oled.show()
    
def check_button_press():
    global buttonA_release, buttonB_release
    global buttonA_pressed, buttonB_pressed

    #Detect button press when button is release
    if buttonA.value == False and buttonA_release == True:
        buttonA_release = False
    elif buttonA.value == True and buttonA_release == False:
        buttonA_release = True
        buttonA_pressed = True
        return 'A'
    
    if buttonB.value == False and buttonB_release == True:
        buttonB_release = False
    elif buttonB.value == True and buttonB_release == False:
        buttonB_release = True
        buttonB_pressed = True
        return 'B'
           
def run_module():
    button = check_button_press()
    if button:
        print(button)

def deinit_module():
    buttonA.deinit()
    buttonB.deinit()
        
if __name__ == "__main__":
    try:
        init_oled()
        init_module(oled)
        while True:
            #Refresh the oled with interval 1s
            run_module()
    finally:
        deinit_module()
        deinit_oled()
