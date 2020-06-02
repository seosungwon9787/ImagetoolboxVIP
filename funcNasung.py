from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np
import math

# 그레이 스케일 
def Gray_scale(image_arr):
   
    arr=[0.299, 0.587, 0.114]  #rgb를 Grayscale로 변환하는 공식 
    gray_arr=image_arr.dot(arr)
    return gray_arr

#패딩 
def padding(gray_arr):

    image_pad = np.pad(gray_arr, 1, mode='constant', constant_values=0)

    return image_pad

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

#LoG 필터 (라플라시안 of 가우시안) 
def LoG(gaus_arr):
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

#zero-crossing #좌우상하의 각 곱이 음수인 경우 zero-crossing 함 

def zerocrossing(lap_arr):
    dims=lap_arr.shape
    n=dims[0]; m=dims[1]
    zero_arr=np.copy(lap_arr)

    for j in range(0,n-1):
        for i in range(0,m-1):
            if(((lap_arr[i-1][j]*lap_arr[i+1][j])<0)&((lap_arr[i][j-1]*lap_arr[i][j+1])<0)): #화소의 좌우 부분의 곱이 음수인 경우 
                zero_arr[i][j]=255 #2차 미분값이 0인 경우 화이트 출력
            else:
                zero_arr[i][j]=0 #2차 미분값이 0이 아닌 경우 블랙 출력
            
    return zero_arr

#허프변환 (영상의 한 점을 거리와 각도 공간으로 바꾸는 과정)

def hough(image_arr, lap_arr):

    kThreshHoldLine=50 #직선을 찾기 위한 임곗값으로, 직선을 구성하는 점의 최소한 개수
    dims=lap_arr.shape 
    n=dims[0]; m=dims[1] # n*m배열 
    hou_arr=np.copy(lap_arr) #입력 에지 이미지
    rho=0 #이미지의 최대 대각선 길이 

    for i in range(0,n-1): #이미지의 높이
        for j in range(0,m-1): #이미지의 너비
            if(lap_arr[i][j]==255): #엣지인 경우
                for angle in range(0,180-1): #angle의 범위는 0~180도에서 1단위로 설정
                    rho= np.sin(angle)*i + np.cos(angle)*j  #직선의 방정식 x=i, y=j 
                                                            #angle은 원점에서 직선에 수직선을 그렸을 때 y축과 이루는 각도의 크기 
                                                            #rho는 원점에서 직선까지의 수직의 거리 

                    hou_arr[angle][rho]+=1 #직선을 구성할 가능성이 있을 경우, 1씩 누적하여 투표 

    for i in range(0,n-1):
        for j in range(0,m-1):
             if(hou_arr[i][j] >= kThreshHoldLine): #임곗값 이상의 점의 수로 구성된 직선 추출
                 image_arr[i][j]=[255,0,0]  

    # for angle in range(0,180-1):
    #     for r in range(0, rho):
    #         if(hou_arr[angle][r] >= kThreshHoldLine): #임곗값 이상의 점의 수로 구성된 직선 추출
    #             isTrueLine = True
    #             for dAngle in range(-1,1):
    #                 for dRho in range(-1,1):
    #                     if(hou_arr[angle+dAngle][r+dRho]>hou_arr[angle][r]):
    #                         isTrueLine=False
                          
    #                 if(isTrueLine==True):
    #                     image_arr[angle][r]=[255,0,0]              

    return image_arr

#코너 검출
def corner(image_arr):

    cor_arr

    return cor_arr



#1. 엣지 검출

def EdgeDetection(image):
    image_arr = qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    gray_arr=Gray_scale(image_arr) #그레이 스케일 
    gray_arr=padding(gray_arr) #패딩
    #gaus_arr=Gaussian_filter(gray_arr) #가우시안 필터
    lap_arr=LoG(gray_arr) #라플라시안 of 가우시안 필터
    print("라플라시안 필터 적용 후 배열")
    print(lap_arr)
    #zero_arr = zerocrossing(lap_arr)
    print("제로크로싱 적용 후 배열")
    #print(zero_arr)
    image=qimage2ndarray.array2qimage(lap_arr, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환   
    
    return qPixmapVar

#2. 직선 검출

def HoughTransform(image):
    image_arr=qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    gray_arr=Gray_scale(image_arr) #그레이 스케일
    gray_arr=padding(gray_arr) #패딩
    #gaus_arr=Gaussian_filter(gray_arr) #가우시안 필터
    lap_arr=LoG(gray_arr) #라플라시안 필터 
    print(lap_arr.shape, "라플라시안 필터 적용 배열") 
    hou_arr=hough(image_arr, lap_arr)  #허프 변환
    image=qimage2ndarray.array2qimage(hou_arr, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환  

    return qPixmapVar

#3. 코너 검출

def Harris_CornerDetection(image):
    image_arr=qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    cor_arr=corner(image_arr)
    image=qimage2ndarray.array2qimage(cor_arr, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환  

    return qPixmapVar

