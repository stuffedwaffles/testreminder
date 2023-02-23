print("EVENT INPUTTER STARTING")

from datetime import datetime as dt
import time as t
from plyer import notification
from twilio.rest import Client
import tkinter
from tkinter import *
import asyncio 
import sys
from PyQt6.QtWidgets import * 
from PyQt6.QtCore import *
from PyQt6.QtGui import * 
import os
import json

windowHeight = 200
windowWidth = 400

#get event file path
folder = os.path.dirname(os.path.abspath(__file__))
eventFilePath = os.path.join(folder, "events.json")

app = QApplication([])
class InputWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ENTER EVENT")
        self.setFixedSize(QSize(windowWidth, windowHeight*2))

        self.dialogLayout = QVBoxLayout()
        layout = QFormLayout()

        self.nameLine = QLineEdit()
        self.yearLine = QLineEdit()
        self.monthLine = QLineEdit()
        self.dayLine = QLineEdit()
        self.hourLine = QLineEdit()
        self.minuteLine = QLineEdit()
        self.secondLine = QLineEdit()

        layout.addRow("Event Name: ", self.nameLine)
        layout.addRow("Event Year: ", self.yearLine)
        layout.addRow("Event Month (number): ", self.monthLine)
        layout.addRow("Event Day: ", self.dayLine)
        layout.addRow("Event Hour (military time): ", self.hourLine)
        layout.addRow("Event Minute: ", self.minuteLine)
        layout.addRow("Event second: ", self.secondLine)
        self.dialogLayout.addLayout(layout)

        submit = QPushButton("Submit Event!")
        submit.clicked.connect(self.onSubmit)
        self.invalid_label = QLabel()

        self.dialogLayout.addWidget(submit)
        self.dialogLayout.addWidget(self.invalid_label)

        self.setLayout(self.dialogLayout)
    
    def onSubmit(self):
        global name
        name = str(self.nameLine.text())
        global year
        year = int(self.yearLine.text())
        global month
        month = int(self.monthLine.text())
        global day
        day = int(self.dayLine.text())
        global hour
        hour = int(self.hourLine.text())
        global minute
        minute = int(self.minuteLine.text())
        global second
        second = int(self.secondLine.text())
        if year<2023:
            self.invalid_label.setText("Invalid year!")
            self.invalid_label.setStyleSheet("color : red")
        elif month>12:
            self.invalid_label.setText("Invalid month!")
            self.invalid_label.setStyleSheet("color : red")
        elif (month==2 and day>28) or ((month==4 or month==6 or month==9 or month==11) and day>30) or day>31:
            self.invalid_label.setText("Invalid day!")
            self.invalid_label.setStyleSheet("color : red")
        elif hour>24:
            self.invalid_label.setText("Invalid hour!")
            self.invalid_label.setStyleSheet("color : red")
        elif minute >60:
            self.invalid_label.setText("Invalid minute!")
            self.invalid_label.setStyleSheet("color : red")
        elif second>60:
            self.invalid_label.setText("Invalid secpmd!")
            self.invalid_label.setStyleSheet("color : red")
        else:
            datetime_list = [year, month, day, hour, minute, second, 0]

            with open(eventFilePath, 'r') as f:
                events_dict = json.loads(f.read())
                events_dict[name] = datetime_list

            events_string = str(events_dict)
            events_string = events_string.replace("\'", "\"")
            with open(eventFilePath, 'w') as file:
                file.write(events_string)
                file.close()


            self.close()
        
        self.setLayout(self.dialogLayout)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EVENT GATHERER")
        self.setMinimumSize(QSize(windowWidth, windowHeight))
        self.setStyleSheet("background-color : gray")


        inputbtn = QPushButton("ENTER EVENT", self)
        inputbtn.setStyleSheet("background-color : white")
        inputbtn.setFixedSize(200,75)
        inputbtn.move(100,50)
        inputbtn.adjustSize()
        inputbtn.clicked.connect(self.input_window)

    def input_window(self,checked):
        self.w = InputWindow()
        self.w.show()



window = MainWindow()

window.show()
app.exec()


