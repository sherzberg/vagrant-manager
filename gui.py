from PyQt4 import QtCore, QtGui, uic
from lib.ui import UIMainWindow, UIWidget
from util import VagrantThread
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

        self.thread = VagrantThread()
        self.connect(self.thread, QtCore.SIGNAL("started()"), self.on_async_start)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.on_async_stop)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.on_async_stop)
        self.connect(self.thread, QtCore.SIGNAL("complete(QString)"), self.on_async_complete)

    def up(self):
        self.thread.do_action('up', self.get_root())

    def suspend(self):
        self.thread.do_action('suspend', self.get_root())

    def resume(self):
        self.thread.do_action('resume', self.get_root())

    def destroy(self):
        self.thread.do_action('destroy', self.get_root())

    def status(self):
        self.thread.do_action('status', self.get_root())

    def get_root(self):
        root = str(self.get_ui().text_root.text())
        return root

    def get_vagrant(self):
        return Vagrant(self.get_root())

    def set_status(self, msg, length=5000):
        self.emit(QtCore.SIGNAL("vagrant_status(QString)"), msg)
        print msg

    def on_async_start(self):
        print 'ASYNC: start'
        self._enable_buttons(False)
        self.get_ui().progress_bar.show()

    def on_async_stop(self):
        print 'ASYNC: stop'
        self._enable_buttons(True)
        self.get_ui().progress_bar.hide()

    def on_async_complete(self, msg):
        if Vagrant.RUNNING == msg:
            self.set_status("Vagrant root %s is Running" % self.get_root())
        elif Vagrant.NOT_CREATED:
            self.set_status("Vagrant root %s is Not Created" % self.get_root())
        elif Vagrant.POWEROFF:
            self.set_status("Vagrant root %s is Powered Off" % self.get_root())


    def _enable_buttons(self, enabled=True):
        for button in [self.get_ui().button_up, self.get_ui().button_suspend, self.get_ui().button_resume, self.get_ui().button_destroy, self.get_ui().button_status]:
            button.setEnabled(enabled)


class MainWindow(UIMainWindow):
    def __init__(self):
        UIMainWindow.__init__(self)

        self.setWindowTitle("Vagrant Manager")

        self.vagrant_widget = VagrantWidget(self)
        self.get_ui().vagrant_widget_layout.addWidget(self.vagrant_widget)
        self.vagrant_widget.show()

        self.connect(self.vagrant_widget, QtCore.SIGNAL("vagrant_status(QString)"), self.on_vagrant_status)

    def on_vagrant_status(self, msg):
        self.set_status(msg)

    def set_status(self, msg, length=5000):
        self.get_ui().statusbar.showMessage(msg, length)
