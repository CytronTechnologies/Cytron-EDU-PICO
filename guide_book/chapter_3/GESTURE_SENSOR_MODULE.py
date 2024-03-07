import board, busio
from adafruit_apds9960.apds9960 import APDS9960

i2c = busio.I2C(board.GP5, board.GP4)
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

while True:
    gesture_value = apds.gesture()
    if gesture_value == 1:
        print("up")
    elif gesture_value == 2:
        print("down")
    elif gesture_value == 3:
        print("left")
    elif gesture_value == 4:
        print("right")


