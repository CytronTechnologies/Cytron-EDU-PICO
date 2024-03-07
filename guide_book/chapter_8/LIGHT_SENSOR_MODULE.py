import board, time, busio
from adafruit_apds9960.apds9960 import APDS9960

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_color = True
apds.color_gain = 2

while True:
    r, g, b, c = apds.color_data
    brightness_percentage = (c / 65535) * 100
    print(f"Brightness: {brightness_percentage:.1f}%")
    time.sleep(0.5)
    
    