"""
DESCRIPTION:
This example code will play the audio file from
Micro SD Card on EDU PICO and control the audio
using Gesture sensor APDS9960.

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io
"""
import time, board
import busio
import sdcardio
import storage
import audiocore
import audiopwmio
import random
import digitalio
import adafruit_ssd1306
import os
from adafruit_apds9960.apds9960 import APDS9960

#Define the i2C GPIOsvand Oled Display.
i2c = busio.I2C(board.GP5, board.GP4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

#Initialize the APDS9960 Gesture Sensor
multi_sensor = APDS9960(i2c)
multi_sensor.enable_proximity = True
multi_sensor.enable_gesture = True

#Initialize Button A & B
buttonA = digitalio.DigitalInOut(board.GP0)
buttonB = digitalio.DigitalInOut(board.GP1)

#Define Audio Left and Right Channel
dac = audiopwmio.PWMAudioOut(left_channel=board.GP20, right_channel=board.GP21)

#Initialize SD Card GPIOs
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = board.GP17
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')

#Oled Display Startup Menu
oled.fill(0)
oled.show()
oled.text("Press Yellow to Start!", 1, 45, 1)
oled.text("Press Blue to Menu!", 10, 20, 1)
oled.show()

button_init = False

buttonA_release = True
buttonB_release = True
buttonA_pressed = False
buttonB_pressed = False

#Define Music Filename // Put ".wav" at last of your music name. example = Birthday.wav
song_array = ["Music_1.wav","Music_2.wav","Music_3.wav","Music_4.wav"]

#Define First music you want it To be play
wavfile = open("/sd/Music_1.wav", "rb")
wav0 = audiocore.WaveFile(wavfile)

def waveFiles(waveNames):
    wavArray = []
    for i in waveNames:
        wavfile1 = open("/sd/"+i, "rb")
        wav1 = audiocore.WaveFile(wavfile1)
        wavArray.append(wav1)
    return wavArray

#Music Track Sort
wavArray = waveFiles(song_array)
lengthArray = len(wavArray)
counter = 0
start_song = False

#List all Music in the SD Card (.wav only)
wav_filename = []
for filename in os.listdir('/sd'):
    if filename.lower().endswith('.wav') and not filename.startswith('.'):
        wav_filename.append(filename[:-4 ])

wav_filename.sort()  
for wave in wav_filename:
    print(wave)
              
while True:
    gesture = multi_sensor.gesture()

    if buttonA.value == False and buttonA_release == True:
        buttonA_release = False
    elif buttonA.value == True and buttonA_release == False:
        buttonA_release = True
        buttonA_pressed = True
        start_song = True
        print("Playing First Song")
        oled.fill(0)
        oled.text("Playing!", 45, 10, 1)
        oled.text("Music: {}".format(wav_filename[counter]), 1, 30, 1)
        oled.show()
        dac.play(wav0)
        
    if buttonB.value == False and buttonB_release == True:
        buttonB_release = False
    elif buttonB.value == True and buttonB_release == False:
        buttonB_release = True
        buttonB_pressed = True
        print("Opening Menu List")
        oled.fill(0)
        oled.text("Slide Down : Pause", 1, 10, 1)
        oled.text("Slide Up   : Play", 1, 20, 1)
        oled.text("Slide Right: Next", 1, 30, 1)
        oled.text("Slide Left : Previous", 1, 40, 1)
        oled.text("Press Yellow To Start", 1, 55, 1)
        oled.show()
        
    if start_song == True:
        if gesture == 1:#Up
            print("Resume Song")
            dac.pause()
            oled.fill(0)
            oled.text("Resume!", 45, 30, 1)
            oled.show()
            time.sleep(0.5)
            oled.fill(0)
            oled.text("Playing!", 45, 10, 1)
            oled.text("Music: {}".format(wav_filename[counter]), 1, 30, 1)
            oled.show()
            dac.resume()
            
        if gesture == 2:#Down
            print("Pause Song")
            dac.pause()
            oled.fill(0)
            oled.text("Pause!", 45, 30, 1)
            oled.show()
            time.sleep(0.5)
            oled.fill(0)
            oled.text("Pause!", 45, 10, 1)
            oled.text("Music: {}".format(wav_filename[counter]), 1, 30, 1)
            oled.show()
            
        if gesture == 3:#left
            print("Previous Song")
            dac.pause()
            counter-=1
            if counter < 0:
                counter = lengthArray-1
            dac.play(wavArray[counter])
            dac.pause()
            oled.fill(0)
            oled.text("Previous!", 45, 10, 1)
            oled.text("Music: {}".format(wav_filename[counter]), 1, 30, 1)
            oled.text("Slide Up To Play!", 15, 50, 1)
            oled.show()           
            
        if gesture == 4:#right
            print("Next Song")
            dac.pause()
            counter+=1
            if counter > lengthArray-1:
                counter = 0
            dac.play(wavArray[counter])
            dac.pause()
            oled.fill(0)
            oled.text("Next!", 45, 10, 1)
            oled.text("Music: {}".format(wav_filename[counter]), 1, 30, 1)
            oled.text("Slide Up To Play!", 15, 50, 1)
            oled.show()

        if not dac.playing:
            counter+=1
            if counter > lengthArray-1:
                counter = 0
            dac.play(wavArray[counter])
            dac.pause()
            oled.fill(0)
            oled.text("Playing!", 45, 10, 1)
            oled.text("Music: {}".format(wav_filename[counter]), 1, 30, 1)
            oled.show()
            dac.resume()