# Import necessary libraries
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor ,QTextCharFormat
import sys
import json
from datetime import datetime
from qt_material import apply_stylesheet

class DataEntryApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.initUI()

    def initUI(self):
        # Main layout
        self.layout = QtWidgets.QGridLayout(self)
        self.setWindowTitle('Phone Portal Data Entry')
        self.setGeometry(0, 0, 500, 400)
        
        # Calendar widget

        self.calendar = QtWidgets.QCalendarWidget(self)
        self.layout.addWidget(self.calendar, 0, 0, 1, 3)
        self.loadCalendarData()

        
        # Headers
        self.videoHeader = QtWidgets.QLabel('Video Calls', self)
        self.audioHeader = QtWidgets.QLabel('Audio Calls', self)
        self.layout.addWidget(self.videoHeader, 1, 1)
        self.layout.addWidget(self.audioHeader, 1, 2)
        
        # Block labels and input fields
        block_names = ['AB-Block-1', 'AB-Block-2', 'Cellular-Block', 'HS-Block', 'A-Class', 'Quratine', 'Hospital','Emulakath']
        
        # Block labels and input fields
        self.blocks = []
        for i, name in enumerate(block_names):
            block_label = QtWidgets.QLabel(name, self)
            video_input = QtWidgets.QLineEdit(self)
            audio_input = QtWidgets.QLineEdit(self)
            
            # Set maximum length for input fields
            video_input.setMaxLength(5)
            audio_input.setMaxLength(5)
            
            # Connect signals
            video_input.textChanged.connect(self.updateSums)
            audio_input.textChanged.connect(self.updateSums)
            
            self.blocks.append((block_label, video_input, audio_input))
            self.layout.addWidget(block_label, i+2, 0)
            self.layout.addWidget(video_input, i+2, 1)
            self.layout.addWidget(audio_input, i+2, 2)
        # Sum and Grand Total Labels
        self.videoSumLabel = QtWidgets.QLabel('Video Sum: 0', self)
        self.audioSumLabel = QtWidgets.QLabel('Audio Sum: 0', self)
        self.grandTotalLabel = QtWidgets.QLabel('Grand Total: 0', self)
        self.layout.addWidget(self.videoSumLabel, 11, 1)
        self.layout.addWidget(self.audioSumLabel, 11, 2)
        self.layout.addWidget(self.grandTotalLabel, 12, 1, 1, 2)
        
        # Buttons
        
        self.saveButton = QtWidgets.QPushButton('Save Data', self)
        self.retrieveButton = QtWidgets.QPushButton('Retrieve Data', self)
        self.layout.addWidget(self.saveButton, 13, 1)
        self.layout.addWidget(self.retrieveButton, 13, 2)


        # Reset Button
        self.resetButton = QtWidgets.QPushButton('Reset', self)
        self.layout.addWidget(self.resetButton, 14, 1)
        self.resetButton.clicked.connect(self.resetFields)

        # Load Button
        self.loadButton = QtWidgets.QPushButton('Load Data', self)
        self.layout.addWidget(self.loadButton, 14, 2)
        
        
        # Signals
        self.loadButton.clicked.connect(self.loadData)
        self.saveButton.clicked.connect(self.saveData)
        self.retrieveButton.clicked.connect(self.retrieveData)

    def updateSums(self):
        video_sum = sum(int(block[1].text() or 0) for block in self.blocks)
        audio_sum = sum(int(block[2].text() or 0) for block in self.blocks)
        grand_total = video_sum + audio_sum
        
        self.videoSumLabel.setText(f'Video Sum: {video_sum}')
        self.audioSumLabel.setText(f'Audio Sum: {audio_sum}')
        self.grandTotalLabel.setText(f'Grand Total: {grand_total}')

    def resetFields(self):
        # Clear all input fields
        for _, video_input, audio_input in self.blocks:
            video_input.clear()
            audio_input.clear()
        self.updateSums()

    def loadData(self):
        # Load data for the selected date
        date_str = self.calendar.selectedDate().toString(QtCore.Qt.ISODate)
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
            if date_str in self.data:
                # New block names mapping
                block_names = ['AB-Block-1', 'AB-Block-2', 'Cellular-Block', 'HS-Block', 'A-Class', 'Quarantine', 'Hospital']
                for i, block in enumerate(self.blocks, start=1):
                    block_name = block_names[i-1] if i <= len(block_names) else f'block_{i}'
                    block_data = self.data[date_str].get(block_name, {})
                    block[1].setText(str(block_data.get('video', '')))
                    block[2].setText(str(block_data.get('audio', '')))
                self.updateSums()
        except FileNotFoundError:
            print("Data file not found. Starting with empty data.")
        except json.JSONDecodeError:
            print("Data file is not in valid JSON format.")


    def saveData(self):
        date_str = self.calendar.selectedDate().toString(QtCore.Qt.ISODate)
        self.data[date_str] = {'total': {'video': 0, 'audio': 0}, 'Grand total': 0}
        
        # New block names mapping
        block_names = ['AB-Block-1', 'AB-Block-2', 'Cellular-Block', 'HS-Block', 'A-Class', 'Quarantine', 'Hospital','Emulakath']
        
        for i, block in enumerate(self.blocks, start=1):
            video = int(block[1].text() or 0)
            audio = int(block[2].text() or 0)
            block_name = block_names[i-1] if i <= len(block_names) else f'block_{i}'
            self.data[date_str][block_name] = {'video': video, 'audio': audio}
            self.data[date_str]['total']['video'] += video
            self.data[date_str]['total']['audio'] += audio
        
        self.data[date_str]['Grand total'] = self.data[date_str]['total']['video'] + self.data[date_str]['total']['audio']
    
    # Save to JSON file
        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=4)


    def loadCalendarData(self):
        # Load the data to check which dates have entries
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
            for date_str in self.data:
                date = QtCore.QDate.fromString(date_str, "yyyy-MM-dd")
                format = QTextCharFormat()
                format.setForeground(QColor('grey'))
                self.calendar.setDateTextFormat(date, format)
        except Exception as e:
            print(f"An error occurred: {e}")

    def formatDateCells(self):
        # Load the data to check which dates have entries
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
            for date_str in self.data:
                date = QtCore.QDate.fromString(date_str, "yyyy-MM-dd")
                format = QtWidgets.QTextCharFormat()
                format.setBackground(QColor('lightgrey'))
                self.calendar.setDateTextFormat(date, format)
        except Exception as e:
            print(f"An error occurred: {e}")

    def retrieveData(self):
        # Logic to retrieve data and display it in a new window
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = DataEntryApp()
    apply_stylesheet(app, theme='dark_teal.xml')
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
