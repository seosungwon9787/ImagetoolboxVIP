from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np


def Preprocessing(image):
    image_arr = qimage2ndarray.rgb_view(image)

    #Grayscale
    gray_arr = [0.2890, 0.5870, 0.1140]
    image_gray = np.dot(image_arr, gray_arr)

    #Padding
    image_pad = np.pad(image_gray, 1, mode='constant', constant_values=0)

    #Smoothing
    kenel = np.array([[1/273,4/273,7/273,4/273,1/273],
                      [4/273,16/273,26/273,16/273,4/273],
                      [7/273,26/273,41/273,26/273,7/273],
                      [4/273,16/273,26/273,16/273,4/273],
                      [1/273,4/273,7/273,4/273,1/273]])

    a = image_pad.shape[0]-kenel.shape[0] + 1
    b = image_pad.shape[1]-kenel.shape[1] + 1
    result2 = []
    for row in range(a):
        for column in range(b):
            result1 = image_pad[ row : row + kenel.shape[0], column : column + kenel.shape[1] ] * kenel
            result2.append(np.sum(result1))
    result = np.array(result2).reshape(a,b)


    image_after = qimage2ndarray.array2qimage(result, normalize=False)

    return QPixmap.fromImage(image_after)
