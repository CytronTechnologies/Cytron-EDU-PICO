"""
DESCRIPTION:
This example code will save the data on the
Micro SD Card on EDU PICO.

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io
"""
import time, board
import busio, sdcardio, storage
import digitalio
import microcontroller
import os

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = board.GP17

# Alternative pin assignment
# spi = board.SD_SPI
# cs = board.SD_CS

sd = sdcardio.SDCard(spi, cs)

vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')

sd_dir = '/sd/'
file_name = 'temperature.csv'
max_file_size = 100*10**6 #100x10^6 = 100MB

with open(sd_dir+file_name, "a") as datalog:
    while True:
        file_size = os.stat(sd_dir+file_name)[6]
        if file_size < max_file_size:
            temp = microcontroller.cpu.temperature
            datalog.write('{0:.1f}\n'.format(temp))
            datalog.flush()
            led.value = not led.value
            time.sleep(1)
        else:
            led.value = True