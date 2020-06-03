from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np
import math
import cv2

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

    for i in range(n):
        for j in range(m):
            gaus_arr[i][j]=0
    
    for i in range(1,n-1):
        for j in range(1,m-1):
            gaus_arr[i,j]+=(gray_arr[i-1,j]+gray_arr[i+1,j]+gray_arr[i,j-1]+gray_arr[i,j+1])*0.5
            gaus_arr[i,j]+=(gray_arr[i-1,j-1]+gray_arr[i-1,j+1]+gray_arr[i+1,j-1]+gray_arr[i+1,j+1])*0.25     
            gaus_arr[i,j]+=gray_arr[i][j]       
    gaus_arr/=4.
    return gaus_arr




#LoG 필터 (라플라시안 of 가우시안) 
def Laplacian(gaus_arr):
    # 커널 형식 [0,1,0],[1,-4,1],[0,1,0]
    
    dims=gaus_arr.shape
    n=dims[0]; m=dims[1]
    lap_arr=np.copy(gaus_arr)

    for i in range(1,n-1):
        for j in range(1,m-1):
            lap=gaus_arr[i-1][j-1]+gaus_arr[i][j-1]+gaus_arr[i+1][j-1]+gaus_arr[i-1][j]+gaus_arr[i][j]*(-8)+gaus_arr[i+1][j]+gaus_arr[i-1][j+1]+gaus_arr[i][j+1]+gaus_arr[i+1][j+1]            
           
            lap_arr[i][j]=lap
    
    return lap_arr

#zero-crossing #좌우상하의 각 곱이 음수인 경우 zero-crossing 함 

def zerocrossing(lap_arr):
    dims=lap_arr.shape
    n=dims[0]; m=dims[1]
    zero_arr=np.copy(lap_arr)
    
    for i in range(n):
        for j in range(m):
            zero_arr[i][j]=0

    for i in range(1,n-1):
        for j in range(1,m-1):
            if(lap_arr[i][j]>=0): #양수인 경우
                    
                if(((lap_arr[i-1][j]*lap_arr[i+1][j])<0) or ((lap_arr[i][j-1]*lap_arr[i][j+1])<0)): #화소의 좌우 부분의 곱이 음수인 경우 or
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

    # for angle in range(0,180-1):
    #     for R in range(0, rho):

    for angle in range(0,n-1):
        for R in range(0, m-1):

            if(hou_arr[angle][R] >= kThreshHoldLine): #임곗값 이상의 점의 수로 구성된 직선 추출
                isTrueLine = True
                for dAngle in range(-1,1):
                    for dRho in range(-1,1):
                        if(hou_arr[angle+dAngle][R+dRho]>hou_arr[angle][R]):
                            isTrueLine=False
                          
                    if(isTrueLine==True):
                        image_arr[angle][R]=[0,255,0] #초록색으로 점표시              

    return image_arr


def hough2(image_arr, zero_arr):

    kThreshHoldLine=400 #직선을 찾기 위한 임곗값으로, 직선을 구성하는 점의 최소한 voting개수
    dims=zero_arr.shape 
    n=dims[0]; m=dims[1] # n*m배열 
    
    angle=0
    rho=0 
    Range=int(math.sqrt((n*n)+(m*m)))  #이미지의 최대 대각선 길이 (a제곱+b제곱=대각선의 제곱)
    rhoSize=Range*2
    Theta=180
    PI=3.14159265
    
    angle_list=[] #임곗값을 넘는 p와 angle값 저장하기 위함 
    rho_list=[]

    Hough = [[0 for col in range(Range)] for row in range(180)] #voting 배열 초기화 
    
    for i in range(0,n-1): #이미지의 높이
        for j in range(0,m-1): #이미지의 너비
            if(zero_arr[i][j]==255): #엣지인 경우
                for angle in range(0,180-1): #angle의 범위는 0~180도에서 1단위로 설정
                    rho= int(np.sin(angle)*i + np.cos(angle)*j)  #직선의 방정식 x=i, y=j 
                                                            #angle은 원점에서 직선에 수직선을 그렸을 때 y축과 이루는 각도의 크기 
                                                            #rho는 원점에서 직선까지의 수직의 거리 

                    Hough[angle][rho]+=1 #직선을 구성할 가능성이 있을 경우, 1씩 누적하여 투표 
                    #Hough 도메인의 값은 각 직선위의 엣지 픽셀의 개수를 의미 

    for angle in range(0,180-1):
            for R in range(-(Range-1), Range-1):

                if(Hough[angle][R] >= kThreshHoldLine): #누적 투표량이 임곗값 이상인 거리와 각도 
                    isTrueLine = True
                    
                    for dAngle in range(-1,1):
                        for dRho in range(-1,1):
                            if(Hough[angle+dAngle][R+dRho]>Hough[angle][R]):
                                isTrueLine=False
                            
                            if(isTrueLine==True): #임곗값 이상의 점의 수로 구성된 직선 추출
                                angle_list.append(angle)
                                rho_list.append(R)
                                
    print(angle_list)
    print("***********************")
    print(rho_list)
    print("***********************")
    
    for i in range(len(angle_list)):
        print(Hough[angle_list[i]][rho_list[i]])

    img=np.zeros((n,m,3),np.uint8)
    image_arr=image_arr.astype(np.uint8)

    for i in range(len(angle_list)):
        a=np.cos(angle_list[i])
        b=np.sin(angle_list[i])
        x0=a*rho_list[i]
        y0=b*rho_list[i]
        x1=int(x0+1000*(-b))
        y1=int(y0+1000*a)
        x2=int(x0-1000*(-b))
        y2=int(y0-1000*a)

        img=cv2.line(image_arr,(x1,y1),(x2,y2),(0,255,0),1) #직선 표시 

    return img
#코너 검출
def corner(gaus_arr):

    ix, iy = np.gradient(gaus_arr) #1차미분계산 
   
    ix2 = (ix ** 2)
    iy2 = (iy ** 2)
    ixiy = (ix * iy)

    detM = (ix2 * iy2) - (ixiy * ixiy) #det M
    traceM = (ix2 + iy2) #trance(M)
    k=0.04 #k값은 보통 0.04로 함 
    R = detM + k * (traceM ** 2) #현재 윈도우의 R값 𝑅 = det 𝑀 − 𝑘(𝑡𝑟𝑎𝑐𝑒(𝑀))2
 
    corners = []
    
    for i in range(1, R.shape[0] - 1):
        for j in range(1, R.shape[1] - 1):
            if R[i][j] >= max(R[i-1][j-1], R[i][j-1], R[i+1][j-1], R[i-1][j+1], R[i][j+1], R[i+1][j+1], R[i-1][j], R[i+1][j]): #센터값이 전체보다 더 클 경우 
                R[i][j]=round(R[i][j],5) #소수점 5째자리까지만 
                if(R[i][j]>(0.00)): #임곗값 
                    corners.append((i, j, R[i][j])) #2개 고유값이이 둘다 클 경우, 코너점임 

    #return corners

    dims=gaus_arr.shape
    n=dims[0]; m=dims[1]
    cor_arr=np.copy(gaus_arr)
    corners_2=[]
    for i in range(1,n-1):
        for j in range(1,m-1):
            lap=gaus_arr[i-1][j-1]+gaus_arr[i][j-1]+gaus_arr[i+1][j-1]+gaus_arr[i-1][j]+gaus_arr[i][j]*(-8)+gaus_arr[i+1][j]+gaus_arr[i-1][j+1]+gaus_arr[i][j+1]+gaus_arr[i+1][j+1]            
            if(lap>=max(gaus_arr[i-1][j-1], gaus_arr[i][j-1], gaus_arr[i+1][j-1], gaus_arr[i-1][j+1], gaus_arr[i][j+1], gaus_arr[i+1][j+1], gaus_arr[i-1][j], gaus_arr[i+1][j])):  
                corners_2.append((i,j))
    
    corners_3=[]
    dims=gaus_arr.shape
    n=dims[0]; m=dims[1]
    cor2_arr=np.copy(gaus_arr)
    for i in range(n):
        for j in range(m):
            cor2_arr[i][j]=0
    
    for i in range(1,n-1):
        for j in range(1,m-1):
            
            if(cor2_arr[i][j]>=max(gaus_arr[i-1][j-1], gaus_arr[i][j-1], gaus_arr[i+1][j-1], gaus_arr[i-1][j+1], gaus_arr[i][j+1], gaus_arr[i+1][j+1], gaus_arr[i-1][j], gaus_arr[i+1][j])):  
                corners_3.append((i,j))

    return corners_2

def corner_image(image_arr, corners):
    x = [corner[0] for corner in corners]
    y = [corner[1] for corner in corners]

    for i in range(len(x)):
            image_arr[int(x[i])][int(y[i])]=(0,255,0)
    
    return image_arr

#1. 엣지 검출

def EdgeDetection(image):
    image_arr = qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    gray_arr=Gray_scale(image_arr) #그레이 스케일 
    gray_arr=padding(gray_arr) #패딩
    gaus_arr=Gaussian_filter(gray_arr) #가우시안 필터
    for i in range(80):
        gaus_arr=Gaussian_filter(gaus_arr) #가우시안 필터
    
    lap_arr=Laplacian(gaus_arr) #라플라시안 필터
    print(lap_arr)
    zero_arr = zerocrossing(lap_arr)
    #print(zero_arr)
    image=qimage2ndarray.array2qimage(zero_arr, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환   
    
    return qPixmapVar

#2. 직선 검출

def HoughTransform(image):
    image_arr=qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    gray_arr=Gray_scale(image_arr) #그레이 스케일
    gray_arr=padding(gray_arr) #패딩
    gaus_arr=Gaussian_filter(gray_arr) #가우시안 필터
    #for i in range(5):
     #   gaus_arr=Gaussian_filter(gaus_arr) #가우시안 필터
    lap_arr=Laplacian(gaus_arr) #라플라시안 필터 엣지검출함
    zero_arr = zerocrossing(lap_arr) 
    hou_arr=hough2(image_arr, zero_arr)  #허프 변환
    image=qimage2ndarray.array2qimage(hou_arr, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환  

    return qPixmapVar

#3. 코너 검출

def Harris_CornerDetection(image):
    image_arr=qimage2ndarray.rgb_view(image) #Qimage를 numpy로 변환
    gray_arr=Gray_scale(image_arr) #그레이 스케일
    gray_arr=padding(gray_arr) #패딩
    gaus_arr=Gaussian_filter(gray_arr) #가우시안 필터
    cor_arr=corner(gaus_arr)
    corner_result=corner_image(image_arr,cor_arr)
    image=qimage2ndarray.array2qimage(corner_result, normalize=False) #numpy를 Qimage로 변환
    qPixmapVar = QPixmap.fromImage(image) #Qimage를 Qpixmap으로 변환  

    return qPixmapVar

