import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication

from controllers.filter_designer import FilterDesigner
from controllers.filter_viewer import FilterViewer
from controllers.signal_viewer import SignalViewer
from models.filter import Filter

uiclass, baseclass = pg.Qt.loadUiType("views/mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()

        # Window and UI configurations
        self.setupUi(self)
        self.setWindowTitle("Real-time Digital Filter Designer")

        self._initialize_state()
        self._initialize_signals_slots()
        self.filter = None

    def _initialize_state(self) -> None:
        # MVC
        self.filter = Filter()
        self.filter_designer = FilterDesigner(window=self)
        self.filter_viewer = FilterViewer(window=self)

    def _initialize_signals_slots(self) -> None:
        ...


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
