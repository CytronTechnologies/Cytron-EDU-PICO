import board
import time
import digitalio

button_A = digitalio.DigitalInOut(board.GP0)
button_A.direction = digitalio.Direction.INPUT
button_A.pull = digitalio.Pull.UP

while True:
    if not button_A.value:
        print("Button A is pressed")
        time.sleep(0.3)




