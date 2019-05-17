# pip install Pillow
from PIL import Image
import os
#path = "/Users/fneus/OneDrive/Dokumente/stock/loadedData/resize1.jpg"


# Soldier: Commander, i found a way to get rid of that nasty white bar at the bottom!
def crop(image_path):

    try:
        img = Image.open(image_path).convert('RGB')
    except IOError:
        print("could not find picture")

    #img.show()
    width, height = img.size

    left = 0
    top = 0
    right = width
    bottom = height - 20
    cropped_image = img.crop((left, top, right, bottom))
    cropped_image.save("tmpImageData_cropped.jpg")

    #cropped_image.show()
