from PyQt4 import QtCore

from vagrant import Vagrant

class VagrantThread(QtCore.QThread):
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent, command, root)
        self.command = command
        self.root = root

    def run(self):
        return_val = Vagrant(self.root)

        methodToCall = getattr(Vagrant(self.root), self.command)
        result = methodToCall()

        self.emit(QtCore.SIGNAL("Complete( QString )"),result)