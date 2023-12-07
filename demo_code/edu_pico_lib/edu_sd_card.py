import board
import busio
import adafruit_ssd1306
import digitalio
import adafruit_sdcard
import storage

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
    global sd_card_write_done, spi, cs
    sd_card_write_done = False
    # Initialize micro SD Card SPI pins
    SCK_PIN = board.GP18
    MOSI_PIN = board.GP19
    MISO_PIN = board.GP16
    CS_PIN = board.GP17
    
    spi = busio.SPI(SCK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)
    cs = digitalio.DigitalInOut(CS_PIN)
        
def run_module(oled):
    global sd_card_write_done, spi, cs
    
    if sd_card_write_done == False:
        #Clear the OLED display
        oled.fill(0)
        
        #Write the data: ('text', x , y, pixel colour)
        #Pixel colour: 0 = false, 1 = true
        oled.text('SD Card', 40, 0, 1)

        try:
            sdcard = adafruit_sdcard.SDCard(spi, cs)
            vfs = storage.VfsFat(sdcard)

            storage.mount(vfs, "/sd")
            with open("/sd/test.txt", "w") as f:
                f.write("SD Card OK!\n")
                #print("Done writing to sd Card")
                oled.text("Done writing", 30, 20, 1)

            with open("/sd/test.txt", "r") as f:
                #print("Read line from file:")
                data = f.readline()
                print(data)
                oled.text(str(data), 30, 35, 1)
                
            storage.umount(vfs)
        except Exception as e:
            print(e);
            oled.text("Error", 45, 20, 1)
            oled.text("{}".format(e), 30, 35, 1)
            
        oled.text('(11)', 0, 0, 1)
            
        oled.text('BACK (A)', 0, 57, 1)
        oled.text('(B) NEXT', 80, 57, 1)
            
        #Show the written data
        oled.show()
        sd_card_write_done = True

def deinit_module():
    global sd_card_write_done
    sd_card_write_done = False
    spi.deinit()
    cs.deinit()
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module()
        while True:
            run_module(oled)
    finally:
        deinit_module()
        deinit_oled()      
    

