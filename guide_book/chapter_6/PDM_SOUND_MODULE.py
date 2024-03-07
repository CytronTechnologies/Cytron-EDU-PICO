import board, time, array, math, audiobusio

mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)

def log10(x):
    return math.log(x) / math.log(10)

def normalized_rms(values):
    minbuf = sum(values) / len(values)
    samples_sum = sum(float(sample - minbuf) * (sample - minbuf)for sample in values)
    return math.sqrt(samples_sum / len(values))

while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    if magnitude > 0:
        sound_level_dB = 20 * log10(magnitude)
        print(f"Sound Level (dB): {sound_level_dB:.2f}")
    else:
        print("Magnitude is too small to calculate dB.")
    time.sleep(0.1)