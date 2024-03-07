import board, time, neopixel, busio, array, math, audiobusio, adafruit_ssd1306
from analogio import AnalogIn

i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
potentiometer = AnalogIn(board.GP28)

pixels = neopixel.NeoPixel(board.GP14, 5, brightness=0.2)
pixels.fill(0)

mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)

sound_min = 30
sound_max = 80

def log10(x):
    return math.log(x) / math.log(10)

def normalized_rms(values):
    minbuf = sum(values) / len(values)
    samples_sum = sum((sample - minbuf) ** 2 for sample in values)
    return math.sqrt(samples_sum / len(values))

def calculate_sound_level_dB(samples):
    magnitude = normalized_rms(samples)
    sound_level_dB = 20 * log10(magnitude)
    return sound_level_dB

while True:
    oled.fill(0)
    mic.record(samples, len(samples))
    sound_level_dB = calculate_sound_level_dB(samples)
    pot_value = potentiometer.value / 65535 * (sound_max - sound_min) + sound_min

    oled.text("Sound Level (dB):", 15, 5, 1)
    oled.text(f"{sound_level_dB:.2f} dB", 40, 20, 1)
    oled.text(f"Threshold: {pot_value:.1f} dB", 10, 35, 1)
    
    if sound_level_dB > pot_value:
        pixels.fill((255, 0, 0))
        oled.text("SOUND LEVEL HIGH!", 15, 50, 1)
    else:
        pixels.fill((0, 255, 0))
        oled.text("SOUND LEVEL LOW!", 20, 50, 1)
    time.sleep(0.1)
    oled.show()


