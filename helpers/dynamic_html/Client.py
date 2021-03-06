import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QApplication


class Client(QWebPage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self.on_page_load)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def on_page_load(self):
        self.html = self.mainFrame().toHtml()
