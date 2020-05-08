from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np

#EdgeDetection

def EdgeDetection(image):
    image_array = qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    print(image_array)
    print(image_array.shape)
    #rgb를 Grayscale로 변환하는 공식 
    arr=np.array([0.299,0.587,0.114]) 
    image_array=arr*image_array #rgb값을 저장하는 배열에 공식을 대입함 
    print(image_array)
    image=qimage2ndarray.array2qimage(image_array, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환   
    
    return qPixmapVar
