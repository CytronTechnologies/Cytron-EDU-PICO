import board, digitalio

relay = digitalio.DigitalInOut(board.GP22)
relay.direction = digitalio.Direction.OUTPUT

while True:
    user_input = input("1: ON, 0: OFF: ")
    state = int(user_input)

    if state == 0:
        print("Relay OFF")
        relay.value = False
    elif state == 1:
        print("Relay ON")
        relay.value = True
    else:
        print("Invalid input. Please enter 0 for OFF or 1 for ON.")
