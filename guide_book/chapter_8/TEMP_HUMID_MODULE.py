import board, time, busio
import adafruit_ahtx0

i2c = busio.I2C(board.GP5, board.GP4)
AHT_sensor = adafruit_ahtx0.AHTx0(i2c)

while True:
    temperature = AHT_sensor.temperature
    humidity = AHT_sensor.relative_humidity
    print(f"Temperature={temperature:.2f} C Humidity={humidity:.2f} %")
    time.sleep(2)