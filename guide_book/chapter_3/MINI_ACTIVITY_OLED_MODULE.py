import board, busio, time
import adafruit_ssd1306

i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    oled.fill(0)
    oled.text('My name is', 35, 25, 1)
    user_input = input("Name: ")
    oled.text(user_input, 40, 40, 1)
    oled.show()
    time.sleep(1)

