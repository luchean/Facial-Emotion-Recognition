from random import randint

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window %d"% randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 临时解决窗口的出现
        self.w1 = AnotherWindow()
        self.w2 = AnotherWindow()

        # 设置对应按钮
        self.button1 = QPushButton("Push for Window1")
        self.button2 = QPushButton("Push for Window2")

        # self.button.clicked.connect(self.show_new_window)

        self.button1.clicked.connect(self.toggle_window1)
        self.button2.clicked.connect(self.toggle_window2)

        v = QVBoxLayout()
        v.addWidget(self.button1)
        v.addWidget(self.button2)

        w = QWidget(self)
        w.setLayout(v)

        self.setCentralWidget(w)
        self.setGeometry(300,300,600,660)

    def toggle_window1(self):
        if self.w1.isVisible():
            self.w1.hide()
        else:
            self.w1.show()

    def toggle_window2(self):
        if self.w2.isVisible():
            self.w2.hide()
        else:
            self.w2.show()


    def show_new_window1(self, checked):
        # 检查窗口是否被重复创建
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()
        else:
            self.w.close()
            self.w = None

    def show_new_window2(self,checked):
        self.w.show()

    def toggle_window(self,check):
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
