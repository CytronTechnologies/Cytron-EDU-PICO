## OLED Animation  
To begin creating the animation, start by obtaining a GIF file. You can easily generate a GIF using the website [EZIGIF](https://ezgif.com/maker).  

To transform the GIF file into a BMP image, you need Python (not the Circuitpython). You can employ the Python environment already integrated into the Thonny IDE by selecting ``Local Python 3`` on the bottom right on the IDE.

Next, proceed with the installation of necessary Python libraries:  
- Pillow-PIL
- numpy

To install on Thonny need to navigate to ``Tools>Manage packages...``. Search the libraries and install it.

Ensure that the GIF file resides in the same directory as your Python file. Then run ``convert_gif_to_bmp.py`` to convert the GIF into a BMP image.
Set below parameter to adjust the image:
```
GIF_FILENAME = "intro_cytron.gif"
BW_THRESHOLD = 90
OUTPUT_SIZE = (128,64)
INVERT_COLOUR = False
```

Copy the BMP image on your Circuitpython Drive and run the code ``run_animation.py``. Remember to edit the parameter below if you made any changes:  
```
BMP_FILENAME = "intro_cytron_20_frames.bmp"
SPRITE_SIZE = (128, 64)
BMP_FRAMES = 20
```
