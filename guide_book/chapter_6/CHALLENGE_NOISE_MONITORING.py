import board, time, neopixel, busio, array, math, audiobusio, adafruit_ssd1306
from analogio import AnalogIn
from pwmio import PWMOut
from adafruit_motor import servo

i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
potentiometer = AnalogIn(board.GP28)

pixels = neopixel.NeoPixel(board.GP14, 5, brightness=0.2)
pixels.fill(0)

mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)

sound_min = 30
sound_max = 80

PWM_Servo = PWMOut(board.GP6, frequency=50)
servo = servo.Servo(PWM_Servo, min_pulse=500, max_pulse=2500)
servo.angle = 0
time.sleep(1)
servo.angle = 180
time.sleep(1)

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
    
    angle = 180 - ((sound_level_dB - sound_min) / (sound_max - sound_min) * 180)
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    servo.angle = angle
    print("servo moving to", angle)
    
    if sound_level_dB > pot_value:
        pixels.fill((255, 0, 0))
        oled.text("SOUND LEVEL HIGH!", 15, 50, 1)
    else:
        pixels.fill((0, 255, 0))
        oled.text("SOUND LEVEL LOW!", 20, 50, 1)
    time.sleep(0.1)
    oled.show()



