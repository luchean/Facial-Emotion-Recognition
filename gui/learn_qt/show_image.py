#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
图片的标定工具，将图片标定为基本的物种表情

Author: Gray_Gl
Last edited: February  2022
"""

# QPixmap用来处理和显示图片
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
    QLabel, QApplication)
from PyQt5.QtGui import QPixmap
import sys

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        hbox = QHBoxLayout(self)
        pixmap = QPixmap(r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\R.jfif")

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())