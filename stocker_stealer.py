# Michael Reder - 10.01.2019
# Pic Stealer
# Pssscht keep it a secret
# Parse an html after <src> and download the pics, so it will be possible to download from sites like shuterstock
# !!!Important!!!
# To not get the same image for the same page twice update the counter here!!!
# Site Counter for: https://www.shutterstock.com/search?page=2&searchterm=pushups
# Counter 8 <- is loaded 9 would be next
# Change the Counter for the name if you safe it in the same folder!!!
import cv2
import os
import urllib
from urllib.request import urlopen
import requests #pip install requests
import matplotlib.pyplot as plt    #python -mpip install matplotlib
from imageCropper import crop

from bs4 import BeautifulSoup #pip install beautifulsoup4

#URL_TO_SITE = "https://www.shutterstock.com/search?searchterm=pushups&search_source=base_search_form&language=de&page=1&sort=popular&image_type=all&measurement=px&safe=true"
URL_TO_SITE = "https://www.shutterstock.com/search?page=14&searchterm=pushups&measurement=px&sort=popular&image_type=all&safe=true&search_source=base_search_form&language=de&saveFiltersLink=true&section=1"
PATH_TO_SAFE = "C:/Users/reder/Desktop"
# PATH_TO_SAFE = "/Users/fneus/OneDrive/Dokumente/stock/" <- example
IMG_SIZE = 224


# Print iterations progress
# For style matters
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def loading_HTML():
    f = urlopen(URL_TO_SITE)
    siteContent = f.read()
    print("Comander: Soldier! I have an quest for you i need some html. *snivel*")
    return siteContent


def parsing_HTML():
    siteContent = loading_HTML()
    print("Soldier: I have the HTML Code i will parse it!")
    print("Comander: Fck man HTML is no code it is a markup, but Fine do it!")

    soup = BeautifulSoup(siteContent, "html.parser")
    tags = soup.findAll('img')
    return set(tag['src'] for tag in tags)
    # print("\n".join(set(tag['src'] for tag in tags)))


def downloading_pic():
    counter = 1207

    image_src_list = parsing_HTML()

    # creats path to safe
    path = os.path.join(PATH_TO_SAFE)  # create path
    checkpath = os.path.join(path, 'loadedData/')
    if not os.path.exists(checkpath):
        os.makedirs(checkpath)

    array_length = len(image_src_list)
    #printProgressBar(0, array_length, prefix='Progress:', suffix='Complete', length=50)
    # loop over the array of source
    for img_url in image_src_list:
        img_data = requests.get(img_url).content
        with open('tmpImageData.jpg', 'wb') as handler:
            handler.write(img_data)

        crop("tmpImageData.jpg")
        img_array = cv2.imread("tmpImageData_cropped.jpg", cv2.IMREAD_COLOR)
        data = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        filename = 'resize' + str(counter) + '.jpg'
        cv2.imwrite(os.path.join(checkpath, filename), data)
        cv2.waitKey(0)

        os.remove("tmpImageData.jpg")
        os.remove("tmpImageData_cropped.jpg")
        # Update Progress Bar and Counter for name
        counter += 1
        #printProgressBar(counter, array_length, prefix='Progress:', suffix='Complete', length=50)
        
    print("Soldier: Everything is saved and i eliminates the last parts of your orgy!")


downloading_pic()




