from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

import numpy as np

fscale=5

#그레이스케일
def Grayscale(image_arr):
   
    arr=[0.299, 0.587, 0.114]
    gray_arr=image_arr.dot(arr)
    
    return gray_arr

#가우시안
def Gaussian(gray_arr):

    h_scale=int(fscale/2)

    filter_arr=[[1,4,7,4,1],
                [4,16,26,16,4],
                [7,26,41,26,7],
                [4,16,26,16,4],
                [1,4,7,4,1]]
    filter_arr/273

    pad_scale=int(fscale/2)
    pad=((pad_scale,pad_scale),(pad_scale,pad_scale))
    image_pad = np.pad(gray_arr, pad, constant_values=(128))

    x,y=gray_arr.shape

    gaussian_arr=np.zeros((x,y))

    for i in range(pad_scale,y+pad_scale):
        for j in range(pad_scale,x+pad_scale):
            sample_pad=image_pad[j:j+fscale,i:i+fscale]
            sample_pad*filter_arr
            







    #model_arr=np.zeros(x+h_scale,x+h_scale)




