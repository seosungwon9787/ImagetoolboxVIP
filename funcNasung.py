from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np

#EdgeDetection

def EdgeDetection(image):
    image_array = qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    print(image_array) #그레이 스케일 전 
    print(image_array.shape)
    #rgb를 Grayscale로 변환하는 공식 
    arr=[0.299, 0.587, 0.114]
    GrayScale=image_array.dot(arr)
    print(GrayScale) #그레이 스케일 후 

    #가우시안 필터

    image=qimage2ndarray.array2qimage(GrayScale, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환   
    
    return qPixmapVar
