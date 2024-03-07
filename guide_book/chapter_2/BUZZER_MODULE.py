import board
import simpleio

buzzer = board.GP21

while True:
    simpleio.tone(buzzer, 440, 1)
    simpleio.tone(buzzer, 0, 2)




