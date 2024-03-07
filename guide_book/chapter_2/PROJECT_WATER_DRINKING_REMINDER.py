import board, digitalio, time, simpleio 

button_start = digitalio.DigitalInOut(board.GP0)
button_start.direction = digitalio.Direction.INPUT
button_start.pull = digitalio.Pull.UP

button_stop = digitalio.DigitalInOut(board.GP1)
button_stop.direction = digitalio.Direction.INPUT
button_stop.pull = digitalio.Pull.UP

buzzer_pin = board.GP21
buzzer_status = False

print("Press Button A to start")

while True:
    if not button_start.value:
        duration = 5
        end_time = time.monotonic() + duration
        print("You have activated the water drinking reminder")

        while time.monotonic() < end_time:
            pass

        print("Reminder to Drink Water! Press Button B to reset")
        buzzer_status = True
        
    if not button_stop.value:
        print("Timer reset")
        buzzer_status = False
        time.sleep(0.3)
        print("Press Button A to start")

    if buzzer_status:
        simpleio.tone(buzzer_pin, 800, 0.5)
        simpleio.tone(buzzer_pin, 0, 0.5)

