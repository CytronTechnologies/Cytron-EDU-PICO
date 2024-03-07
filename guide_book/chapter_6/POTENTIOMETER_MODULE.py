import time, board
from analogio import AnalogIn

potentio = AnalogIn(board.GP28)

while True:
    voltage = (potentio.value * 3.3) / 65536
    print(voltage)
    time.sleep(0.1)
    
    
    
    