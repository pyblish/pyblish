import sys
from PyQt5 import QtCore, QtWidgets


app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QWidget()

label = QtWidgets.QLabel("Initial state")
button1 = QtWidgets.QPushButton("Button 1")
quitbutton = QtWidgets.QPushButton("Quit")

layout = QtWidgets.QVBoxLayout(window)
layout.addWidget(label)
layout.addWidget(button1)
layout.addWidget(quitbutton)
layout.setAlignment(QtCore.Qt.AlignTop)

window.setMinimumSize(300, 400)
window.show()

s1 = QtCore.QState()
s11 = QtCore.QState(s1)
s12 = QtCore.QState(s1)
s13 = QtCore.QState(s1)
s2 = QtCore.QState()
s3 = QtCore.QFinalState()

s11.assignProperty(label, "text", "Welcome")
s12.assignProperty(label, "text", "Processing..")
s13.assignProperty(label, "text", "Finished")

s2.assignProperty(label, "text", "Quitting..")

s11.addTransition(button1.clicked, s12)
s12.addTransition(button1.clicked, s13)
s13.addTransition(button1.clicked, s11)
s1.addTransition(quitbutton.clicked, s2)
s2.addTransition(s2.entered, s3)  # Transient
s12.addTransition(quitbutton.clicked, s12)


def quit():
    QtCore.QTimer.singleShot(1000, app.quit)

s1.setInitialState(s11)
machine = QtCore.QStateMachine(window)
machine.addState(s1)
machine.addState(s2)
machine.addState(s3)
machine.setInitialState(s1)
machine.finished.connect(quit)
machine.start()

app.exec_()
