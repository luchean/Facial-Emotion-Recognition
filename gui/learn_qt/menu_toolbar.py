###########################################################
# 菜单和工具栏
###########################################################
import sys
# QAction是菜单栏、工具栏和快捷键的动作组合
from PyQt5.QtWidgets import QMainWindow,QApplication, QAction,qApp
from PyQt5.QtGui import QIcon

# 当前窗口的属性是
class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        ###############################################################
        # 创建菜单栏，并指定退出
        # 创建一个退出的标签,设置为退出
        # 创建一个行为对象，这个对象绑定了一个标签、图标快捷键
        exitAct = QAction(QIcon(r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\HTSCIT_退出1.png'),'&Exit',self)
        # 创建一个退出的快捷键
        exitAct.setShortcut('Ctrl+Q')
        # 创建同时设置按钮的状态信息
        exitAct.setStatusTip('Exit Application')
        # 执行指定的动作时，触发一个QApplication的退出事件
        exitAct.triggered.connect(qApp.quit)

        ###############################################################
        # 设置工具栏
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        ###############################################################
        # 设置菜单栏
        menubar = self.menuBar()
        # 菜单栏增加对应的file菜单
        fileMenu = menubar.addMenu('&File')
        # 关联了点击退出应用的事件
        fileMenu.addAction(exitAct)

        ###############################################################
        # 创建状态栏，并设置信息为ready模式
        self.statusBar().showMessage('Ready')

        # 设置窗口大小
        self.setGeometry(300,300,400,350)
        self.setWindowTitle('StatusBar')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
