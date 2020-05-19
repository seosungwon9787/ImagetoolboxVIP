from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np
from numpy import pi, exp, sqrt


def gaussian(scale, sigma):
    mask = np.ones(shape=(scale, scale))
    sum = 0
    for i in range(0, scale):
        for j in range(0, scale):
            mask[i, j] = exp((-i * i - j * j) / (2 * sigma * sigma))
            mask[i, j] = mask[i, j] / (2 * 3.14 * sigma * sigma)
            sum += mask[i, j]
    mask = mask / sum
    return mask

def EdgeDetection(image):
    #grayscale
    image_arr=qimage2ndarray.rgb_view(image)
    gray_weights=[0.2989, 0.5870, 0.1140]
    grayscale=np.dot(image_arr[...,:3],gray_weights)

    #mask= np.array([[1 / 273, 4 / 273, 7 / 273, 4 / 273, 1 / 273],
    #                [4 / 273, 16 / 273, 28 / 273, 16 / 273, 4 / 273],
    #                [7 / 273, 26 / 273, 41 / 273, 26 / 273, 7 / 273],
    #                [4 / 273, 16 / 273, 28 / 273, 16 / 273, 4 / 273],
    #                [1 / 273, 4 / 273, 7 / 273, 4 / 273, 1 / 273]])
    #가우시안 필터 생성
    scale = 5
    mask2 = gaussian(scale, 2)

    #패딩
    npad = int(scale / 2)
    pad = ((npad, npad), (npad, npad))
    image_padding = np.pad(grayscale, pad, 'constant', constant_values=(128))

    #가우시안 필터 적용
    x, y = grayscale.shape
    gaussian_arr = np.zeros(shape=(x + 2 * npad, y + 2 * npad))
    for i in range(npad, x + npad):
        for j in range(npad, y + npad):
            for k in range(0, scale):
                for s in range(0, scale):
                    gaussian_arr[i, j] = gaussian_arr[i, j] + (mask2[k, s]) * image_padding[i - npad + k, j - npad + s]

    #여백 제거
    for i in range(1, npad+1):
        gaussian_arr=np.delete(gaussian_arr,0,axis=0)
        gaussian_arr = np.delete(gaussian_arr, 0, axis=1)

        m,n=gaussian_arr.shape
        gaussian_arr = np.delete(gaussian_arr, m-1, axis=0)
        gaussian_arr = np.delete(gaussian_arr, n-1, axis=1)

    image = qimage2ndarray.array2qimage(gaussian_arr, normalize=False)
    qPixmapVar = QPixmap.fromImage(image)
    return qPixmapVar
