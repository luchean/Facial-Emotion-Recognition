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
                             QTextEdit)
# 增加窗口的图标的显示
from PyQt5.QtGui import QIcon,QFont
# 导入相关事件和信息槽宝
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()


    def initUI(self):
        '''
        设置页面的布局，并显示
        :return:
        '''

        # 声明五种基本的情绪
        emotion = ['listening','understanding','tired','discreted','unknown']
        emotion_button = []
        for i in emotion:
            temp = QPushButton(i)
            temp.clicked.connect(self.buttonClicked)
            emotion_button.append(temp)

        # 设置退出和导入按钮
        # 退出按钮设置，了解singles和slot的机制
        quit_button = QPushButton('Quit')
        import_button = QPushButton('import')

        # 设置显示图片的工具
        image_show = QTextEdit()

        # 设置布局grid
        grid = QGridLayout()
        grid.setSpacing(10)

        # 添加对应控件
        grid.addWidget(image_show,1,0,6,6)
        for i in range(len(emotion_button)):
            grid.addWidget(emotion_button[i],2,i)
        grid.addWidget(import_button,3,0)
        grid.addWidget(import_button,3,1)
        # 样例  设置空间的提示信息
        self.setLayout(grid)

        # 设置窗口的位置并设置大小，先是坐标，再是大小
        self.setGeometry(300,300,600,660)
        self.center()
        self.setWindowTitle('Learning Emotion Recognition')
        self.setWindowIcon(QIcon(r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\icon.png'))

        self.show()

    def buttonClicked(self):
        '''
        按钮点击事件，获取按钮的信息，获取下一个图片，并将当前的按钮信息写入到字典中
        :return:
        '''
        sender = self.sender()
        print(sender.text())

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

    def closeEvent(self, event):
        '''
        消息盒子机制，如果关闭QWdget，会产生一个QCloseEvent，将之传入到
        closeEvent函数中的event参数钟，改变空间的默认行为，替换掉默认的
        事件处理
        :param event:
        :return:
        注意：这里有一个bug，如果是你自己设置关闭按钮，就不会有提示
        '''

        # 第二个字符显示在对话框
        # 第三个字符是消息框的两个按钮
        # 最后一个参数默认选中的值
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit ?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    # 创建的应用对象，sys.argv是一组命令行参数
    app = QApplication(sys.argv)

    ex = Example()

    # 确保主循环安全退出，确保外界环境能够收到著空间结束的消息
    sys.exit(app.exec_())