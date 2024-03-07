import board, time
from analogio import AnalogIn
from pwmio import PWMOut
from adafruit_motor import motor

PWM_M1A = PWMOut(board.GP10,frequency=10000)
PWM_M1B = PWMOut(board.GP11,frequency=10000)
motor = motor.DCMotor(PWM_M1A, PWM_M1B)

potentio = AnalogIn(board.GP28)

while True:
    speed = potentio.value / 65536
    motor.throttle = speed
    print("Speed:", speed)
    time.sleep(0.1)