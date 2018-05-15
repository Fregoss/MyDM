import os
import re
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from os import path
import urllib.request
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("DM")
        self.setWindowIcon(QIcon("Images\if_dashboard_basic_blue_69481.ico"))
        self.handleButtons()

    def handleUi(self):
        pass

    def handleButtons(self):
        self.pushButton.clicked.connect(self.handleDownload)
        self.actionExit.triggered.connect(self.handleDownload)
        self.pushButton_3.clicked.connect(self.endMyLife)
        self.actionExit_2.triggered.connect(self.endMyLife)
        self.pushButton_2.clicked.connect(self.handleBrowse)

    def handleBrowse(self):
        select = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="ALL Files (*.*)")
        self.plainTextEdit_2.setPlainText(select[0])

    def setDefaultDownloadLocation(self):
        pass

    def handleProgressBar(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
        QApplication.processEvents()

    def handleDownload(self):
        urllib.request.urlretrieve(self.getUrl(), self.getPath(), self.handleProgressBar)

    def pauseContinue(self):
        pass

    def getUrl(self):
        if self.plainTextEdit.toPlainText() == "":
            self.plainTextEdit.setPlainText("TEST")
            return "http://www.tutorialspoint.com/python/python_tutorial.pdf"
        else:
            return self.plainTextEdit.toPlainText()

    def getPath(self):
        if self.plainTextEdit_2.toPlainText() == "":
            self.plainTextEdit_2.setPlainText("TEST")
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            return desktop + "\\" + "test.pdf"
        else:
            return self.plainTextEdit_2.toPlainText()

    def getFileName(self, url):
        remotefile = urlopen(url)
        blah = remotefile.info()['Content-Disposition']
        value, params = cgi.parse_header(blah)
        filename = params["filename"]
        urlretrieve(url, filename)
        return filename

    def dublicatesCheck(self):
        # check if the givin dir exists and if the file already exists if it does check if it is complete or the same
        #  as the new one may offer multible opthions to deal
        pass

    # gather errors and notify
    def notifier(self):
        pass

    def downloadCompleted(self):
        self.message()
        self.startOver()
        pass

    def message(self):
        QMessageBox.information(self, "Completed", "Done")

    def endMyLife(self):
        QCoreApplication.quit()

    def startOver(self):
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit_2.setPlainText("")
        self.progressBar.setValue(0)

    def checkIfYouTube(url):
        youTube = re.compile(
            "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")
        if re.match(youTube, url):
            return True
        else:
            return False


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
