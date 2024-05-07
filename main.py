import sys
from datetime import datetime
import plotly.graph_objects as go
from plotly.offline import plot
from db_interaction import DBService


import pymongo
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import QLocale
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QDate
from PyQt5.QtWebEngineWidgets import QWebEngineView


from interface import Ui_MainWindow


class MyWindow(QMainWindow):
    def __init__(self, collection):
        super().__init__()

        self.db_coll = collection
        self.new_rows = []
        self.edited_rows = []

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.webview = QWebEngineView()
        self.ui.layout_3.addWidget(self.webview)
        self.webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.ui.find_button.clicked.connect(self.filter_data)
        self.ui.search_line.textChanged.connect(self.filter_data)
        self.ui.add_button.clicked.connect(self.add_row)
        self.ui.save_button.clicked.connect(self.save_changes)
        self.ui.delete_button.clicked.connect(self.delete_row)

        self.ui.by_warehouse_button.clicked.connect(self.by_warehouse)
        self.ui.avg_rating_warehouse_button.clicked.connect(self.avg_rating_in_warehouse)
        self.ui.all_prices_button.clicked.connect(self.prices_plot)
        self.ui.amount_by_date_button.clicked.connect(self.amount_by_date_helper)
        self.ui.submit_date.clicked.connect(self.warehouses_amount_by_date)

        self.draw_table()
        self.ui.table_widget.cellChanged.connect(self.mark_edited)




    def draw_table(self):
        data = self.db_coll.get_all()
        table = self.ui.table_widget

        header = ["Інвентарний номер", "Назва", "Опис", "Склад", "Оцінка", "Кількість", "Ціна", "Дата додачі", "Дата зміни"]
        table.setHorizontalHeaderLabels(header)
        for i, d in enumerate(data):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(str(d['inv_num'])))
            table.setItem(i, 1, QTableWidgetItem(str(d['name'])))
            table.setItem(i, 2, QTableWidgetItem(str(d['desc'])))
            table.setItem(i, 3, QTableWidgetItem(str(d['warehouse'])))
            table.setItem(i, 4, QTableWidgetItem(str(d['rating'])))
            table.setItem(i, 5, QTableWidgetItem(str(d['quantity'])))
            table.setItem(i, 6, QTableWidgetItem(str(d['price'])))
            table.setItem(i, 7, QTableWidgetItem(QDate(d['date_added']).toString("dd.MM.yyyy")))
            table.setItem(i, 8, QTableWidgetItem(QDate(d['date_changed']).toString("dd.MM.yyyy")))

    def filter_data(self):
        text = self.ui.search_line.text()

        for i in range(self.ui.table_widget.rowCount()):
            self.ui.table_widget.setRowHidden(i, False)

        if text:
            for i in range(self.ui.table_widget.rowCount()):
                if (text.lower() not in self.ui.table_widget.item(i, 1).text().lower() and
                        text.lower() not in self.ui.table_widget.item(i, 2).text().lower() and
                        text.lower() not in self.ui.table_widget.item(i, 0).text().lower()):
                    self.ui.table_widget.setRowHidden(i, True)

    def add_row(self):
        row_position = self.ui.table_widget.rowCount()
        self.new_rows.append(row_position)
        self.ui.table_widget.insertRow(row_position)

        for i in range(self.ui.table_widget.columnCount()):
            item = QTableWidgetItem("")
            item.setBackground(QColor(144, 238, 144))
            self.ui.table_widget.setItem(row_position, i, item)

        self.ui.table_widget.scrollToItem(self.ui.table_widget.item(row_position, 0))


    def save_changes(self):
        self.ui.table_widget.cellChanged.disconnect()
        for row in self.new_rows:
            inv_num = self.ui.table_widget.item(row, 0).text()
            name = self.ui.table_widget.item(row, 1).text()
            desc = self.ui.table_widget.item(row, 2).text()
            warehouse = self.ui.table_widget.item(row, 3).text()
            rating = int(self.ui.table_widget.item(row, 4).text())
            quantity = int(self.ui.table_widget.item(row, 5).text())
            price = int(self.ui.table_widget.item(row, 6).text())
            date_added = datetime.strptime(self.ui.table_widget.item(row, 7).text(), "%d.%m.%Y")
            date_changed = datetime.strptime(self.ui.table_widget.item(row, 8).text(), "%d.%m.%Y")

            self.db_coll.insert_one(inv_num, name, desc, warehouse, rating, quantity, price, date_added, date_changed)

        for row in self.edited_rows:
            inv_num = self.ui.table_widget.item(row, 0).text()
            name = self.ui.table_widget.item(row, 1).text()
            desc = self.ui.table_widget.item(row, 2).text()
            warehouse = self.ui.table_widget.item(row, 3).text()
            rating = int(self.ui.table_widget.item(row, 4).text())
            quantity = int(self.ui.table_widget.item(row, 5).text())
            price = int(self.ui.table_widget.item(row, 6).text())
            date_added = datetime.strptime(self.ui.table_widget.item(row, 7).text(), "%d.%m.%Y")
            date_changed = datetime.strptime(self.ui.table_widget.item(row, 8).text(), "%d.%m.%Y")

            self.db_coll.update_one(inv_num, name, desc, warehouse, rating, quantity, price, date_added, date_changed)

        self.new_rows = []
        self.edited_rows = []
        self.ui.table_widget.clearContents()
        self.ui.table_widget.setRowCount(0)
        self.draw_table()
        self.ui.table_widget.cellChanged.connect(self.mark_edited)


    def delete_row(self):
        selected = self.ui.table_widget.selectedItems()
        if selected:
            row = selected[0].row()
            self.db_coll.delete_one(self.ui.table_widget.item(row, 0).text())
            self.ui.table_widget.removeRow(row)
            self.ui.table_widget.clearContents()
            self.ui.table_widget.setRowCount(0)
            self.draw_table()

    def mark_edited(self, row):
        if row not in self.edited_rows:
            self.edited_rows.append(row)

    def by_warehouse(self):
        self.ui.date_info.setVisible(False)


        data = self.db_coll.get_amount_by_warehouse()
        warehouses = []
        quantities = []
        for d in data:
            warehouses.append(d["_id"])
            quantities.append(d["total"])

        fig = go.Figure(data=go.Pie(labels=warehouses, values=quantities))
        fig.update_layout(title="Одиниці товару на складі")
        html_content = plot(fig, output_type="div", include_plotlyjs='cdn')
        self.webview.setHtml(html_content)


    def avg_rating_in_warehouse(self):
        self.ui.date_info.setVisible(False)


        data = self.db_coll.get_avg_rating_in_warehouse()
        warehouses = []
        ratings = []

        for d in data:
            warehouses.append(d["_id"])
            ratings.append(d["avg_rating"])

        fig = go.Figure(data=go.Bar(x=warehouses, y=ratings))
        fig.update_layout(title="Середня оцінка товарів на складі", xaxis_title="Склад", yaxis_title="Середня оцінка")
        html_content = plot(fig, output_type="div", include_plotlyjs='cdn')
        self.webview.setHtml(html_content)

    def prices_plot(self):
        self.ui.date_info.setVisible(False)

        data = self.db_coll.get_all()
        prices = []
        inventory_numbers = []
        for d in data:
            prices.append(d["price"])
            inventory_numbers.append(d["inv_num"])

        fig = go.Figure(data=go.Scatter(x=inventory_numbers, y=prices))
        fig.update_layout(title="Вартість товарів", xaxis_title="Інвентарний номер", yaxis_title="Ціна")
        html_content = plot(fig, output_type="div", include_plotlyjs='cdn')
        self.webview.setHtml(html_content)

    def amount_by_date_helper(self):
        self.webview.setHtml("")
        self.ui.date_info.setVisible(True)

    def warehouses_amount_by_date(self):
        self.ui.date_info.setVisible(False)

        start_date = datetime.strptime(self.ui.date_picker1.date().toString("yyyy-MM-dd"), "%Y-%m-%d")
        end_date = datetime.strptime(self.ui.date_picker2.date().toString("yyyy-MM-dd"), "%Y-%m-%d")

        data = self.db_coll.get_amount_by_date(start_date, end_date)
        warehouses = []
        quantities = []
        for d in data:
            warehouses.append(d["_id"])
            quantities.append(d["total"])

        fig = go.Figure(data=go.Bar(x=warehouses, y=quantities))
        fig.update_layout(title="Кількість доданих товарів за період", xaxis_title="Склад", yaxis_title="Кількість")
        html_content = plot(fig, output_type="div", include_plotlyjs='cdn')
        self.webview.setHtml(html_content)




if __name__ == "__main__":
    collection = DBService('mongodb://localhost:27017', "warehouse", "goods")

    app = QApplication(sys.argv)
    locale = QLocale(QLocale.Ukrainian, QLocale.Ukraine)
    QLocale.setDefault(locale)
    window = MyWindow(collection)
    window.show()
    sys.exit(app.exec_())
