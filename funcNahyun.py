from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np

def EdgeDetection(image):
    image_arr= qimage2ndarray_rgb_view(image)
    gray_weights=[0.2989, 0.5870,0.1140]
    grayscale=np.dot(image_arr[...,:3], gray_weights)


