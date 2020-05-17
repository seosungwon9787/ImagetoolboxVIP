from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np

# 그레이 스케일 
def Gray_scale(image_arr):
   
    arr=[0.299, 0.587, 0.114]  #rgb를 Grayscale로 변환하는 공식 
    gray_arr=image_arr.dot(arr)
    return gray_arr

# 가우시안 필터 
def Gaussian_filter(gray_arr):

    dims=gray_arr.shape
    n=dims[0]; m=dims[1] 
    gaus_arr=np.copy(gray_arr)
    for j in range(1,n-1):
        for i in range(1,m-1):
            gaus_arr[j,i]+=(gray_arr[j-1,i]+gray_arr[j+1,i]+gray_arr[j,i-1]+gray_arr[j,i+1])*0.5
            gaus_arr[j,i]+=(gray_arr[j-1,i-1]+gray_arr[j-1,i+1]+gray_arr[j+1,i-1]+gray_arr[j+1,i+1])*0.25            
    gaus_arr/=4.
    return gaus_arr

#라플라시안 필터 
def Laplacian(gaus_arr):
    # 커널 형식 [0,1,0],[1,-4,1],[0,1,0]
    
    dims=gaus_arr.shape
    n=dims[0]; m=dims[1]
    lap_arr=np.copy(gaus_arr)

    for j in range(1,n-1):
        for i in range(1,m-1):
            lap=gaus_arr[i][j-1]+gaus_arr[i-1][j]+gaus_arr[i][j]*(-4)+gaus_arr[i+1][j]+gaus_arr[i][j+1]

            if(lap>255):
                lap=255
            if(lap<0):
                lap=0

            lap_arr[i][j]=lap
    
    return lap_arr


#엣지 검출

def EdgeDetection(image):
    image_arr = qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    gray_arr=Gray_scale(image_arr) #그레이 스케일 
    gaus_arr=Gaussian_filter(gray_arr) #가우시안 필터
    lap_arr=Laplacian(gaus_arr) #라플라시안 필터 
    image=qimage2ndarray.array2qimage(lap_arr, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환   
    
    return qPixmapVar
