"""
DESCRIPTION:
This example code will convert the GIF file to
BMP image by sorting each frames horizontally.

AUTHOR   : Cytron Technologies Sdn Bhd
WEBSITE  : www.cytron.io
EMAIL    : support@cytron.io

REFERENCE:
Code adapted from educ8s.tv:
https://educ8s.tv/oled-animation/
"""
from PIL import Image, ImageOps
import numpy

INPUT_FILENAME = "intro_cytron.gif"
BW_THRESHOLD = 90
OUTPUT_SIZE = (128,64)
INVERT_COLOUR = False

gif = Image.open(INPUT_FILENAME)
print(f"Size: {gif.size}")
print(f"Frames: {gif.n_frames}")

OUTPUT_FILENAME = f"{INPUT_FILENAME[:-4]}_{gif.n_frames}_frames.bmp"

sprite_sheet = Image.new("L", (OUTPUT_SIZE[0]*gif.n_frames, OUTPUT_SIZE[1]),3)

def binarize_image(image_file, threshold):
    """Binarize an image."""
    image = image_file.convert('L')  # convert image to monochrome
    # Binarize a numpy array
    numpy_array = numpy.array(image)
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0       
    image =  Image.fromarray(numpy_array)
    return image


def compress_bmp(img):
    """
    Compresses a BMP image by setting pixels with a value of 255 to True (1) and all other values to False (0),
    and saves the result as a 1-bit per pixel BMP image.
    """
    image_data = numpy.array(img)
    bool_data = (image_data == 255)
    compressed_data = bool_data.astype(numpy.uint8)
    compressed_img = Image.fromarray(compressed_data * 255, 'L').convert('1')
    return compressed_img

# Arrange the each gif frame on the horizontal images
for frame in range(0, gif.n_frames):
    gif.seek(frame)
    extracted_frame = gif.resize(OUTPUT_SIZE)
    extracted_frame = binarize_image(extracted_frame, BW_THRESHOLD)
    if INVERT_COLOUR:
        extracted_frame = ImageOps.invert(extracted_frame)
    position = (frame*OUTPUT_SIZE[0],0)
    sprite_sheet.paste(extracted_frame, position)
    
sprite_sheet.show()

# Use the function to compress the image
compressed_img = compress_bmp(sprite_sheet)

# Save the compressed image as BMP
compressed_img.save(OUTPUT_FILENAME, 'BMP')


