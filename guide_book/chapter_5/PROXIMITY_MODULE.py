import board, time, busio
from adafruit_apds9960.apds9960 import APDS9960

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_proximity = True

while True:
    proximity = apds.proximity
    print(f"Proximity:{proximity}")          
    time.sleep(0.1)
    

    