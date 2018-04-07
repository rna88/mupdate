import sys
import os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog, QMessageBox
from PyQt4.QtCore import QThread, SIGNAL

import ftplib
import ssl
ftps = ftplib.FTP_TLS()
import time

fileType = ".bsp"   # File extension to download.
localDir =  ''   # Directory to place downloaded files.
blockSize = 8192    # bytes
qtCreatorFile = "mupclient.ui"  # UI schema

# Original stylesheet from http://tech-artists.org/t/release-qt-dark-orange-stylesheet/2287
# http://www.yasinuludag.com/darkorange.stylesheet
styleSheet="""
QToolTip
{
     border: 1px solid black;
     background-color: #ffa02f;
     padding: 1px;
     border-radius: 3px;
     opacity: 100;
}

QWidget
{
    color: #b1b1b1;
    background-color: #323232;
}

QWidget:item:hover
{
    /*background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);*/
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
    color: #000000;
}

QWidget:item:selected
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 1px solid #ffaa00;
}

QMenuBar::item:pressed
{
    background: #444;
    border: 1px solid #000;
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:1 #212121,
        stop:0.4 #343434/*,
        stop:0.2 #343434,
        stop:0.1 #ffaa00*/
    );
    margin-bottom:-1px;
    padding-bottom:1px;
}

QMenu
{
    border: 1px solid #000;
}

QMenu::item
{
    padding: 2px 20px 2px 20px;
}

QMenu::item:selected
{
    color: #000000;
}

QWidget:disabled
{
    color: #404040;
    background-color: #323232;
}

QAbstractItemView
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);
}

QWidget:focus
{
    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/
}

QLineEdit
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
    padding: 1px;
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QPushButton
{
    color: #b1b1b1;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 6;
    padding: 3px;
    font-size: 12px;
    padding-left: 5px;
    padding-right: 5px;
}

QPushButton:pressed
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}

QComboBox
{
    selection-background-color: #ffaa00;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QComboBox:hover,QPushButton:hover
{
    border: 0px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}


QComboBox:on
{
    padding-top: 3px;
    padding-left: 4px;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
    selection-background-color: #ffaa00;
}

QComboBox QAbstractItemView
{
    border: 2px solid darkgray;
    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QComboBox::drop-down
{
     subcontrol-origin: padding;
     subcontrol-position: top right;
     width: 15px;

     border-left-width: 0px;
     border-left-color: darkgray;
     border-left-style: solid; /* just a single line */
     border-top-right-radius: 3px; /* same radius as the QComboBox */
     border-bottom-right-radius: 9px;
 }

QComboBox::down-arrow
{
     image: url(:/down_arrow.png);
}

QGroupBox:focus
{
border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QTextEdit:focus
{
    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
}

QScrollBar:horizontal {
     border: 1px solid #222222;
     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
     height: 7px;
     margin: 0px 16px 0 16px;
}

QScrollBar::handle:horizontal
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
      subcontrol-position: right;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);
      width: 14px;
     subcontrol-position: left;
     subcontrol-origin: margin;
}

QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
      background: none;
}

QScrollBar:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
      width: 7px;
      margin: 16px 0 16px 0;
      border: 1px solid #222222;
}

QScrollBar::handle:vertical
{
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);
      min-height: 20px;
      border-radius: 2px;
}

QScrollBar::add-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);
      height: 14px;
      subcontrol-position: bottom;
      subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical
{
      border: 1px solid #1b1b19;
      border-radius: 2px;
      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);
      height: 14px;
      subcontrol-position: top;
      subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
      border: 1px solid black;
      width: 1px;
      height: 1px;
      background: white;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
      background: none;
}

QTextEdit
{
    background-color: #242424;
}

QPlainTextEdit
{
    background-color: #242424;
}

QHeaderView::section
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
}

QCheckBox:disabled
{
color: #414141;
}

QDockWidget::title
{
    text-align: center;
    spacing: 3px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button, QDockWidget::float-button
{
    text-align: center;
    spacing: 1px; /* spacing between items in the tool bar */
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover
{
    background: #242424;
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed
{
    padding: 1px -1px -1px 1px;
}

QMainWindow::separator
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    border: 1px solid #4c4c4c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QMainWindow::separator:hover
{

    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QToolBar::handle
{
     spacing: 3px; /* spacing between items in the tool bar */
     background: url(:/images/handle.png);
}

QMenu::separator
{
    height: 2px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}

QProgressBar
{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk
{
    /*background-color: #d7801a;*/
    /*background-color: #c95000;*/
    /*background-color: #990000;*/
    /*background-color: #911515;*/
    /*background-color: #7c1313;*/
    /*background-color: #4f4f4f;*/
    background-color: #555555;
    width: 2.15px;
    /*margin: 0.5px;*/
    margin: 0.0px;
}

QTabBar::tab {
    color: #b1b1b1;
    border: 1px solid #444;
    border-bottom-style: none;
    background-color: #323232;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 2px;
    margin-right: -1px;
}

QTabWidget::pane {
    border: 1px solid #444;
    top: 1px;
}

QTabBar::tab:last
{
    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
    border-top-right-radius: 3px;
}

QTabBar::tab:first:!selected
{
 margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */


    border-top-left-radius: 3px;
}

QTabBar::tab:!selected
{
    color: #b1b1b1;
    border-bottom-style: solid;
    margin-top: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);
}

QTabBar::tab:selected
{
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    margin-bottom: 0px;
}

QTabBar::tab:!selected:hover
{
    /*border-top: 2px solid #ffaa00;
    padding-bottom: 3px;*/
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);
}

QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    border-radius: 6px;
}

QRadioButton::indicator:checked
{
    background-color: qradialgradient(
        cx: 0.5, cy: 0.5,
        fx: 0.5, fy: 0.5,
        radius: 1.0,
        stop: 0.25 #ffaa00,
        stop: 0.3 #323232
    );
}

QCheckBox::indicator{
    color: #b1b1b1;
    background-color: #323232;
    border: 1px solid #b1b1b1;
    width: 9px;
    height: 9px;
}

QRadioButton::indicator
{
    border-radius: 6px;
}

QRadioButton::indicator:hover, QCheckBox::indicator:hover
{
    border: 1px solid #ffaa00;
}

QCheckBox::indicator:checked
{
    image:url(:/images/checkbox.png);
}

QCheckBox::indicator:disabled, QRadioButton::indicator:disabled
{
    border: 1px solid #444;
}
"""

 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class retrieveThread(QThread):

    def __init__(self, dpath): # all variables found in main thread need to be passed in here.
        QThread.__init__(self)
        self.dpath = dpath # Assign the passed in variables to the thread, so the thread functions can use them.

    def __del(self):
        self.wait()

    def run(self):
        print ("hey " + self.dpath)
        #self.list_serverListing.clear()
        self.emit(SIGNAL("clearText()")) # Add arguments to clearText after SIGNAL param
        #localDir = str(self.line_downloadPath.text())
        localDir = self.dpath
        if ( (not localDir) or (not os.path.isdir(localDir)) ):
            self.emit(SIGNAL("invalidPath()")) # Add arguments to clearText after SIGNAL param
        else:
            print ("continue")
#        #    self.label_fileProgress.setText("Retrieving...")
#            try:
#                ftps.connect('0.0.0.0',47274)            
#                ftps.login('user','12345')
#                ftps.prot_p()
#
#                localFiles= os.listdir(localDir)
#                remoteFiles=ftps.nlst()
#                newFiles = set(remoteFiles) - set(localFiles)
#                filteredFiles = [] 
#                ftps.sendcmd("TYPE i")
#                for f in newFiles:
#                    if f.endswith(fileType):
#                        filteredFiles.append(f)
#        #                self.list_serverListing.addItem(self.formatSize(ftps.size(f)) + " " + f) # Needs to emit signal
#            except (ftplib.all_errors) as e:
#                self.emit(SIGNAL("invalidPath()")) # Add arguments to clearText after SIGNAL param
#        #        QMessageBox.information(self, "FTP error", "[" + str(e.errno) + "]" + " " + str(e.strerror))
#        #        self.label_fileProgress.setText("Could not retrieve listing")  # signal
#                msg = "FTP error", "[" + str(e.errno) + "]" + " " + str(e.strerror)
#                self.emit(SIGNAL("setProgressText(PyQt_PyObject)", msg)

        #    self.label_fileProgress.setText("Done") # signal
        #    self.emit(SIGNAL("setProgressText(text)", "Done")
        #self.emit(SIGNAL("setProgressBar(value)"), 0)
        #self.progressBar.setValue(0) # signal


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.button_change.clicked.connect(self.changePath)
        #self.button_retrieve.clicked.connect(self.retrieveList)
        self.button_retrieve.clicked.connect(self.retrieveListThread)
        self.button_download.clicked.connect(self.downloadList)
        self.button_cancel.clicked.connect(self.cancelDownload)
        self.list_serverListing.clicked.connect(self.updateSelected)
        self.progressBar.setValue(0)

        
        # Open config file during startup to read contents.
        try:
            with open('mupdate.cfg', 'r') as cfg:
                localDir = cfg.readline()
                self.line_downloadPath.setText(localDir)
                #self.line_downloadPath.setText(cfg.readline())
                cfg.close()
        except (FileNotFoundError) as e:
            pass
        except (IOError) as e:
            QMessageBox.information(self, "IO error", str(e.errno) + " " + str(e.strerror))

    def retrieveListThread(self):
        self.rThread = retrieveThread(self.line_downloadPath.text()) # pass in variables needed to thread here.
        self.connect(self.rThread, SIGNAL("clearText()"), self.clearText) # feed argument self 
        self.connect(self.rThread, SIGNAL("invalidPath()"), self.invalidPath)
        self.connect(self.rThread, SIGNAL("setProgressText(PyQt_PyObject)"), self.setProgressText)
        #self.connect(self.rThread, SIGNAL("setProgressBar(PyQT_PyObject)"), self.setProgressBar)

        self.rThread.start()


    def clearText(self):
        self.list_serverListing.clear()
        print ("cleared")

    def invalidPath(self):
        QMessageBox.information(self, "Mupdate error", "Specify a valid download path")

    def setProgressText(self, text):
        self.label_fileProgress.setText(text)

    def setProgressBar(self, value):
        self.progressBar.setValue(value)

    # Abbreviate the filesize in bytes to kB/MB/GB etc.
    def formatSize(self,size):
        if size < 1000:
            return (str(size)[:3] + "B")
        elif size < 1000000:
            return (str(size / 1000)[:3] + "K")
        elif size < 1000000000:
            return (str(size / 1000000)[:3] + "M")
        elif size < 1000000000000:
            return (str(size / 1000000000)[:3] + "G")
 
    def changePath(self):
        localDir = QFileDialog.getExistingDirectory()
        self.line_downloadPath.setText(localDir)
        try:
            with open('mupdate.cfg', 'w') as cfg:
                cfg.write(str(self.line_downloadPath.text()))
                cfg.close()
        except (IOError) as e:
            QMessageBox.information(self, "IO error", str(e.errno) + " " + str(e.strerror))

    def retrieveList(self):
        self.list_serverListing.clear()
        localDir = str(self.line_downloadPath.text())
        if ( (not localDir) or (not os.path.isdir(localDir)) ):
            QMessageBox.information(self, "Mupdate error", "Specify a valid download path")
        else:
            self.label_fileProgress.setText("Retrieving...")
            try:
                ftps.connect('0.0.0.0',47274)            
                ftps.login('user','12345')
                ftps.prot_p()

                localFiles= os.listdir(localDir)
                remoteFiles=ftps.nlst()
                newFiles = set(remoteFiles) - set(localFiles)
                filteredFiles = [] 
                ftps.sendcmd("TYPE i")
                for f in newFiles:
                    if f.endswith(fileType):
                        filteredFiles.append(f)
                        self.list_serverListing.addItem(self.formatSize(ftps.size(f)) + " " + f) # Needs to emit signal
            except (ftplib.all_errors) as e:
                QMessageBox.information(self, "FTP error", "[" + str(e.errno) + "]" + " " + str(e.strerror))
                self.label_fileProgress.setText("Could not retrieve listing")  # signal
            self.label_fileProgress.setText("Done") # signal
        self.progressBar.setValue(0) # signal

    def updateSelected(self):
        self.label_fileProgress.setText(str(len(self.list_serverListing.selectedItems())) + " file(s) selected")

    # Callback used to update the relevant UI elements as a file is being downloaded.
    def updateProgress(self, i, fname, fsize, block, downloadedFile, totalFileCount):
        downloadedFile.write(block)
        curSize = os.stat(fname).st_size
        self.label_fileProgress.setText("(" + str(i) + "/" + totalFileCount + ")" + " " + fname + " " + str(curSize) + "/" + str(fsize) + " B")
        self.progressBar.setValue(curSize / fsize * 100)
        time.sleep(0.01) #   <----------------------------------------remove this if testing on network
        

    def downloadList(self):
        i = 0
        totalFileCount = str(len(self.list_serverListing.selectedItems()))
        localDir = str(self.line_downloadPath.text())
        currentDir = os.getcwd()
        os.chdir(localDir)
        for files in self.list_serverListing.selectedItems():
            try:
                ftps.sendcmd("TYPE i") # Turn on binary mode, needed for file size retrieval.
                i = i + 1
                fname = str(files.text())[5:] # Strip off first 5 characters as they show the file size.
                fsize = ftps.size(fname)
                downloadedFile = open(fname, 'wb')
                ftps.retrbinary('RETR %s' % fname, lambda block: self.updateProgress(i, fname, fsize, block, downloadedFile, totalFileCount), blockSize)
            except Exception as e:
                QMessageBox.information(self, "Error " , "Problem downloading the file: " + str(fname) + "\n\n" + str(e) )
                try:
                    os.remove(fname) # Remove any partly downloaded files.
                except (FileNotFoundError):
                    pass
                continue
   
        os.chdir(currentDir)
        self.label_fileProgress.setText("(" + str(i) + "/" + totalFileCount + ")" + " Done")
        #self.retrieveList()

    def cancelDownload(self):
        #ftps.abort()
        #print ("canel")
        pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    #app.setStyle('GTK+')
    app.setStyleSheet(styleSheet)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
