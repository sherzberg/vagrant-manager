from PyQt4 import QtCore, QtGui, uic
from lib.ui import UIMainWindow, UIWidget
from vagrantmanager.util import VagrantThread
import sys, os
from datetime import datetime

from vagrant import Vagrant

class VagrantWidget(UIWidget):
    def __init__(self, parent=None):
        super(VagrantWidget, self).__init__(parent)

        self.get_ui().progress_bar.setValue(0)
        self.get_ui().progress_bar.setMaximum(100)

        self.connect(self.get_ui().button_up, QtCore.SIGNAL("clicked()"), self.up)
        self.connect(self.get_ui().button_suspend, QtCore.SIGNAL("clicked()"), self.suspend)
        self.connect(self.get_ui().button_resume, QtCore.SIGNAL("clicked()"), self.resume)
        self.connect(self.get_ui().button_status, QtCore.SIGNAL("clicked()"), self.status)
        self.connect(self.get_ui().button_destroy, QtCore.SIGNAL("clicked()"), self.destroy)

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

    def set_root(self, root):
        self.get_ui().text_root.setText(root)

    def get_vagrant(self):
        return Vagrant(self.get_root())

    def set_status(self, msg, length=5000):
        self.emit(QtCore.SIGNAL("vagrant_status(QString)"), msg)
        print msg
        self.get_ui().label_status.setText(msg)
        self.log(msg)

    def log(self, msg):
        self.emit(QtCore.SIGNAL("log(QString)"), msg)
        datetime_format = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.get_ui().detail_log.insertPlainText(datetime_format +": "+msg)
        self.get_ui().detail_log.insertPlainText(os.linesep)

    def on_async_start(self):
        print 'ASYNC: start'
        self._enable_buttons(False)
        self.get_ui().progress_bar.setValue(-1)
        self.get_ui().progress_bar.setMaximum(0)

    def on_async_stop(self):
        print 'ASYNC: stop'
        self._enable_buttons(True)
        self.get_ui().progress_bar.setValue(0)
        self.get_ui().progress_bar.setMaximum(100)

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
        self.connect(self.get_ui().action_quit, QtCore.SIGNAL("triggered()"), self.quit )

        self.load_ui()

    def on_vagrant_status(self, msg):
        self.set_status(msg)

    def load_ui(self):
        self.vagrant_widget = VagrantWidget(self)
        self.get_ui().vagrant_widget_layout.addWidget(self.vagrant_widget)
        self.vagrant_widget.show()
        self.connect(self.vagrant_widget, QtCore.SIGNAL("vagrant_status(QString)"), self.on_vagrant_status)
        self.vagrant_widget.set_root(self.read_settings()['vagrant_root'])

    def set_status(self, msg, length=5000):
        self.get_ui().statusbar.showMessage(msg, length)

    def _get_settings(self):
        return QtCore.QSettings('vagrant-manager')

    def write_settings(self):
        print 'Write settings'
        settings = self._get_settings()
        settings.setValue("vagrant_root", self.vagrant_widget.get_root());

    def read_settings(self):
        print 'Read settings'
        conf = {}
        settings = self._get_settings()
        conf['vagrant_root'] = settings.value('vagrant_root').toString()
        return conf

    def quit(self):
        print 'QUIT'
        self.write_settings()
        self.close()
