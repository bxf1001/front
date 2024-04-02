from PyQt5 import QtWidgets, QtCore
import sys
import json
from datetime import datetime, timedelta

class RetrieveDataApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Retrieve Data')
        self.setGeometry(100, 100, 600, 400)

        layout = QtWidgets.QVBoxLayout(self)

        # Date range selection
        date_range_layout = QtWidgets.QHBoxLayout()
        self.from_label = QtWidgets.QLabel('From:', self)
        self.to_label = QtWidgets.QLabel('To:', self)
        self.from_date = QtWidgets.QDateEdit(self)
        self.to_date = QtWidgets.QDateEdit(self)
        self.from_date.setCalendarPopup(True)
        self.to_date.setCalendarPopup(True)
        # Set "from" date to 30 days before current date
        thirty_days_ago = datetime.now() - timedelta(days=30)
        self.from_date.setDate(QtCore.QDate(thirty_days_ago.year, thirty_days_ago.month, thirty_days_ago.day))
        # Set "to" date to current date
        self.to_date.setDate(QtCore.QDate.currentDate())
        date_range_layout.addWidget(self.from_label)
        date_range_layout.addWidget(self.from_date)
        date_range_layout.addWidget(self.to_label)
        date_range_layout.addWidget(self.to_date)
        layout.addLayout(date_range_layout)

        # Button to retrieve data
        self.retrieve_button = QtWidgets.QPushButton('Retrieve', self)
        layout.addWidget(self.retrieve_button)

        # Table to display retrieved data
        self.table = QtWidgets.QTableWidget(self)
        layout.addWidget(self.table)

        # Connect signals
        self.retrieve_button.clicked.connect(self.retrieveData)

    def retrieveData(self):
        from_date = self.from_date.date().toString(QtCore.Qt.ISODate)
        to_date = self.to_date.date().toString(QtCore.Qt.ISODate)
        data = self.loadData(from_date, to_date)
        self.displayData(data)

    def loadData(self, from_date, to_date):
        try:
            with open('data.json', 'r') as f:
                all_data = json.load(f)
            # Filter data within the date range
            filtered_data = {date: all_data[date] for date in all_data if from_date <= date <= to_date}
            return filtered_data
        except FileNotFoundError:
            print("Data file not found.")
            return {}
        except json.JSONDecodeError:
            print("Data file is not in valid JSON format.")
            return {}

    def displayData(self, data):
        self.table.clear()
        if not data:
            QtWidgets.QMessageBox.information(self, 'No Data', 'No data available for the selected date range.')
            return
        self.table.setRowCount(len(data))
        self.table.setColumnCount(9)  # Assuming 9 columns for the block names
        headers = ['Date'] + ['AB-Block-1', 'AB-Block-2', 'Cellular-Block', 'HS-Block', 'A-Class', 'Quarantine', 'Hospital', 'Emulakath'] + ['Video', 'Audio']
        self.table.setHorizontalHeaderLabels(headers)
        row = 0
        for date, blocks_data in data.items():
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(date))
            for col, block_name in enumerate(headers[1:], start=1):
                if block_name in blocks_data:
                    self.table.setItem(row, col, QtWidgets.QTableWidgetItem(str(blocks_data[block_name])))
            row += 1

def main():
    app = QtWidgets.QApplication(sys.argv)
    retrieve_data_app = RetrieveDataApp()
    retrieve_data_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
