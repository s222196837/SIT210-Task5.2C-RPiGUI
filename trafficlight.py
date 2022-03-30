#!/usr/bin/env python

import sys
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QWidget
from PyQt5.QtWidgets import QGridLayout, QPushButton, QRadioButton
from PyQt5.QtCore import QCoreApplication, QTimer

# allocated pin numbers
RED = 36
BLUE = 22
GREEN = 8


class LED:
    def __init__(self, pins):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) # use physical pin numbering
        for pin in pins:
            print("Setup pin", pin)
            GPIO.setup(pin, GPIO.OUT, initial = GPIO.LOW)

    def on(self, pin):
        GPIO.output(pin, GPIO.HIGH) # on
        print("LED on", pin)

    def off(self, pin):
        GPIO.output(pin, GPIO.LOW) # off
        print("LED off", pin)


class App(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.initUI(title)
        self.light = LED([RED, GREEN, BLUE])

    def initUI(self, title):
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 150)
        self.setFixedSize(400, 150)

        central = QWidget()
        self.setCentralWidget(central)
        grid = QGridLayout(central)
        grid.setContentsMargins(40, 22, 20, 0)

        # Create radio buttons
        self.radio1 = QRadioButton("Red")
        self.radio1.pin = RED
        self.radio1.toggled.connect(self.toggle)
        self.radio2 = QRadioButton("Green")
        self.radio2.pin = GREEN
        self.radio2.toggled.connect(self.toggle)
        self.radio3 = QRadioButton("Blue")
        self.radio3.toggled.connect(self.toggle)
        self.radio3.pin = BLUE

        # Create quit button
        self.finish = QPushButton('Quit', self)
        self.finish.clicked.connect(QCoreApplication.instance().quit)

        # Assemble everything in a grid and then reveal
        grid.addWidget(self.radio1, 0, 0)
        grid.addWidget(self.radio2, 0, 1)
        grid.addWidget(self.radio3, 0, 2)
        grid.addWidget(self.finish, 1, 2)
        self.show()

    def toggle(self):
        radio = self.sender()
        if radio.isChecked():
            self.light.on(radio.pin)
        else:
            self.light.off(radio.pin)


# main
app = QApplication(sys.argv)
me = App('Traffic Light LED')
sys.exit(app.exec_())
