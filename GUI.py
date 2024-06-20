import sys
import uic

from PyQt5.QtWidgets import QApplication, QWidget

class Main_window(QWidget):
    def __init__(self):
        super(Main_window, self).__init__()
        uic.loadUi('Screen/result.ui', self)
        self.save.clicked.connect(self.Save)
        self.download.clicked.connect(self.Download)
        self.compilate.clicked.connect(self.Compl)

    def Save(self):
        pass

    def Download(self):
        pass

    def Compl(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Gui_main_window = Main_window()
    Gui_main_window.show()
    sys.exit(app.exec_())