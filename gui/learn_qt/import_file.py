#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
图片的标定工具，将图片标定为基本的物种表情

Author: Gray_Gl
Last edited: February  2022
"""

# QFileDialog实现选择文件夹，并对其进行打开和保存
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        # 定义一个文本编辑器
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()


    def showDialog(self):

        # 弹出一个QFileDialog窗口
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            # 选中读取的文件，并显示在文本编辑器中
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                # 将文件显示在文本编辑器中
                self.textEdit.setText(data)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())