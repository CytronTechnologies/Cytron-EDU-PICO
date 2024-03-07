import board, time
from pwmio import PWMOut
from adafruit_motor import motor

PWM_M1A = PWMOut(board.GP10,frequency=10000)
PWM_M1B = PWMOut(board.GP11,frequency=10000)
motor = motor.DCMotor(PWM_M1A, PWM_M1B)
speed_mode = [-0.5, -0.25, 0, 0.25, 0.5, 0]

while True:
    for speed in speed_mode:
        print("Speed:", speed * 100)
        motor.throttle = speed
        time.sleep(2)
