import os
import re
import sys
import urllib.request
from os import path

import pafy
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox
from PyQt5.uic import loadUiType

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):

    def __init__(self):
        super(MainApp, self).__init__()
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

    def downloadRequirementsCheck(self):
        # TODO check link if standard check if it have a file not html get the file name or ask the user to provide
        # i think we should use Requests lib for th e check
        # TODO ask for location if the default not set then set
        # check for dubs
        pass

    def handleBrowse(self):
        select = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.plainTextEdit_2.setPlainText(select)

    def setDefaultDownloadLocation(self):
        # TODO should be set as the last used or downloads
        pass

    def handleProgressBar(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
        QApplication.processEvents()

    def handleDownload(self):
        url = self.getUrl()
        path = self.getPath()

        try:
            if self.checkIfYouTube(url):
                if "playlist" in url:
                    self.playlistDownload(url)
                self.youtubeDownload(url,path)
            else:
                self.standardDownload(url, path)
        except Exception:
            QMessageBox.information(self, "ERROR", "Sorry, Check Your Internet Connection")
        else :
            QMessageBox.information(self, "Downloading", "Please WAIT")

    def standardDownload(self, url, standardPath):
        urllib.request.urlretrieve(url, standardPath, self.handleProgressBar)

    def youtubeDownload(self, url,path):
        v = pafy.new(url)
        for s in v.allstreams:
            size = s.get_filesize()
            data = "{}{}{}{}".format(s.mediatype, s.extension, s.quality, size)
            self.comboBox.addItem(data)
        quality = self.comboBox.currentIndex()
        v.allstreams[quality].download(filepath=path)

        # TODO  video name, ETA, Received Bytes, Speed

    # def playlistDownload(self, url):
    #
    #     os.chdir(path)
    #
    #     if os.path.exists(str(playlist["title"])) :
    #         os.chdir(str(playlist["title"]))
    #     else:
    #         os.mkdir(str(playlist["title"]))
    #         os.chdir(str(playlist["title"]))

    def videoDataRetrieve(self, url):
        pass

    # def playlistDataRetrieve(self, url):
    #     playlist = pafy.get_playlist(url)

    def pauseContinue(self):
        pass

    def getUrl(self):
        # TODO get url from clipboard
        if self.plainTextEdit.toPlainText() == "":
            self.plainTextEdit.setPlainText("TEST")
            return "http://www.tutorialspoint.com/python/python_tutorial.pdf"
        elif self.plainTextEdit.toPlainText() == "y":
            self.plainTextEdit.setPlainText("YOUTUBE TEST")
            return "https://youtube.com/watch?v=XJGiS83eQLk"
        else:
            return self.plainTextEdit.toPlainText()

    def getPath(self):
        if self.plainTextEdit_2.toPlainText() == "":
            self.plainTextEdit_2.setPlainText("TEST")
            downloads = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
            return downloads + "\\" + "test.pdf"
        else:
            return self.plainTextEdit_2.toPlainText()

    # TODO takes a url ==> return file name
    def getFileName(self):
        pass

    #     remotefile = urlopen(url)
    #     blah = remotefile.info()['Content-Disposition']
    #     value, params = cgi.parse_header(blah)
    #     filename = params["filename"]
    #     urlretrieve(url, filename)
    #     return filename

    def dublicatesCheck(self):
        # check if the given dir exists and if the file already exists if it does check if it is complete or the same
        # as the new one may offer multiple options to deal
        try:
            pass
        except FileExistsError:
            print("DUB")
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

    def checkIfYouTube(self, url):
        youTube = re.compile(
            "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?")
        if re.match(youTube, url):
            # TODO check if a playlist
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
