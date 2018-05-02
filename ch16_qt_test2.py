import sys

from pyqt5_QtWidgets import *

def clicked_slot():
    print("clicked!")

app = QApplication(sys.argv)

btn = QPushButton("Hello, PyQT")
btn.clicked.connect(clicked_slot())
btn.show()

app.exec_()