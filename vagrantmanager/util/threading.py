from PyQt4 import QtCore

from vagrantmanager.util.vagrant import Vagrant

class VagrantThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)

    def do_action(self, command, root):
        self.command = command
        self.root = root
        self.start()

    def run(self):
        return_val = Vagrant(self.root)

        methodToCall = getattr(Vagrant(self.root), self.command)
        result = methodToCall()

        result = result if result != None else ''

        self.emit(QtCore.SIGNAL("complete(QString)"),result)

    def __del__(self):
        self.exiting = True
        self.wait()