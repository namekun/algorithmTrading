import sys
from PyQt5.QtWidgets import *

def clicked_slot():
    print("clicked")

app = QApplication(sys.argv)
label = QPushButton("Hello PyQt")
label.show()

print("Before event loop")
app.exec_()
print("After event loop")