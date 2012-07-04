================
vagrant-manager
================

Simple GUI application that manages multiple vagrant instances.

Can be setup to run with cron.

Requirements
============

vagrant-manager is tested with (may work with other versions):

* Python 2.7.3
* PyQt4 4.9.1
* Vagrant 0.3

**Currently vagrant-manager has only been tested in Linux. Windows and Mac support
will be comming in future releases**
    
Features (that currently work):
===============================

* Register a single vagrant root (the folder with a Vagrantfile) and suspend, resume, destroy, get the status, and provision a machine.

Usage
============

Execute this in a shell or double click this file in your file browser:

$ vagrantmanager/vagrantmanager