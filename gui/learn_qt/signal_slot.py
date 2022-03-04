#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
图片的标定工具，将图片标定为基本的物种表情

Author: Gray_Gl
Last edited: February  2022
"""

import sys
# 同时引入多个包，一定要带逗号
# QDesktopWidget提供了用户桌面信息，包括屏幕的大小
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QGridLayout,
                             QTextEdit, QLCDNumber, QSlider, QVBoxLayout, QLabel, QMainWindow, QHBoxLayout)
# 增加窗口的图标的显示
from PyQt5.QtGui import QIcon,QFont
# 导入相关事件和信息槽宝
from PyQt5.QtCore import QCoreApplication, Qt, QObject, pyqtSignal


class Example_LED(QWidget):
    '''
    介绍：
    应用都是由事件进行驱动，调用exec_()应用会进入主循环，主循环会监听和分发事件
    事件的三个角色：事件源，事件，事件目标。事件源绑定事件处理函数，作用在事件目标上
    signal和slot适用于对象间的通讯，事件触发产生一个signal，python会据此调用一个slot
    '''
    def __init__(self):
        super(Example_LED, self).__init__()
        self.initUI()


    def initUI(self):
        '''
        设置页面的布局，并显示
        :return:
        '''

        # 声明新的配件
        lcd = QLCDNumber()
        sld = QSlider(Qt.Horizontal, self)

        # 垂直盒子进行合并
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        # 设定排列
        self.setLayout(vbox)

        # 设定signal和slot的配合
        # sld滑轨是事件源，display是数据的展示
        sld.valueChanged.connect(lcd.display)

        # 设置窗口的位置并设置大小，先是坐标，再是大小
        self.setGeometry(300,300,600,660)
        self.center()
        self.setWindowTitle('Learning Emotion Recognition')
        self.setWindowIcon(QIcon(r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\icon.png'))

        self.show()

    def center(self):
        '''
        在主窗口之上又设置了一个主框架，通过主窗口和主框架位置的相对关系实现对齐
        :return:
        '''
        # 获取主窗口所在的框架
        qr = self.frameGeometry()
        # 获取屏幕的分辨率，并得到屏幕中间点的位置
        cp = QDesktopWidget().availableGeometry().center()
        # 将主窗口的框架的中心点放置到屏幕的中心位置
        qr.moveCenter(cp)
        # 通过move函数将主窗口的左上角移动到框架的左上角，实现对其居中
        self.move(qr.topLeft())


# 重构事件处理器
class Example_reshape(QWidget):

    def __init__(self):
        super(Example_reshape, self).__init__()
        self.initUI()

    def initUI(self):
        '''
        初始化运行的界面
        :return:
        '''
        self.setGeometry(300,300,250,150)
        self.setWindowTitle("Event Handler")
        self.show()

    def keyPressEvent(self,e):
        '''
        注意，这里是重构了事件处理函数KeyPressEvent，替换了原先的函数
        :param e:
        :return:
        '''
        if e.key() == Qt.Key_Escape:
            self.close()


# 事件对象：python用来描述一系列事件自身属性的对象
class Example_object(QWidget):

    def __init__(self):
        super(Example_object, self).__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        x = 0
        y = 0

        self.text = "x:{0},y:{1}".format(x,y)

        self.label = QLabel(self.text,self)
        grid.addWidget(self.label,0,0,Qt.AlignTop)

        # 开启鼠标追踪事件
        self.setMouseTracking(True)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 200)
        self.setWindowTitle('Event object')
        self.show()


    # 事件对象是鼠标移动，打开是鼠标移动事件的监督
    def mouseMoveEvent(self, e):

        x = e.x()
        y = e.y()

        text = "x:{0},y:{1}".format(x,y)
        self.label.setText(text)


# 事件发送：确定发送信号的组件,同时有多个按钮，可以判定的到底是哪个按钮返回的信息
class Example_sendMessage(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        btn1 = QPushButton("Button1")
        btn2 = QPushButton("Button2")

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        # self.statusBar()

        grid = QGridLayout()
        self.setLayout(grid)

        grid.setSpacing(10)
        grid.addWidget(btn1,1,0)
        grid.addWidget(btn2,2,0)

        self.setGeometry(300,300,290,150)
        self.setWindowTitle('test')
        self.show()

    def buttonClicked(self):

        sender = self.sender()
        print(sender.text())
        # self.statusBar().showMessage(sender.text() + 'was pressed')


# 信号发送：QObject能够发送事件信号
# 创建一个closeApp的信号，信号会在鼠标按下的时候触发
class Communicate(QObject):
    closeApp = pyqtSignal()


class Example_QObject(QMainWindow):

    def __init__(self):
        super(Example_QObject, self).__init__()
        self.initUI()

    def initUI(self):
        self.c = Communicate()
        # 将信号和closeApp的信号进行的绑定
        self.c.closeApp.connect(self.close)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mousePressEvent(self, event):
        # 点击鼠标，信号发送
        self.c.closeApp.emit()

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # 一旦mainwindow的名称改变了，新的名称就会传递给on_window_title_changed
        self.windowTitleChanged.connect(self.on_window_title_changed)

        # 这里仅仅并没有传入任何的参数，截取并未传入任何新的信号
        self.windowTitleChanged.connect(lambda x:self.on_window_title_changed_no_params())

        # 这里截取了对应的信号，并将signal作为x传给了真实的信号变量，同时附加了25这个值
        self.windowTitleChanged.connect(lambda x: self.my_custom_fn(x,25))

        self.setWindowTitle('new window title!')

        # SLOT: This accepts a string, e.g. the window title, and prints it

    def on_window_title_changed(self, s):
        print(s)

        # SLOT: This is called when the window title changes.

    def on_window_title_changed_no_params(self):
        print("Window title changed.")

        # SLOT: This has default parameters and can be called without a value

    def my_custom_fn(self, a="HELLLO!", b=5):
        print(a, b)

class Trouble_loop(QWidget):

    def __init__(self):
        super(Trouble_loop, self).__init__()
        self.initUI()

    def initUI(self):

        v = QVBoxLayout()
        h = QHBoxLayout()

        for i in range(7):
            bt1 = QPushButton(str(i))
            bt1.pressed.connect(
                # lambda i: self.button_pressed(i)
                lambda a = i: self.button_pressed(a)
            )
            h.addWidget(bt1)
        v.addLayout(h)

        self.label1 = QLabel(" ")
        v.addWidget(self.label1)

        self.setLayout(v)
        self.setGeometry(300,300,250,250)
        self.show()

    def button_pressed(self,num):
        print(num)
        self.label1.setText(str(num))


if __name__ == '__main__':
    # 创建的应用对象，sys.argv是一组命令行参数
    app = QApplication(sys.argv)

    # ex = Example_LED()
    # ex = Example_reshape()
    # ex = Example_object()
    # ex = Example_sendMessage()
    # ex = Example_QObject()
    # ex = MainWindow()
    ex = Trouble_loop()
    ex.show()
    # 确保主循环安全退出，确保外界环境能够收到著空间结束的消息
    sys.exit(app.exec_())