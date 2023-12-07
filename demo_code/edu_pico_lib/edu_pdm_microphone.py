#Import necessary libraries
import board
import busio
import adafruit_ssd1306
import time
import array, math, audiobusio

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
    #Initialize the PDM Microphone colour
    global mic
    mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=16000, bit_depth=16)
    
    global interval
    interval = time.monotonic()
    
def log10(x):
    return math.log(x) / math.log(10)

def normalized_rms(values):
    minbuf = sum(values) / len(values)
#         samples_sum = sum(float(sample - minbuf) * (sample - minbuf)for sample in values)
    samples_sum = 0
    for sample in values:
        sample_normalize = float(sample - minbuf) * (sample - minbuf)
        samples_sum += sample_normalize
    return math.sqrt(samples_sum / len(values))

def horiz(l,r,t,c, oled):  # left, right ,top, colour
    n = r-l+1        # Horizontal line
    for i in range(n):
        oled.pixel(l + i, t , c)

def vert(l,t,b,c, oled):   # left, top, bottom, colour
    n = b-t+1        # Vertical line
    for i in range(n):
        oled.pixel(l, t+i, c)
        
def graphbar1(oled):
    oled.text("100", 0, 30, 1)
    oled.text("50", 6, 45, 1)
    oled.text("0", 12, 57, 1)
    
    vert(20,30,63,1, oled) # x axis
    horiz(20,120,63,1, oled) # y axis
    
    horiz(19,22,30,1, oled)
    horiz(19,22,48,1, oled)    

def showlinegraph1(oled):
    global buffer_index
    graphbar1(oled)
    
    for i in range(MAX_WIDTH - 1):
        x0 = int(20 + i)
        y0 = int(63 - round(graphdata1[i]/4))  # Reverse the y-coordinate
        x1 = int(20 + i + 1)
        y1 = int(63 - round(graphdata1[i + 1]/4))  # Reverse the y-coordinate
        oled.line(x0, y0, x1, y1, 1)
      
# Increase the buffer size to store more data points
BUFFER_SIZE = 10
MAX_WIDTH = 100
buffer_data = [0] * BUFFER_SIZE
graphdata1 = [0] * MAX_WIDTH
buffer_index = 0  # Index to keep track of the current position in the buffer
DISPLAY_INTERVAL = 1.0  # Update the display every 1 second 

def run_module(duration, oled):
    global interval
    global sound_level_dB
    global last_display_time
    global buffer_index
    global graphdata1
    
    sound_level_dB = 0.0
    
    if time.monotonic() > interval:
        interval = time.monotonic() + duration
        
        samples = array.array('H', [0] * 50)
        mic.record(samples, len(samples))
        magnitude = normalized_rms(samples)
        if magnitude > 0:
            sound_level_dB += 20 * log10(magnitude)
#             print(sound_level_dB)

        # Store the sampled data in the buffer
        if buffer_index < BUFFER_SIZE:
            buffer_data[buffer_index] = sound_level_dB
            buffer_index += 1
#             print(buffer_data)
        else:
            buffer_index = 0
            for index in range(BUFFER_SIZE-1):
                for graph_index in range(MAX_WIDTH-1):
                    graphdata1[graph_index] = graphdata1[graph_index+1] # Shift the array
                graphdata1[len(graphdata1)-1] = buffer_data[index] # Update new data on last array
#             print(graphdata1)
                
            
            # Clear the OLED display
            oled.fill(0)

            oled.text('PDM Microphone', 25, 0, 1)
            oled.text("Sound Level(dB):{:.2f}".format(sound_level_dB), 0, 15, 1)
            oled.text('(8)', 0, 0, 1)

            showlinegraph1(oled)

            oled.show()

def deinit_module():
    mic.deinit()

if __name__ == "__main__":
    try:
        init_oled()
        init_module()
        while True:
            
            #Run the module with interval 0.5s
            run_module(0.01, oled)
    finally:
        deinit_module()
        deinit_oled()        