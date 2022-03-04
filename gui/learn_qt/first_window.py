import sys
# 同时引入多个包，一定要带逗号
# QDesktopWidget提供了用户桌面信息，包括屏幕的大小
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton,QMessageBox, QDesktopWidget)
# 增加窗口的图标的显示
from PyQt5.QtGui import QIcon,QFont
# 导入相关事件和信息槽宝
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()


    def initUI(self):

        # 样例六，窗口剧中

        # 样例，设置退出按钮
        # 退出按钮设置，了解singles和slot的机制
        qbtn = QPushButton('Quit', self)
        # connect指定按下按钮的事件
        # QCoreApplication包含了事件的主循环，能够添加和删除所有事件
        # instance创建QCoreApplication的一个实例
        # 将点击事件和能终止进程并退出应用的quit函数绑定在一起
        # 在发送者和接收者之间建立通讯
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 80)

        # 样例  设置空间的提示信息
        # 这是提示框的字体和大小
        QToolTip.setFont(QFont('SansSerif',10))

        # 创建提示框，是widget的提示内容，同时可以使用富文本编辑器
        self.setToolTip('This is a <b>QWidget</b> widget')

        # 创建按键并设置按键提示信息,同时指定按钮所属的父类控件
        # 注意，没有父级的组建都是顶级窗口
        btn = QPushButton('确认',self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        # 调整按钮的大小，并移动位置，sizeHint是默认按钮大小
        btn.resize(btn.sizeHint())
        btn.move(50,50)

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