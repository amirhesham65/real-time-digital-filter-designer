import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication


uiclass, baseclass = pg.Qt.loadUiType("views/mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()

        # Window and UI configurations
        self.setupUi(self)
        self.setWindowTitle("Real-time Digital Filter Designer")
        self.show()


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
