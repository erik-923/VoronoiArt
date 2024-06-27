"""
Erik Blix
This file contains code to read the GAOutput.txt file and create a gif of the evolution process.
The gif shows the progress of the evolution by combining images of the best painting every 10 generations.
The gif also shows the generation in the top left corner and updates every 500 generations.
Ex: 0, 500, 1000, ...
"""

import csv
import imageio
from PIL import Image, ImageDraw, ImageFont
from painting import Painting

def add_text_to_image(img, text):
    # create a drawing object
    draw = ImageDraw.Draw(img)

    # choose a font, size, color, and location
    font = ImageFont.load_default()
    font = ImageFont.truetype("arial.ttf", 100)
    position = (10, 10)
    text_color = (255, 255, 255)

    # add text to the image
    draw.text(position, text, font=font, fill=text_color)
    return img

dimensions = Image.open('Testing Images/original_image.png').size
images = []
epoch = '1'
with open('GAoutput.txt', 'r') as datafile:
    plotting = csv.reader(datafile, delimiter=' ')
    for row in plotting:
        # use this to change the number of generations per image
        if int(row[0]) % 10 == 0:
            if int(row[0]) % 500 == 0:
                epoch = row[0]
            img = Painting(row[3], *dimensions).getImage()
            img = add_text_to_image(img, epoch)
            images.append(img)

gif_path = "output/output.gif"

# save the images as a GIF
imageio.mimsave(gif_path, images, fps=25)
