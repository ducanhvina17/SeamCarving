# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from funtion import *
import cv2
import time
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.inputDir=''
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.choose_Image = QtWidgets.QPushButton(self.centralwidget)
        self.choose_Image.setGeometry(QtCore.QRect(30, 10, 121, 31))
        self.choose_Image.setObjectName("choose_Image")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 10, 91, 31))
        self.label.setObjectName("label")
        self.size_image = QtWidgets.QLabel(self.centralwidget)
        self.size_image.setGeometry(QtCore.QRect(330, 10, 121, 31))
        self.size_image.setObjectName("size_image")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(30, 60, 441, 101))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 11, 47, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 40, 47, 20))
        self.label_3.setObjectName("label_3")
        self.width_new = QtWidgets.QLineEdit(self.tab)
        self.width_new.setGeometry(QtCore.QRect(60, 10, 101, 21))
        self.width_new.setObjectName("width_new")
        self.height_new = QtWidgets.QLineEdit(self.tab)
        self.height_new.setGeometry(QtCore.QRect(60, 40, 101, 21))
        self.height_new.setObjectName("height_new")
        self.do_Resize = QtWidgets.QPushButton(self.tab)
        self.do_Resize.setGeometry(QtCore.QRect(270, 20, 121, 31))
        self.do_Resize.setObjectName("do_Resize")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.do_Remove = QtWidgets.QPushButton(self.tab_2)
        self.do_Remove.setGeometry(QtCore.QRect(150, 20, 121, 31))
        self.do_Remove.setObjectName("do_Remove")
        self.tabWidget.addTab(self.tab_2, "")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(60, 170, 411, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.text_process = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_process.setGeometry(QtCore.QRect(25, 311, 441, 131))
        self.text_process.setObjectName("text_process")
        self.openImageOrg = QtWidgets.QPushButton(self.centralwidget)
        self.openImageOrg.setGeometry(QtCore.QRect(30, 230, 111, 31))
        self.openImageOrg.setObjectName("openImageOrg")
        self.openImagePro = QtWidgets.QPushButton(self.centralwidget)
        self.openImagePro.setGeometry(QtCore.QRect(180, 230, 121, 31))
        self.openImagePro.setObjectName("openImagePro")
        self.openImageEng = QtWidgets.QPushButton(self.centralwidget)
        self.openImageEng.setGeometry(QtCore.QRect(340, 230, 101, 31))
        self.openImageEng.setObjectName("openImageEng")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.btn_toggle(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Seam Carving"))
        self.choose_Image.setText(_translate("MainWindow", "Chọn File Ảnh"))
        self.label.setText(_translate("MainWindow", "Kích thước ảnh:"))
        self.size_image.setText(_translate("MainWindow", "Vui lòng chọn file"))
        self.label_2.setText(_translate("MainWindow", "Width:"))
        self.label_3.setText(_translate("MainWindow", "Height:"))
        self.do_Resize.setText(_translate("MainWindow", "Resize ảnh"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Thay đổi kích thước ảnh"))
        self.do_Remove.setText(_translate("MainWindow", "Chọn vật thể"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Xóa vật thể"))
        self.openImageOrg.setText(_translate("MainWindow", "Mở ảnh gốc"))
        self.openImagePro.setText(_translate("MainWindow", "Mở ảnh hoàn thành"))
        self.openImageEng.setText(_translate("MainWindow", "Mở ảnh Energy"))
    def btn_toggle(self, MainWindow):
        self.choose_Image.clicked.connect(self.setExistingDirectory)
        self.do_Resize.clicked.connect(self.resizeImage)
        self.do_Remove.clicked.connect(self.removeObject)
        self.openImageOrg.clicked.connect(self.openOrg)
        self.openImagePro.clicked.connect(self.openSuc)
        self.openImageEng.clicked.connect(self.openEng)
    def setExistingDirectory(self): 
        filename = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.inputDir=filename
        print(self.inputDir)
        choose_Image=cv2.imread(filename)
        h,w=choose_Image.shape[:2]
        self.size_image.setText('W: '+str(w)+" - "+"H: "+str(h))
    def resizeImage(self):
        start_time = time.time()
        self.resize=SeamCarving(self,self.inputDir,int(self.height_new.text()),int(self.width_new.text()),is_remove_object=False)
        print("--- %s seconds ---" % (time.time() - start_time))
        self.text_process.append("--- %s seconds ---" % (time.time() - start_time))
    def removeObject(self):
        start_time = time.time()
        self.resize=SeamCarving(self,self.inputDir,is_remove_object=True)
        print("--- %s seconds ---" % (time.time() - start_time))
        self.text_process.append("--- %s seconds ---" % (time.time() - start_time))
    def openOrg(self):
        choose_Image=cv2.imread(self.inputDir)
        cv2.imshow('Image Orginal',choose_Image)
    def openSuc(self):
        self.resize.show_image_process()
    def openEng(self):
        self.resize.show_enery()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

