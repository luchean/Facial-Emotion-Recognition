from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys


class WorkerSignals(QObject):
    '''
     Defines the signals available from a running worker thread.

     Supported signals are:

     finished
         No data

     error
         tuple (exctype, value, traceback.format_exc() )

     result
         object data returned from processing, anything

     '''
    finished = pyqtSignal()
    # 定义需要传递的信号类型
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    work thread

    继承QRunnable去处理工作进程的设置、信号处理和包装，函数本身对象，并不是子类，是可以进行传递的

    :param callback:函数回调是运行在工作进程中，提供的参数args和kwargs是传递进需要执行的进程的
    :param args and kwargs：传递给函数回调进行执行的
    '''

    def __init__(self,fn,*args,**kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        # 增加对参数的回调
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        初始化执行函数，并传入参数
        :return:
        '''
        try:
            result = self.fn(
                *self.args,**self.kwargs
            )
        except:
            # 异常打印出异常信息
            traceback.print_exc()
            exctype,value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.l)
        layout.addWidget(b)
        w = QWidget()
        w.setLayout(layout)

        # 将整个布局放于网络中间
        self.setCentralWidget(w)

        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads "% self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()


    def progress_fn(self,n):
        print("%d%% done"%n)


    def execute_this_fn(self,progress_callback):
        for n in range(0,5):
            time.sleep(1)
            progress_callback.emit(n*100/4)

        return "Done"

    def print_output(self,s):
        print(s)

    def thread_complete(self):
        print("THread COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)


    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)


app = QApplication([])
window = MainWindow()
app.exec_()