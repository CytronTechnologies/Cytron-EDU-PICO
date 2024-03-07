import board, time, busio, simpleio
from adafruit_apds9960.apds9960 import APDS9960

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_proximity = True

buzzer = board.GP21

while True:
    proximity = apds.proximity
    duration = 1 - proximity / 255
    print(f"Proximity: {proximity}, duration: {duration} sec")
    simpleio.tone(buzzer, 440, 0.1)  
    time.sleep(duration)
