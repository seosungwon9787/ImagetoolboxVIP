from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np
from numpy import pi, exp, sqrt

#가우시안 마스크
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

#필터적용
def filter(mask, scale, image):
    # 패딩
    npad = int(scale / 2)
    pad = ((npad, npad), (npad, npad))
    image_padding = np.pad(image, pad, 'constant', constant_values=(128))
    x, y = image.shape
    filter_arr = np.zeros(shape=(x + 2 * npad, y + 2 * npad))
    for i in range(npad, x + npad):
        for j in range(npad, y + npad):
            for k in range(0, scale):
                for s in range(0, scale):
                    filter_arr[i, j] = filter_arr[i, j] + (mask[k, s]) * image_padding[i - npad + k, j - npad + s]
    #여백제거
    for i in range(1, npad+1):
        filter_arr=np.delete(filter_arr,0,axis=0)
        filter_arr = np.delete(filter_arr, 0, axis=1)

        m,n=filter_arr.shape
        filter_arr = np.delete(filter_arr, m-1, axis=0)
        filter_arr = np.delete(filter_arr, n-1, axis=1)

    return filter_arr

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

    #가우시안 마스크 생성 및 적용
    scale = 5 #로딩시간이 오래걸린다면 scale=3으로 변경
    gaussian_mask = gaussian(scale, 1)
    gaussian_arr=filter(gaussian_mask,scale,grayscale)

    #라플라시안 마스크 및 적용
    laplacian1_mask=np.array([[-1,-1,-1],
                              [-1,8,-1],
                              [-1,-1,-1]])
    laplacian_mask2 = np.array([[0, 0, -1, 0, 0],
                                [0, -1, -2, -1, 0],
                                [-1, -2, 16, -2, -1],
                                [0, -1, -2, -1, 0],
                                [0, 0, -1, 0, 0]])

    #시간이 로래걸린다면 laplacian_arr=filter(laplacian_mask1,3,gaussian_arr)으로 변경
    laplacian_arr=filter(laplacian_mask2,5,gaussian_arr)

    image = qimage2ndarray.array2qimage(laplacian_arr, normalize=False)
    qPixmapVar = QPixmap.fromImage(image)
    return qPixmapVar

