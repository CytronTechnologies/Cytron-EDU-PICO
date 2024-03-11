"""
DESCRIPTION:
This example code will uses:
EDU PICO to play the WAV audio file from SD card.

CONNECTION:
EDU PICO :  SD card SPI
GP18     -  SCK/clock
GP19     -  MOSI
GP16     -  MISO
GP17     -  CS

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io
"""
import board
import busio
import sdcardio
import storage
import audiocore
import audiopwmio

dac = audiopwmio.PWMAudioOut(left_channel=board.GP21, right_channel=board.GP20)

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = board.GP17

# Alternative pin assignment
# spi = board.SD_SPI()
# cs = board.SD_CS

sd = sdcardio.SDCard(spi, cs)

vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')
            
wavfile = open("/sd/L-R.wav", "rb")
wav = audiocore.WaveFile(wavfile)          

dac.play(wav)
while dac.playing:
  pass
print("stopped")