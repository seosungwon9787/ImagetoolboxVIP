from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np

import funcBitna
import funcDongwook
import funcJunghyun
import funcJungsu
import funcNahyun
import funcNasung
import funcRosa
import funcSeungeon
import funcSungho
import funcSungwon

basic_ui = uic.loadUiType("toolbox.ui")[0]
dialog_ui = uic.loadUiType("dialog.ui")[0]

class Dialog1Class(QDialog, dialog_ui) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.filename_left = ''
        self.filename_right = ''

        self.image_left = QImage()
        self.image_right = QImage()
        
        self.pushButton.clicked.connect(self.onOKButtonClicked)
        self.pushButton_2.clicked.connect(self.getLeftfile)
        self.pushButton_3.clicked.connect(self.getRightfile)

    def onOKButtonClicked(self):
        self.accept()

    def getLeftfile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "./data")
        self.filename_left = fileName
        self.image_left = QImage(self.filename_left)
        flist = self.filename_left.split('/')
        self.pushButton_2.setText(flist[-1])
        
    def getRightfile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "./data")
        self.filename_right = fileName
        self.image_right = QImage(self.filename_right)

        flist = self.filename_right.split('/')
        self.pushButton_3.setText(flist[-1])

class WindowClass(QMainWindow, basic_ui) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.resize(1656, 750)

        self.filename_left = ''
        self.filename_right = ''
        
        self.image_left = QImage()
        self.image_right = QImage()

        self.actionCorner_detection_1.triggered.connect(lambda : self.Cornerdetection(1))
        self.actionCorner_detection_2.triggered.connect(lambda : self.Cornerdetection(2))
        self.actionCorner_detection_3.triggered.connect(lambda : self.Cornerdetection(3))
        self.actionCorner_detection_4.triggered.connect(lambda : self.Cornerdetection(4))
        self.actionCorner_detection_5.triggered.connect(lambda : self.Cornerdetection(5))
        self.actionCorner_detection_6.triggered.connect(lambda : self.Cornerdetection(6))
        self.actionCorner_detection_7.triggered.connect(lambda : self.Cornerdetection(7))
        self.actionCorner_detection_8.triggered.connect(lambda : self.Cornerdetection(8))
        self.actionCorner_detection_9.triggered.connect(lambda : self.Cornerdetection(9))
        self.actionCorner_detection_10.triggered.connect(lambda : self.Cornerdetection(10))

        self.actionHough_transtorm_1.triggered.connect(lambda : self.Houghtransform(1))
        self.actionHough_transtorm_2.triggered.connect(lambda : self.Houghtransform(2))
        self.actionHough_transtorm_3.triggered.connect(lambda : self.Houghtransform(3))
        self.actionHough_transtorm_4.triggered.connect(lambda : self.Houghtransform(4))
        self.actionHough_transtorm_5.triggered.connect(lambda : self.Houghtransform(5))
        self.actionHough_transtorm_6.triggered.connect(lambda : self.Houghtransform(6))
        self.actionHough_transtorm_7.triggered.connect(lambda : self.Houghtransform(7))
        self.actionHough_transtorm_8.triggered.connect(lambda : self.Houghtransform(8))
        self.actionHough_transtorm_9.triggered.connect(lambda : self.Houghtransform(9))
        self.actionHough_transtorm_10.triggered.connect(lambda : self.Houghtransform(10))

        self.actionEdge_detection_1.triggered.connect(lambda : self.Edgedetection(1))
        self.actionEdge_detection_2.triggered.connect(lambda : self.Edgedetection(2))
        self.actionEdge_detection_3.triggered.connect(lambda : self.Edgedetection(3))
        self.actionEdge_detection_4.triggered.connect(lambda : self.Edgedetection(4))
        self.actionEdge_detection_5.triggered.connect(lambda : self.Edgedetection(5))
        self.actionEdge_detection_6.triggered.connect(lambda : self.Edgedetection(6))
        self.actionEdge_detection_7.triggered.connect(lambda : self.Edgedetection(7))
        self.actionEdge_detection_8.triggered.connect(lambda : self.Edgedetection(8))
        self.actionEdge_detection_9.triggered.connect(lambda : self.Edgedetection(9))
        self.actionEdge_detection_10.triggered.connect(lambda : self.Edgedetection(10))

        self.actionStereo_matching_1.triggered.connect(lambda : self.Stereomatching(1))
        self.actionStereo_matching_2.triggered.connect(lambda : self.Stereomatching(2))
        self.actionStereo_matching_3.triggered.connect(lambda : self.Stereomatching(3))
        self.actionStereo_matching_4.triggered.connect(lambda : self.Stereomatching(4))
        self.actionStereo_matching_5.triggered.connect(lambda : self.Stereomatching(5))
        self.actionStereo_matching_6.triggered.connect(lambda : self.Stereomatching(6))
        self.actionStereo_matching_7.triggered.connect(lambda : self.Stereomatching(7))
        self.actionStereo_matching_8.triggered.connect(lambda : self.Stereomatching(8))
        self.actionStereo_matching_9.triggered.connect(lambda : self.Stereomatching(9))
        self.actionStereo_matching_10.triggered.connect(lambda : self.Stereomatching(10))

        self.actionFace_detection_1.triggered.connect(lambda : self.Facedetection(1))
        self.actionFace_detection_2.triggered.connect(lambda : self.Facedetectiong(2))
        self.actionFace_detection_3.triggered.connect(lambda : self.Facedetection(3))
        self.actionFace_detection_4.triggered.connect(lambda : self.Facedetection(4))
        self.actionFace_detection_5.triggered.connect(lambda : self.Facedetection(5))
        self.actionFace_detection_6.triggered.connect(lambda : self.Facedetection(6))
        self.actionFace_detection_7.triggered.connect(lambda : self.Facedetection(7))
        self.actionFace_detection_8.triggered.connect(lambda : self.Facedetection(8))
        self.actionFace_detection_9.triggered.connect(lambda : self.Facedetection(9))
        self.actionFace_detection_10.triggered.connect(lambda : self.Facedetection(10))

    def Cornerdetection(self, num):
        dialog_1 = Dialog1Class()
        ret = dialog_1.exec_()
        
        if ret:
            self.filename_left = dialog_1.filename_left
            self.filename_right = dialog_1.filename_right

            self.image_left = dialog_1.image_left
            self.image_right = dialog_1.image_right
           
            self.label_1.setGeometry(30, 30, self.image_left.width(), self.image_left.height())
            self.label_2.setGeometry(572, 30, self.image_right.width(), self.image_right.height())
            self.label_3.setGeometry(1114, 30, self.image_left.width(), self.image_left.height())
            
            qPixmapVar1 = QPixmap.fromImage(self.image_left)
            qPixmapVar2 = QPixmap.fromImage(self.image_right)
            qPixmapVar3 = QPixmap.fromImage(self.image_left)
            
            #권나성
            if num == 1:
                qPixmapVar3=funcNasung.Harris_CornerDetection(self.image_left)
                pass
            #권나성


            #권동욱
            elif num == 2:
                pass
            #권동욱


            #금빛나
            elif num == 3:
                pass
            #금빛나


            #김나현
            elif num == 4:
                pass
            #김나현


            #서성원
            elif num == 5:
                pass
            #서성원


            #손정현
            elif num == 6:
                pass
            #손정현


            #이로사
            elif num == 7:
                pass
            #이로사


            #이성호
            elif num == 8:
                pass
            #이성호


            #한정수
            elif num == 9:
                pass
            #한정수


            #황승언
            else :
                pass
            #황승언

            
            self.label_1.setPixmap(qPixmapVar1)
            self.label_2.setPixmap(qPixmapVar2)
            self.label_3.setPixmap(qPixmapVar3)

            self.show()

    def Houghtransform(self, num):
        dialog_1 = Dialog1Class()
        ret = dialog_1.exec_()
        
        if ret:
            self.image_left = dialog_1.image_left
            self.image_right = dialog_1.image_right
               
            self.label_1.setGeometry(30, 30, self.image_left.width(), self.image_left.height())
            self.label_2.setGeometry(572, 30, self.image_right.width(), self.image_right.height())
            self.label_3.setGeometry(1114, 30, self.image_left.width(), self.image_left.height())
            
            qPixmapVar1 = QPixmap.fromImage(self.image_left)
            qPixmapVar2 = QPixmap.fromImage(self.image_right)
            qPixmapVar3 = QPixmap.fromImage(self.image_left)
            
            #권나성
            if num == 1:
                qPixmapVar3=funcNasung.HoughTransform(self.image_left)
                pass
            #권나성


            #권동욱
            elif num == 2:
                pass
            #권동욱


            #금빛나
            elif num == 3:
                pass
            #금빛나


            #김나현
            elif num == 4:
                pass
            #김나현


            #서성원
            elif num == 5:
                pass
            #서성원


            #손정현
            elif num == 6:
                pass
            #손정현


            #이로사
            elif num == 7:
                pass
            #이로사


            #이성호
            elif num == 8:
                pass
            #이성호


            #한정수
            elif num == 9:
                pass
            #한정수


            #황승언
            else :
                pass
            #황승언


            
            self.label_1.setPixmap(qPixmapVar1)
            self.label_2.setPixmap(qPixmapVar2)
            self.label_3.setPixmap(qPixmapVar3)

            self.show()

    def Edgedetection(self, num):
        dialog_1 = Dialog1Class()
        ret = dialog_1.exec_()
        
        if ret:
            self.image_left = dialog_1.image_left
            self.image_right = dialog_1.image_right
               
            self.label_1.setGeometry(30, 30, self.image_left.width(), self.image_left.height())
            self.label_2.setGeometry(572, 30, self.image_right.width(), self.image_right.height())
            self.label_3.setGeometry(1114, 30, self.image_left.width(), self.image_left.height())
            
            qPixmapVar1 = QPixmap.fromImage(self.image_left)
            qPixmapVar2 = QPixmap.fromImage(self.image_right)
            qPixmapVar3 = QPixmap.fromImage(self.image_left)
            
            #권나성
            if num == 1:
                qPixmapVar3=funcNasung.EdgeDetection(self.image_left)
                pass
            #권나성


            #권동욱
            elif num == 2:
                pass
            #권동욱


            #금빛나
            elif num == 3:
                pass
            #금빛나


            #김나현
            elif num == 4:
                pass
            #김나현


            #서성원
            elif num == 5:
                pass
            #서성원


            #손정현
            elif num == 6:
                pass
            #손정현


            #이로사
            elif num == 7:
                pass
            #이로사


            #이성호
            elif num == 8:
                pass
            #이성호


            #한정수
            elif num == 9:
                pass
            #한정수


            #황승언
            else :
                pass
            #황승언

            
            self.label_1.setPixmap(qPixmapVar1)
            self.label_2.setPixmap(qPixmapVar2)
            self.label_3.setPixmap(qPixmapVar3)

            self.show()

    def Stereomatching(self, num):
        dialog_1 = Dialog1Class()
        ret = dialog_1.exec_()
        
        if ret:
            self.image_left = dialog_1.image_left
            self.image_right = dialog_1.image_right
               
            self.label_1.setGeometry(30, 30, self.image_left.width(), self.image_left.height())
            self.label_2.setGeometry(572, 30, self.image_right.width(), self.image_right.height())
            self.label_3.setGeometry(1114, 30, self.image_left.width(), self.image_left.height())
            
            qPixmapVar1 = QPixmap.fromImage(self.image_left)
            qPixmapVar2 = QPixmap.fromImage(self.image_right)
            qPixmapVar3 = QPixmap.fromImage(self.image_left)

            #권나성
            if num == 1:
                pass
            #권나성


            #권동욱
            elif num == 2:
                pass
            #권동욱


            #금빛나
            elif num == 3:
                pass
            #금빛나


            #김나현
            elif num == 4:
                pass
            #김나현


            #서성원
            elif num == 5:
                pass
            #서성원


            #손정현
            elif num == 6:
                pass
            #손정현


            #이로사
            elif num == 7:
                pass
            #이로사


            #이성호
            elif num == 8:
                pass
            #이성호


            #한정수
            elif num == 9:
                pass
            #한정수


            #황승언
            else :
                pass
            #황승언           

            
            self.label_1.setPixmap(qPixmapVar1)
            self.label_2.setPixmap(qPixmapVar2)
            self.label_3.setPixmap(qPixmapVar3)

            self.show()

    def Facedetection(self, num):
        dialog_1 = Dialog1Class()
        ret = dialog_1.exec_()
        
        if ret:
            self.image_left = dialog_1.image_left
            self.image_right = dialog_1.image_right
               
            self.label_1.setGeometry(30, 30, self.image_left.width(), self.image_left.height())
            self.label_2.setGeometry(572, 30, self.image_right.width(), self.image_right.height())
            self.label_3.setGeometry(1114, 30, self.image_left.width(), self.image_left.height())
            
            qPixmapVar1 = QPixmap.fromImage(self.image_left)
            qPixmapVar2 = QPixmap.fromImage(self.image_right)
            qPixmapVar3 = QPixmap.fromImage(self.image_left)

            #권나성
            if num == 1:
                pass
            #권나성


            #권동욱
            elif num == 2:
                pass
            #권동욱


            #금빛나
            elif num == 3:
                pass
            #금빛나


            #김나현
            elif num == 4:
                pass
            #김나현


            #서성원
            elif num == 5:
                pass
            #서성원


            #손정현
            elif num == 6:
                pass
            #손정현


            #이로사
            elif num == 7:
                pass
            #이로사


            #이성호
            elif num == 8:
                pass
            #이성호


            #한정수
            elif num == 9:
                pass
            #한정수


            #황승언
            else :
                pass
            #황승언

            
            self.label_1.setPixmap(qPixmapVar1)
            self.label_2.setPixmap(qPixmapVar2)
            self.label_3.setPixmap(qPixmapVar3)

            self.show()


        
if __name__ == "__main__" :
    app = QApplication([]) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()


