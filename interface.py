from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget



class Ui_MainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setWindowTitle("Склад підприємства")
        mainWindow.setGeometry(200, 100, 1200, 900)

        self.central_widget = QWidget()
        mainWindow.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QtWidgets.QLabel("Супер система складу підприємства")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(QtGui.QFont("Arial", 20))
        self.layout.addWidget(self.label)

        self.tabs = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tabs)
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tabs.addTab(self.tab1, "База даних")
        self.tabs.addTab(self.tab2, "Аналітика")
        self.layout_2 = QVBoxLayout(self.tab1)

        self.search_box = QtWidgets.QWidget()
        self.layout_2.addWidget(self.search_box)
        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_box.setLayout(self.search_layout)
        self.search_line = QtWidgets.QLineEdit()
        self.find_button = QtWidgets.QPushButton("Пошук")
        self.search_layout.addWidget(self.search_line)
        self.search_layout.addWidget(self.find_button)

        self.table_widget = MyTableWidget(self.tab1)
        self.layout_2.addWidget(self.table_widget)
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(9)

        self.button_container = QtWidgets.QWidget()
        self.layout_2.addWidget(self.button_container)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_container.setLayout(self.button_layout)

        self.add_button = QtWidgets.QPushButton("Додати річ")
        self.add_button.setFixedWidth(100)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QtWidgets.QPushButton("Видалити річ")
        self.delete_button.setFixedWidth(100)
        self.button_layout.addWidget(self.delete_button)

        self.save_button = QtWidgets.QPushButton("Зберегти зміни")
        self.save_button.setFixedWidth(100)
        self.button_layout.addWidget(self.save_button)

        self.layout_3 = QVBoxLayout(self.tab2)
        self.statistic_buttons = QtWidgets.QWidget()
        self.statistic_buttons.setFixedHeight(50)
        self.layout_3.addWidget(self.statistic_buttons)
        self.statistic_layout = QtWidgets.QHBoxLayout()
        self.statistic_buttons.setLayout(self.statistic_layout)
        self.by_warehouse_button = QtWidgets.QPushButton("Одиниці товару на складі")
        self.by_warehouse_button.setMinimumWidth(200)
        self.statistic_layout.addWidget(self.by_warehouse_button, stretch=1)
        self.avg_rating_warehouse_button = QtWidgets.QPushButton("Середня оцінка товарів складу")
        self.avg_rating_warehouse_button.setMinimumWidth(200)
        self.statistic_layout.addWidget(self.avg_rating_warehouse_button, stretch=1)
        self.all_prices_button = QtWidgets.QPushButton("Вартість товарів")
        self.all_prices_button.setMinimumWidth(200)
        self.statistic_layout.addWidget(self.all_prices_button, stretch=1)
        self.amount_by_date_button = QtWidgets.QPushButton("Кількість товарів по даті")
        self.amount_by_date_button.setMinimumWidth(200)
        self.statistic_layout.addWidget(self.amount_by_date_button, stretch=1)

        self.date_info = QtWidgets.QWidget()
        self.date_info.setVisible(False)
        self.layout_3.addWidget(self.date_info)
        self.date_layout = QtWidgets.QHBoxLayout()
        self.date_info.setLayout(self.date_layout)
        self.date_layout.addStretch(2)
        self.date_label = QtWidgets.QLabel("Початкова дата:")
        self.date_layout.addWidget(self.date_label)
        self.date_picker1 = QtWidgets.QDateEdit()
        self.date_picker1.setDate(QDate(2020, 1, 1))
        self.date_picker1.setCalendarPopup(True)
        self.date_layout.addWidget(self.date_picker1, stretch=1)
        self.date_layout.addSpacerItem(QtWidgets.QSpacerItem(20, 20))
        self.date_label2 = QtWidgets.QLabel("Кінцева дата:")
        self.date_layout.addWidget(self.date_label2)
        self.date_picker2 = QtWidgets.QDateEdit()
        self.date_picker2.setDate(QDate.currentDate())
        self.date_picker2.setCalendarPopup(True)
        self.date_layout.addWidget(self.date_picker2, stretch=1)
        self.date_layout.addSpacerItem(QtWidgets.QSpacerItem(20, 20))
        self.submit_date = QtWidgets.QPushButton("Встановити дати")
        self.date_layout.addWidget(self.submit_date, stretch=1)
        self.submit_date.setFixedWidth(200)


        self.plots = QtWidgets.QWidget()
        self.layout_3.addWidget(self.plots)



class MyTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def resizeEvent(self, event):
        # Call the base class implementation
        super().resizeEvent(event)

        viewport_width = self.viewport().width()

        ratios = [0.1, 0.15, 0.35, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1]
        for i in range(self.columnCount()):
            self.setColumnWidth(i, int(ratios[i] * viewport_width))