#   Michael Reder - 10.01.2019
#   Project Sem 3
#   File to resize an folder of pictures to an size of 224x224
#   Important to change the size if the model takes other sizes
#   You can add multiple SubFolder but it will safed in one Folder


#   Settings


import os

import cv2
from tqdm import tqdm

FROM_DATADIR = "data/change"
IMG_SIZE = 224


def resize_data():
    path = os.path.join(FROM_DATADIR)  # create path

    counter = 0
    for img in tqdm(os.listdir(path)):  # iterate over each image per dogs and cats
        try:
            img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_COLOR)  # convert to array
            data = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
            # plt.imshow(data, cmap='gray')
            # plt.show()

            checkpath = os.path.join(path, 'resized/')
            if not os.path.exists(checkpath):
                os.makedirs(checkpath)

            filename = 'resize' + str(counter) + '.jpg'
            cv2.imwrite(os.path.join(checkpath, filename), data)
            cv2.waitKey(0)
            counter += 1
        except Exception as e:  # in the interest in keeping the output clean...
            pass
        # except OSError as e:
        #    print("OSErrroBad img most likely", e, os.path.join(path,img))
        # except Exception as e:
        #    print("general exception", e, os.path.join(path,img))


resize_data()
