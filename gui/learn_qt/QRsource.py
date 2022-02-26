import sys
from PyQt5 import QtGui,QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.value = 1
        self.setWindowTitle("Hello World")
        self.button = QtWidgets.QPushButton("My button")

        icon = QtGui.QIcon(r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\monkey.png")
        self.button.setIcon(icon)
        self.button.clicked.connect(self.change_icon)

        self.setCentralWidget(self.button)

        self.show()

    def change_icon(self):
        if self.value == 1:
            icon = QtGui.QIcon(r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\penguin.png")
            self.button.setIcon(icon)
            self.value = 0
        else:
            self.value = 1
            icon = QtGui.QIcon(r"C:\Users\gray\Desktop\FacialEmotion\Facial-Emotion-Recognition\gui\image\monkey.png")
            self.button.setIcon(icon)

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()