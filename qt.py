from PyQt5.QtCore import Qt, QTimer, QCoreApplication, QRegExp, QRect
from PyQt5.QtGui import QFont, QPalette, QColor, QRegExpValidator
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QPushButton, QLabel, QLineEdit,
        QComboBox, QTableWidget, QTableWidgetItem,QMessageBox)
import mysql.connector
from mysql.connector import Error
import datetime       
desc_txt='''                        Приветствуем Вас в программе для подбора концерта!
Тут Вы можете посмотреть все концерты на представленных концертных площадках,
     а также ознакомиться со списками песен и исполнителей на каждом концерте.
                                              Выберите категорию ниже.'''
desc_txt2='''Выберите одну из следующих опций: '''
menu=['Информация о концертах', 'Выбрать концерт по',\
 'Информация об артисте', 'Администрирование']
requests = [['Информация о концертах (все концерты)', 'Список песен для данного концерта',
'Список исполнителей для данного концерта', 'Длительность данного концерта', 'Вывести все занятные места для конкретного концерта'],
['Информация о концертах на выбранной площадке','Информация о концертах, в которых участвует выбранный исполнитель',
'Информация о концертах, на которых будет исполняться выбранная композиция', 'Информация о концертах в ближайшие M месяцев',
'Информация о концертах, отсортированных по возрастанию цены', 
'Информация о концертах, отсортированных по убыванию цены', 'Информация о концертах не дороже заданного значения',
'Концерты исполнителя с ценой ниже заданной'],
['Информация о концертах, в которых участвует выбранный исполнитель', 'Все песни данного исполнителя', 'Все исполнители',
'Популярность исполнителя по участию в концертах'],
['Печать билета','Сколько билетов осталось на конкретный концерт', 'Удалить концерт', 'Изменить дату и время концерта',
'Обновить группу по id', 'Создать билет', 'Добавить группу', 'Вывести все занятные места для конкретного концерта']]


procedures = [[('allConcertsSorted',),('SongsOnConcert', 'Введите название концерта'), 
('BandOnConcert', 'Введите название концерта'), ('DurationOfConcert', 'Введите название концерта'),
('existingTicketForConcert', 'Введите название концерта')],
[('ConcertsInHall', 'Введите название концертного зала'), ('ConcertsWithBand', 'Введите исполнителя'),
('ConcertsWithSong', 'Введите название песни'), ('ConcertsMonths', 'Введите количество месяцев'),
('fromCheapToExpensive', ), ('fromExpensiveToCheap', ), ('CheapTicket', 'Введите сумму'),
('cheaperThanWithBand', 'Введите исполнителя', 'Введите сумму')],
[('ConcertsWithBand', 'Введите исполнителя'), ('songsOfBand', 'Введите исполнителя'),('AllBands',), 
('popularBand', 'Введите количество концертов')],
[('PrintTickets', 'Введите id билета'), ('FreeTickets', 'Введите название концерта'),
('deleteConcert2', 'Введите название концерта для удаления'), 
('changeConcertDateAndTime', 'Введите название концерта', 'Введите новую дату', 'Введите новое время'),
('updateBand1', 'Введите id исполнителя', 'Введите новое название исполнителя', 'Введите новое количество человек'),
('CreateTicket4', 'Введите название концерта', 'Введите номер места', 'Введите тип билета (0 или 1)'),
('addBand', 'Введите id исполнителя', 'Введите название исполнителя', 'Введите количество человек'),
('existingTicketForConcert', 'Введите название концерта')]]
flags = [[0, 1, 1, 1, 1],
[2, 4, 3, 0, 0, 0, 0, 4, (4, 0)],
[4, 4, 0, 0],
[0, 1, 1, (1, 0, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0), 1]]

#                    _oo0oo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                   0\  =  /0
#                 ___/`---'\___
#               .' \\|     |// '.
#              / \\|||  :  |||// \
#             / _||||| -:- |||||- \
#            |   | \\\  -  /// |   |
#            | \_|  ''\---/''  |_/ |
#            \  .-\__  '-'  ___/-. /
#          ___'. .'  /--.--\  `. .'___
#        ."" '<  `.___\_<|>_/___.' >' "".
#       | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#       \  \ `_.   \_ __\ /__ _/   .-` /  /
#   =====`-.____`.___ \_____/___.-`___.-'=====
#                     `=---='


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


# Find result of request by procedure
def execute_procedure(connection, nameOfProcedure, args):
    cursor = connection.cursor()
    result = []
    desc=[]
    tmp=None
    try:
        cursor.callproc(nameOfProcedure, args)
        for _str in cursor.stored_results():
            result=_str.fetchall()
            tmp=_str.description
        if tmp!=None:
            for i in tmp:
                desc.append(i[0])        
            return result, desc
        else:
            connection.commit()
            return result, tmp        
    except Error as e:
        print(f"The error '{e}' occurred")

def createList(lst):
    result=[] 
    for i in lst:
        result.append(i[0])
    return result    




connection=create_connection('localhost', 'root', 'Vagner99', 'ConcertHalls')
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
        self.next_button = QPushButton('Далее', self)
        self.back_button = QPushButton('Назад', self)
        layout_row_but = QHBoxLayout()
        
        layout_col = QVBoxLayout()
        amount=len(procedures[txt_choose][txt_choose2])-1
        if amount==1:
            self.txt_on_IW = QLabel(procedures[txt_choose][txt_choose2][1])
            layout_col.addWidget(self.txt_on_IW, alignment=Qt.AlignCenter)
            self.choose3 = QComboBox()
            self.line1 = QLineEdit()
            if flags[txt_choose][txt_choose2]==3:
                self.choose3.addItems(createList(execute_procedure(connection,'AllSongs',())[0]))
                layout_col.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2]==4:
                self.choose3.addItems(createList(execute_procedure(connection,'AllBands',())[0]))
                layout_col.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2]==2:
                self.choose3.addItems(createList(execute_procedure(connection,'AllConcertHalls',())[0]))
                layout_col.addWidget(self.choose3, alignment=Qt.AlignCenter)    
            elif flags[txt_choose][txt_choose2]==1:
                self.choose3.addItems(createList(execute_procedure(connection,'AllConcerts',())[0]))
                layout_col.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2]==0:
                self.line1.setValidator(QRegExpValidator(QRegExp('^[А-ЯA-Za-zа-я0-9-.,:!\s]{0,45}$')))    
                layout_col.addWidget(self.line1)
        elif amount==2:
            layout_row_txt = QHBoxLayout()
            layout_row_in = QHBoxLayout()
            self.line1=QLineEdit()
            self.line2=QLineEdit()
            self.choose3 = QComboBox()
            if flags[txt_choose][txt_choose2]==3:
                self.choose3.addItems(createList(execute_procedure(connection,'AllSongs',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2]==4:
                self.choose3.addItems(createList(execute_procedure(connection,'AllBands',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2]==2:
                self.choose3.addItems(createList(execute_procedure(connection,'AllConcertHalls',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)    
            elif flags[txt_choose][txt_choose2]==1:
                self.choose3.addItems(createList(execute_procedure(connection,'AllConcerts',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2]==0:
                self.line1.setValidator(QRegExpValidator(QRegExp('^[А-ЯA-Za-zа-я0-9-.,:!\s]{0,45}$')))    
                layout_row_in.addWidget(self.line1, alignment=Qt.AlignCenter)
            self.line2.setValidator(QRegExpValidator(QRegExp('^[А-ЯA-Za-zа-я0-9-.,:!\s]{0,45}$')))
            self.txt_on_IW1 = QLabel(procedures[txt_choose][txt_choose2][1])
            self.txt_on_IW2 = QLabel(procedures[txt_choose][txt_choose2][2])
            layout_row_txt.addWidget(self.txt_on_IW1, alignment=Qt.AlignCenter)
            layout_row_txt.addWidget(self.txt_on_IW2, alignment=Qt.AlignCenter)
            layout_row_in.addWidget(self.line2, alignment=Qt.AlignCenter)
            layout_col.addLayout(layout_row_txt)
            layout_col.addLayout(layout_row_in)
            
        elif amount==3:
            layout_row_txt = QHBoxLayout()
            layout_row_in = QHBoxLayout()
            self.line1=QLineEdit()
            self.line2=QLineEdit()
            self.line3=QLineEdit()
            self.choose3 = QComboBox()
            if flags[txt_choose][txt_choose2][0]==3:
                self.choose3.addItems(createList(execute_procedure(connection,'AllSongs',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2][0]==4:
                self.choose3.addItems(createList(execute_procedure(connection,'AllBands',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2][0]==2:
                self.choose3.addItems(createList(execute_procedure(connection,'AllConcertHalls',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)    
            elif flags[txt_choose][txt_choose2][0]==1:
                self.choose3.addItems(createList(execute_procedure(connection,'AllConcerts',())[0]))
                layout_row_in.addWidget(self.choose3, alignment=Qt.AlignCenter)
            elif flags[txt_choose][txt_choose2][0]==0:
                self.line1.setValidator(QRegExpValidator(QRegExp('^[А-ЯA-Za-zа-я0-9-.,:!\s]{0,45}$')))    
                layout_row_in.addWidget(self.line1, alignment=Qt.AlignCenter)
            self.line2.setValidator(QRegExpValidator(QRegExp('^[А-ЯA-Za-zа-я0-9-.,:!\s]{0,45}$')))
            self.line3.setValidator(QRegExpValidator(QRegExp('^[А-ЯA-Za-zа-я0-9-.,:!\s]{0,45}$')))
            self.txt_on_IW1 = QLabel(procedures[txt_choose][txt_choose2][1])
            self.txt_on_IW2 = QLabel(procedures[txt_choose][txt_choose2][2])
            self.txt_on_IW3 = QLabel(procedures[txt_choose][txt_choose2][3])
            layout_row_txt.addWidget(self.txt_on_IW1, alignment=Qt.AlignCenter)
            layout_row_txt.addWidget(self.txt_on_IW2, alignment=Qt.AlignCenter)
            layout_row_txt.addWidget(self.txt_on_IW3, alignment=Qt.AlignCenter)

            layout_row_in.addWidget(self.line2, alignment=Qt.AlignCenter)
            layout_row_in.addWidget(self.line3, alignment=Qt.AlignCenter)
            layout_col.addLayout(layout_row_txt)
            layout_col.addLayout(layout_row_in) 

        layout_row_but.addWidget(self.next_button)
        layout_row_but.addWidget(self.back_button)
        layout_col.addLayout(layout_row_but)
        self.setLayout(layout_col)

    def set_appear(self):
        self.setWindowTitle('Input Window')
        self.resize(1000, 300)
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()-100) // 2
        self.move(x,y)

    def connects(self):
        self.next_button.clicked.connect(self.open_result_window)
        self.back_button.clicked.connect(self.open_SecondMenuWindow_window)

    def open_result_window(self):
        global result, desc, RW, MW
        if len(procedures[txt_choose][txt_choose2])-1==1:
            if self.line1.text()!='':
                txt_in=[self.line1.text()]
            else:    
                txt_in=[self.choose3.currentText()]
        elif len(procedures[txt_choose][txt_choose2])-1==2:
            if self.line1.text()!='':
                txt_in=[self.line1.text(), self.line2.text()]
            else:    
                txt_in=[self.choose3.currentText(), self.line2.text()]   
        elif len(procedures[txt_choose][txt_choose2])-1==3:
            if self.line1.text()!='':
                txt_in=[self.line1.text(), self.line2.text(), self.line3.text()]
            else:    
                txt_in=[self.choose3.currentText(), self.line2.text(), self.line3.text()]

        result, desc = execute_procedure(connection, procedures[txt_choose][txt_choose2][0], txt_in)

        if desc==None:
            QMessageBox.information(self, "Информация", "Процедура администрирования прошла успешно", QMessageBox.Ok)
            MW=MainWindow()
            self.hide()
        elif len(result)==0:
            QMessageBox.warning(self, "Предупреждение", "  Информации по запросу\nс данными параметрами нет", QMessageBox.Ok)
        else:    
            RW = ResultWindow()
            self.hide()

    def open_SecondMenuWindow_window(self):  
        global SMW      
        SMW = SecondMenuWindow()
        self.hide()    


# Window return result of request
class ResultWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI()
        self.connects()
        self.set_appear()
        self.show()

    def initUI(self):
        self.to_start_button= QPushButton('В начало', self)
        self.close_button= QPushButton('Закрыть', self)
        self.table = QTableWidget()  
        self.table.setColumnCount(len(result[0]))    
        self.table.setRowCount(len(result))
        self.table.setHorizontalHeaderLabels(desc)
        for i in range(len(result)):
            for j in range(len(result[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(result[i][j])))
        layout_col = QVBoxLayout()
        self.table.resizeColumnsToContents()
        layout_col.addWidget(self.table)
        layout_row = QHBoxLayout()
        layout_row.addWidget(self.to_start_button)
        layout_row.addWidget(self.close_button)
        layout_col.addLayout(layout_row)
        self.setLayout(layout_col)

    def set_appear(self):
        self.setWindowTitle('Result Window')
        self.resize(700, 900)
        self.move(625, 50)
        
    def connects(self):
        self.to_start_button.clicked.connect(self.open_MainWindow_window)
        self.close_button.clicked.connect(QCoreApplication.instance().quit)

    def open_MainWindow_window(self):
        global MW
        MW = MainWindow()
        self.hide()


class SecondMenuWindow(QWidget):
    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI()
        self.connects()
        self.set_appear()
        self.show()


    def initUI(self):
        self.choose_button2 = QPushButton('Выбрать', self)
        self.back_button = QPushButton('Назад', self)
        self.describe_txt2 = QLabel(desc_txt2)
        self.choose2 = QComboBox() 
        self.choose2.addItems(requests[txt_choose])
        layout_col = QVBoxLayout()
        layout_col.addWidget(self.describe_txt2, alignment=Qt.AlignCenter)
        layout_col.addWidget(self.choose2, alignment=Qt.AlignCenter)
        layout_row = QHBoxLayout()
        layout_row.addWidget(self.choose_button2)
        layout_row.addWidget(self.back_button)
        layout_col.addLayout(layout_row)
        self.setLayout(layout_col)


    def set_appear(self):
        self.setWindowTitle('SecondMenuWindow')
        self.resize(980, 300)
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()-100) // 2
        self.move(x, y)

    def connects(self):
        self.choose_button2.clicked.connect(self.open_next_window)
        self.back_button.clicked.connect(self.open_MainWindow_window)


    def open_next_window(self):
        global txt_choose2, IW, RW, desc
        txt_choose2=self.choose2.currentIndex()
        if len(procedures[txt_choose][txt_choose2])!=1:
            IW = InputWindow()
            self.hide()
        else:
            global result
            result, desc = execute_procedure(connection, procedures[txt_choose][txt_choose2][0],())
            RW = ResultWindow()
            self.hide()

    def open_MainWindow_window(self):
        global MW
        MW = MainWindow()
        self.hide()    


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
        self.choose.addItems(menu)
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
        self.resize(1000, 300)
        desktop = QApplication.desktop()
        x = (desktop.width() - self.frameSize().width()) // 2
        y = (desktop.height() - self.frameSize().height()-100) // 2
        self.move(x, y)

    def connects(self):
        self.choose_button.clicked.connect(self.open_SecondMenu_window)
        self.close_button.clicked.connect(QCoreApplication.instance().quit)

    def open_SecondMenu_window(self):
        global SMW, txt_choose
        txt_choose=self.choose.currentIndex()
        SMW = SecondMenuWindow()
        self.hide()

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    app.setFont(QFont("MerriWeather", 12))   
    pal = QPalette() 
    pal.setColor(QPalette.Window, QColor(204, 153, 254)) 
    pal.setColor(QPalette.Button, QColor(208, 202, 255)) 
    app.setPalette(pal)
    mW = MainWindow()
    app.exec()