import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# This file create signals that pressing either 'e' or 'i' will emit


class KeyboardWidget(QWidget):

    eReleased = pyqtSignal(str)
    iReleased = pyqtSignal(str)

    def keyReleaseEvent(self, keyEvent):

        # to prevent holding the key / frequent pressing to result in multiple signals being emitted
        if keyEvent.isAutoRepeat():
            return

        # when 'e' is released
        if keyEvent.text() == "e":
            self.eReleased.emit(keyEvent.text())

        # when 'i' is released
        if keyEvent.text() == "i":
            self.iReleased.emit(keyEvent.text())