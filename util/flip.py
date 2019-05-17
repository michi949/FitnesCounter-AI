"""@package util
"""

import os

from PIL import Image


def flip_image(image_path, saved_location):
    """
    Flip or mirror the image

    :param  image_path: The path to the image to edit
    :param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_image.save(saved_location)


def main():
    image_dir = "../data/classif/squat_down"
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            print(filename)
            image = filename
            new_name = "flip_" + filename
            flip_image(os.path.join(image_dir, image), os.path.join(image_dir, new_name))
            continue
        else:
            continue


if __name__ == "__main__":
    main()
