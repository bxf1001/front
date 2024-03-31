import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QDateEdit, QHBoxLayout, QLabel
from PyQt5.QtCore import QDate

# Load data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Define the main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Display")
        self.setGeometry(100, 100, 1200, 600)
        self.createTable()

        # Set the layout
        layout = QVBoxLayout()
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("From Date:"))
        date_layout.addWidget(self.date_from)
        date_layout.addWidget(QLabel("To Date:"))
        date_layout.addWidget(self.date_to)
        layout.addLayout(date_layout)
        layout.addWidget(self.tableWidget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def createTable(self):
        # Create date range selection widgets
        self.date_from = QDateEdit(calendarPopup=True)
        self.date_to = QDateEdit(calendarPopup=True)
        self.date_from.setDate(QDate.currentDate().addDays(-30))  # Default to 30 days ago
        self.date_to.setDate(QDate.currentDate())  # Default to today

        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(data) * 2 + 1)  # 2 rows for each date entry (video and audio) + 1 for grand total
        self.tableWidget.setColumnCount(len(data[list(data.keys())[0]]) - 1)  # Number of blocks + S.No + Date - Grand total
        headers = ["S.No", "Date"] + [block for block in data[list(data.keys())[0]] if block not in ['total', 'Grand total']]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Populate the table with data
        row = 0
        for date, values in data.items():
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(row // 2 + 1)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(date))
            col = 2
            for block, stats in values.items():
                if block not in ['total', 'Grand total']:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(stats['video'])))
                    self.tableWidget.setItem(row + 1, col, QTableWidgetItem(str(stats['audio'])))
                    col += 1
            row += 2

        # Add total and grand total in the last row
        self.tableWidget.setItem(len(data) * 2, 1, QTableWidgetItem("Total"))
        self.tableWidget.setItem(len(data) * 2, 2, QTableWidgetItem(str(values['total']['video'])))
        self.tableWidget.setItem(len(data) * 2, 3, QTableWidgetItem(str(values['total']['audio'])))
        self.tableWidget.setItem(len(data) * 2, 4, QTableWidgetItem(str(values['Grand total'])))

        self.tableWidget.resizeColumnsToContents()

# Run the application
app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
