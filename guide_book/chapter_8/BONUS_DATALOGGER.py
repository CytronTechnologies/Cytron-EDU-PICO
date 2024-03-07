import board, digitalio, time, microcontroller, os

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

file_name = "temperature.csv"
max_file_size = 400000 #400kB

with open(file_name, "a") as datalog:
    while True:
        file_size = os.stat(file_name)[6]
        if file_size < max_file_size:
            temp = microcontroller.cpu.temperature
            datalog.write("{0:.1f}\n".format(temp))
            datalog.flush()
            led.value = not led.value
            time.sleep(1)
        else:
            led.value = True


