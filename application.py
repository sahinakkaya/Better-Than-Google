from PySide2.QtCore import QUrl
from PySide2.QtWidgets import QApplication
from PySide2.QtWebEngineWidgets import QWebEngineView
import prepare_main_page


class MyBrowser(QWebEngineView):
    def __init__(self):
        super(MyBrowser, self).__init__()
        self.setWindowTitle("Loading")
        self.titleChanged.connect(self.adjustTitle)

    def load(self, url):
        self.setUrl(QUrl.fromLocalFile(url))

    def adjustTitle(self):
        self.setWindowTitle(self.title())


if __name__ == '__main__':
    import sys, os
    prepare_main_page.main()
    curr_path = os.getcwd()
    app = QApplication(sys.argv)
    x_coord = 600
    y_coord = 150
    width = 506
    height = 900
    b = MyBrowser()
    b.setGeometry(x_coord, y_coord, width, height)
    b.load(os.sep.join([curr_path, "whatsapp_ui", "index.html"]))

    b.show()
    sys.exit(app.exec_())
