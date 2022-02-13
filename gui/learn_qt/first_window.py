import sys
from PyQt5.QtWidgets import QApplication, QWidget
# 增加窗口的图标的显示
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,300,220)
        self.setWindowTitle('Learning Emotion Recognition')
        self.setWindowIcon(QIcon(r'C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\icon.png'))

        self.show()

if __name__ == '__main__':
    # 创建的应用对象，sys.argv是一组命令行参数
    app = QApplication(sys.argv)

    ex = Example()

    # 确保主循环安全退出，确保外界环境能够收到著空间结束的消息
    sys.exit(app.exec_())