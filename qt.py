# import sys
# from PyQt5.QtWidgets import (QWidget, QToolTip,
#     QPushButton, QApplication, QDesktopWidget)
# from PyQt5.QtGui import QFont
# from PyQt5.QtCore import QCoreApplication

# class main_window(QWidget):

#     def __init__(self):
#         super().__init__()

#         self.initUI()


#     def initUI(self):

#         self.resize(500, 300)
#         self.center()
#         self.button_open('Выбрать', [100,250])
#         self.button_close([300,250])
#         self.setWindowTitle('Center')
#         self.show()


#     def center(self):

#         qr = self.frameGeometry()
#         cp = QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())

#     def button_open(self, name, pos):

#         btn = QPushButton(name, self)
#         btn.resize(100,35)
#         btn.clicked.connect()
#         btn.move(pos[0], pos[1])

#     def button_close(self, pos):

#         btn = QPushButton('Закрыть', self)
#         btn.resize(100,35)
#         btn.clicked.connect(QCoreApplication.instance().quit)
#         btn.move(pos[0], pos[1])

# if __name__ == '__main__':

#     app = QApplication(sys.argv)
#     ex = main_window()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton


class Window1(QWidget):
    def __init__(self):
        super(Window1, self).__init__()
        self.setWindowTitle('Window1')
        self.resize(500, 300)
        self.button1 = QPushButton(self)
        self.button1.setText('Выбор')
        self.button1.resize(100,35)
        self.button1.move(100,250)
        self.button1.show()
        self.button_close = QPushButton(self)
        self.button_close.setText('Закрыть')
        self.button_close.resize(100,35)
        self.button_close.move(300,250)
        self.button_close.show()


class Window2(QWidget):
    def __init__(self):
        super(Window2, self).__init__()
        self.setWindowTitle('Window2')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('MainWindow')

    def show_window_1(self):
        self.w1 = Window1()
        self.w1.button1.clicked.connect(self.show_window_2)
        self.w1.button_close.clicked.connect(self.w1.close)
        self.w1.show()

    def show_window_2(self):
        self.w2 = Window2()
        self.w2.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show_window_1()
    sys.exit(app.exec_())