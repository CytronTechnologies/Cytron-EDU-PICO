import board, time
from pwmio import PWMOut
from adafruit_motor import servo

PWM_Servo = PWMOut(board.GP6, frequency=50)
servo = servo.Servo(PWM_Servo, min_pulse=500, max_pulse=2500)

position = [0, 45, 90, 135, 180]

while True:
    for angle in position:
        servo.angle = angle
        print("servo moving to", angle)
        time.sleep(2)




    
    