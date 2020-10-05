from PyQt5.QtCore import Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QIntValidator, QFont, QPalette, QColor # QIntValidator проверяет, что пользователем вводятся целые числа
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QPushButton, QLabel, QLineEdit,
        QComboBox, QTableWidget, QTableWidgetItem)
import mysql.connector
from mysql.connector import Error
import datetime        
desc_txt=''' тут текст о том что делает приложение '''
requests = ["Информация о концертах на выбранной площадке",
"Информация о концертах, в которых участвует выбранный исполнитель"]
procedures = ['ConcertsInHall', 'ConcertsWithBand18']

#                    _oo0oo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                   0\  =  /0
#                 ___/`---'\___
#                .' \\|     |// '.
#               / \\|||  :  |||// \
#              / _||||| -:- |||||- \
#             |   | \\\  -  /// |   |
#             | \_|  ''\---/''  |_/ |
#            \  .-\__  '-'  ___/-. /
#          ___'. .'  /--.--\  `. .'___
#        ."" '<  `.___\_<|>_/___.' >' "".
#       | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#       \  \ `_.   \_ __\ /__ _/   .-` /  /
#   =====`-.____`.___ \_____/___.-`___.-'=====
#                        `=---='


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Work with MySQL
# Connection to necessary DB 
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Find result of request by query
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Find result of request by procedure
def execute_procedure(connection, nameOfProcedure, args):
    cursor = connection.cursor()
    result = []
    try:
        cursor.callproc(nameOfProcedure, args)
        for _str in cursor.stored_results():
            result=_str.fetchall()
        return result    
    except Error as e:
        print(f"The error '{e}' occurred")


connection=create_connection('localhost', 'root', 'Vagner99', 'ConcertHalls')

##############################################################

# def data_check(lst_in):
#     for i in range(len(lst_in)):
#         for j in range(len(lst_in[0])):
#             if isinstance(lst_in[i][j], datetime.date) or isinstance(lst_in[i][j], datetime.date):
                

                

##############################################################

# Сreation of UI of Application
# Window with input parameters for the request
class InputWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI()
        self.connects()
        self.set_appear()
        self.show()

    def initUI(self):

        self.txt_on_IW = QLabel('Введите данные')
        self.next_button = QPushButton('Далее', self)
        layout_col = QVBoxLayout()
        layout_col.addWidget(self.txt_on_IW, alignment=Qt.AlignCenter)
        if txt_choose==2:
            layout_row = QHBoxLayout()
            self.line1=QLineEdit()
            self.line2=QLineEdit()
            layout_row.addWidget(self.line1)
            layout_row.addWidget(self.line2)
            layout_col.addLayout(layout_row)
        elif txt_choose==1 or txt_choose==0:
            self.line1=QLineEdit()
            layout_col.addWidget(self.line1)
        layout_col.addWidget(self.next_button, alignment=Qt.AlignCenter)
        self.setLayout(layout_col)


    def set_appear(self):
        self.setWindowTitle('Input Window')
        self.resize(650, 400)
        self.move(500, 400)

    def connects(self):
        self.next_button.clicked.connect(self.open_result_window)

    def open_result_window(self):
        global RW, txt_in
        txt_in=self.line1.text()
        RW = ResultWindow()
        self.hide()



# Window return result of request
class ResultWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI()
        #self.connects()
        self.set_appear()
        self.show()

    def initUI(self):
        result = execute_procedure(connection, procedures[txt_choose], [txt_in])
        print(result)
        self.table = QTableWidget()  
        self.table.setColumnCount(len(result[0]))    
        self.table.setRowCount(len(result)) 
        for i in range(len(result)):
            for j in range(len(result[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(result[i][j])))
        layout_col = QVBoxLayout()
        self.table.resizeColumnsToContents()
        layout_col.addWidget(self.table)
        self.setLayout(layout_col)


    def set_appear(self):
        self.setWindowTitle('Result Window')
        self.resize(650, 400)
        self.move(500, 400)

    

# Main window with choosing of the request
class MainWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI()
        self.connects()
        self.set_appear()
        self.show()

    def initUI(self):
        self.choose_button = QPushButton('Выбрать', self)
        self.close_button = QPushButton('Закрыть', self)
        self.describe_txt = QLabel(desc_txt)
        self.choose = QComboBox()
        self.choose.addItems(requests)
        layout_col = QVBoxLayout()
        layout_col.addWidget(self.describe_txt, alignment=Qt.AlignCenter)
        layout_col.addWidget(self.choose, alignment=Qt.AlignCenter)
        layout_row = QHBoxLayout()
        layout_row.addWidget(self.choose_button)
        layout_row.addWidget(self.close_button)
        layout_col.addLayout(layout_row)
        self.setLayout(layout_col)


    def set_appear(self):
        self.setWindowTitle('Start Window')
        self.resize(650, 400)
        self.move(500, 400)

    def connects(self):
        self.choose_button.clicked.connect(self.open_input_window)
        self.close_button.clicked.connect(QCoreApplication.instance().quit)

    def open_input_window(self):
        global IW, txt_choose
        txt_choose=self.choose.currentIndex()
        IW=InputWindow()
        self.hide()

if __name__ == '__main__':
    app = QApplication([])
    mW = MainWindow()
    app.exec()