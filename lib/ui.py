from PyQt4 import QtCore, QtGui, uic

class UIMainWindow(QtGui.QMainWindow):

    __ui_name__ = None

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        ui_name = self.__ui_name__ if self.__ui_name__ else self.__class__.__name__
        self._ui = uic.loadUi("ui/%s.ui" %ui_name, parent)

    def show(self):
        self._ui.show()

    def get_ui(self):
        return self._ui

class UIWidget(QtGui.QWidget):

    __ui_name__ = None

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        ui_name = self.__ui_name__ if self.__ui_name__ else self.__class__.__name__
        self._ui = uic.loadUi("ui/%s.ui" %ui_name, self)

    def get_ui(self):
        return self._ui