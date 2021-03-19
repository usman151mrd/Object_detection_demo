import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
import torch
import matplotlib.image as mpimg


def response(result):
    out = {}
    for i, (img, pred) in enumerate(zip(result.imgs, result.pred)):
        if pred is not None:
            for c in pred[:, -1].unique():
                n = (pred[:, -1] == c).sum()  # detections per class
                out[result.names[int(c)]] = int(n)
    return out


class Detection:
    def __init__(self, path):
        self.image_path = path

    def detection(self):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        image = mpimg.imread(self.image_path)
        results = model(image)
        dic = response(results)
        return dic


class Ui_MainWindow(object):
    def __init__(self):
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.frame = QtWidgets.QFrame(self.central_widget)
        self.image_view = QtWidgets.QLabel(self.central_widget)
        self.convert = QtWidgets.QPushButton(self.central_widget)
        self.browse = QtWidgets.QPushButton(self.frame)
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.label = QtWidgets.QLabel(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)

        self.textEdit = QtWidgets.QTextEdit(self.central_widget)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1118, 485)
        self.central_widget.setObjectName("centralwidget")
        self.textEdit.setGeometry(QtCore.QRect(10, 110, 701, 351))
        self.textEdit.setObjectName("textEdit")
        self.frame.setGeometry(QtCore.QRect(19, 20, 581, 45))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.browse.setObjectName("browse")
        self.horizontalLayout.addWidget(self.browse)
        self.browse.clicked.connect(self.open_file)
        self.convert.setGeometry(QtCore.QRect(620, 30, 89, 25))
        self.convert.setObjectName("convert")
        self.convert.clicked.connect(self.convert_to_text)
        self.image_view.setGeometry(QtCore.QRect(740, 110, 331, 341))
        self.image_view.setObjectName("image_view")
        pixmap = QPixmap('logo.png')
        pixmap = pixmap.scaled(self.image_view.width(), self.image_view.height())
        self.image_view.setPixmap(pixmap)
        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def onQApplicationStarted(self):
        # QMessageBox.about(None,"Message","Application started ")
        pixmap = QPixmap('logo.png')
        pixmap = pixmap.scaled(self.image_view.width(), self.image_view.height())
        self.image_view.setPixmap(pixmap)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "File Name"))
        self.browse.setText(_translate("MainWindow", "Browse"))
        self.convert.setText(_translate("MainWindow", "Convert"))
        self.image_view.setText(_translate("MainWindow", "show image here"))
        self.onQApplicationStarted()

    def open_file(self):
        # self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", "Images Files (*.jpg)")
        # if self.file_name[0] != '':
        #     self.lineEdit.setText(self.file_name[0])
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select your image",
            "",
            "All Files (*);;Image Files (*.jpeg)",
            options=options)
        if fileName:
            self.lineEdit.setText(fileName)
            pixmap = QPixmap(fileName)
            pixmap = pixmap.scaled(self.image_view.width(), self.image_view.height())
            self.image_view.setPixmap(pixmap)

    def convert_to_text(self):

        if sys.version_info[0] < 3:
            QMessageBox.about(None, "python version Error", "Please install python 3.x ")
        path = self.lineEdit.text()
        detect = Detection(path)
        text = str(detect.detection())
        self.textEdit.setText(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
