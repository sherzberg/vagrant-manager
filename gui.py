from PyQt4 import QtCore, QtGui, uic
from lib.ui import UIMainWindow, UIWidget
import sys

from vagrant import Vagrant

class VagrantWidget(UIWidget):

    def __init__(self, parent=None):
        super(VagrantWidget, self).__init__(parent)

        self.get_ui().progress_bar.hide()

        self.connect(self.get_ui().button_up, QtCore.SIGNAL("clicked()"), self.up)
        self.connect(self.get_ui().button_suspend, QtCore.SIGNAL("clicked()"), self.suspend)
        self.connect(self.get_ui().button_resume, QtCore.SIGNAL("clicked()"), self.resume)
        self.connect(self.get_ui().button_status, QtCore.SIGNAL("clicked()"), self.status)
        self.connect(self.get_ui().button_destroy, QtCore.SIGNAL("clicked()"), self.destroy)

        if sys.platform == 'win32':
            self.get_ui().text_root.setText("C:\\Users\\sherzberg\\workspace\\CQRS\\vagrant-services")
        else:
            self.get_ui().text_root.setText("/home/sherzberg/workspace/vagrant-testing")

    def up(self):
        print 'UP', self.get_root()
        self.get_vagrant().up()
        print 'DONE'
        self.set_status("Up: " + self.get_root())

    def suspend(self):
        print 'SUSPEND', self.get_root()
        self.get_vagrant().suspend();
        print 'DONE'
        self.set_status("Suspend: " + self.get_root())

    def resume(self):
        print 'RESUME', self.get_root()
        self.get_vagrant().resume()
        print 'DONE'
        self.set_status("Resume: " + self.get_root())

    def destroy(self):
        print 'DESTROY', self.get_root()
        self.get_vagrant().destroy()
        print 'DONE'
        self.set_status("Destroyed: " + self.get_root())

    def status(self):
        self.on_async_start()
        print 'STATUS', self.get_vagrant().status()
        self.set_status("Status: " + self.get_vagrant().status())
        self.on_async_stop()

    def get_root(self):
        root = str(self.get_ui().text_root.text())
        return root

    def get_vagrant(self):
        return Vagrant(self.get_root())

    def set_status(self, msg, length=5000):
#        self.get_ui().statusbar.showMessage(msg, length)
#        self.emit("status(QSTring, QInteger)", QString(msg), length)
        pass

    def on_async_start(self):
        self.get_ui().progress_bar.show();

    def on_async_stop(self):
        self.get_ui().progress_bar.hide();

class MainWindow(UIMainWindow):
    
    def __init__(self):
        UIMainWindow.__init__(self)

        self.setWindowTitle("Vagrant Manager")

        self.vagrant_widget = VagrantWidget(self)
        self.get_ui().vagrant_widget_layout.addWidget(self.vagrant_widget)
        self.vagrant_widget.show()

    def set_status(self, msg, length=5000):
        self.get_ui().statusbar.showMessage(msg, length)
