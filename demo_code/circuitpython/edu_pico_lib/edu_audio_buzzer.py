import board
import busio
import adafruit_ssd1306
import time
import simpleio

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

def init_custom_tone(custom):
    global melody_index
    global MELODY_NOTE, MELODY_DURATION, PIEZO_AUDIO_L_PIN, AUDIO_R_PIN
    
    melody_index = 0
    
    if custom == "intro":
        MELODY_NOTE = [2637, 2637, 0, 2637, 0, 2093, 2637, 0, 3136, 0]
        MELODY_DURATION = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15]
    elif custom == "next":
        MELODY_NOTE = [659, 784, 987]  # Adjust the note frequencies as needed
        MELODY_DURATION = [0.2, 0.2, 0.2]  # Adjust the durations as needed
    elif custom == "back":
        MELODY_NOTE = [987, 784, 659]  # Adjust the note frequencies as needed
        MELODY_DURATION = [0.2, 0.2, 0.2]  # Adjust the durations as needed
    
    #Define pin connected to piezo buzzer
    PIEZO_AUDIO_L_PIN = board.GP21
    AUDIO_R_PIN = board.GP20
    
    while melody_index < len(MELODY_DURATION)-1:
        run_module()

def init_module(oled):
    # Initialize audio and buzzer pins
    global melody_index
    global MELODY_NOTE, MELODY_DURATION, PIEZO_AUDIO_L_PIN, AUDIO_R_PIN
    
    melody_index = 0
    
    MELODY_NOTE = [2637, 2637, 0, 2637, 0, 2093, 2637, 0, 3136, 0, 0, 0, 1568, 0, 0, 0, 2093, 0, 0, 1568, 0, 0, 1319, 0, 0, 1760, 0,
                 1976, 0, 1865, 1760, 0, 1568, 2637, 0, 3136, 3520, 0, 2794, 3136, 0, 2637, 0, 2093, 2349, 1976, 0, 0, 0, 0, 0]
    MELODY_DURATION = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15,
                   0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15,
                   0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15]
    
    #Define pin connected to piezo buzzer
    PIEZO_AUDIO_L_PIN = board.GP21
    AUDIO_R_PIN = board.GP20
    
    #Clear the OLED display
    oled.fill(0)
    
    #Write the data: ('text', x , y, pixel colour)
    #Pixel colour: 0 = false, 1 = true
    oled.text('Audio & Buzzer', 25, 0, 1)
        
    oled.text("Slide the switch", 15, 20, 1)
    oled.text("Audio & Buzzer", 25, 35, 1)
    
    oled.text('(10)', 0, 0, 1)
    
    oled.text('BACK (A)', 0, 57, 1)
    oled.text('(B) NEXT', 80, 57, 1)

    #Show the written data
    oled.show()

    global interval
    interval = time.monotonic()
        
def run_module():
    global interval
    global melody_index

    if MELODY_NOTE[melody_index] == 0:
        interval = time.monotonic() + MELODY_DURATION[melody_index]
        time.sleep(MELODY_DURATION[melody_index])
    else:
        # Play melody tones
        simpleio.tone(PIEZO_AUDIO_L_PIN, MELODY_NOTE[melody_index], duration=MELODY_DURATION[melody_index])
#         simpleio.tone(AUDIO_R_PIN, MELODY_NOTE[melody_index], duration=MELODY_DURATION[melody_index])
    
    if melody_index < len(MELODY_DURATION)-1:
        # Move to the next melody note
        melody_index += 1
    else:
        melody_index = 0

def deinit_module():
    pass
    
if __name__ == "__main__":
    try:
        init_oled()
        init_module(oled)
#         init_custom_tone('intro')
        while True:
            run_module()
    finally:
        deinit_module()
        deinit_oled()      
    