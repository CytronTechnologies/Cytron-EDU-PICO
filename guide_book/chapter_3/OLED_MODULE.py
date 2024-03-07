import board, busio, time
import adafruit_ssd1306

i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.invert(True)
oled.text("Hello", 50, 20, 1)
oled.text("EDU PICO!", 40, 35, 1)
oled.show()

