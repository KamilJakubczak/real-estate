from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtCore import pyqtSignal, QUrl


class WebPage(QWebEnginePage):
    htmlReady = pyqtSignal(str, str)

    def __init__(self, verbose=False):
        super().__init__()
        self._verbose = verbose
        self.loadFinished.connect(self.handleLoadFinished)

    def process(self, urls):
        self._urls = iter(urls)
        self.fetchNext()

    def fetchNext(self):
        try:
            url = next(self._urls)
            print(url)
        except StopIteration:
            return False
        else:
            self.load(QUrl(url))
        return True

    def processCurrentPage(self, html):
        self.htmlReady.emit(html, self.url().toString())
        if not self.fetchNext():
            QApplication.instance().quit()

    def handleLoadFinished(self):
        self.toHtml(self.processCurrentPage)

    def javaScriptConsoleMessage(self, *args, **kwargs):
        if self._verbose:
            super().javaScriptConsoleMessage(*args, **kwargs)
