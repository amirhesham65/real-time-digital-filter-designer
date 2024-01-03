from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
import pyqtgraph as pg
from models.signal import Signal
from managers.signal_loader import ISignalLoader, TextSignalLoader, CSVSignalLoader, ExcelXSignalLoader, ExcelSignalLoader
from helper.get_signal_from_file import get_signal_from_file
from math import floor

class SignalViewer:
    def __init__(self,window):
        self.signal = None
        self.timer = QTimer()
        self.window = window
        self._initialize_signals_slots()
        self.x_data = []
        self.y_data = []
        self.largest_x_data = []
        self.largest_y_data = []
        self.data_index = 0
        self.y_min = None
        self.y_max = None
        self.x_vec = []
        self.y_vec = []
        self.is_plotting = False
        self.speed = 1

    def _initialize_signals_slots(self):
        self.window.pushButton_6.clicked.connect(self.import_signal)
        self.timer.timeout.connect(self.update_plot)
    
    def import_signal(self):
        self.signal = get_signal_from_file(self.window)
        self.render_signal_to_channel(signal=self.signal)
    
    def render_signal_to_channel(self, signal):
        self.timer.start(floor(8 / self.speed))  # Update every 8/speed ms
        self.x_data.extend(signal.x_vec)
        self.y_data.extend(signal.y_vec)
        self.largest_x_data = signal.x_vec
        self.window.signal_input_graph.plot(self.x_data, self.y_data)
        self.data_index = 0
        self.is_plotting = True
        
        
    def update_plot(self):
        if self.is_plotting:
            if self.data_index < len(self.largest_x_data):
                x_data = self.largest_x_data[: self.data_index + 1]
                # if x_data[-1] < 1:
                #     self.window.signal_input_graph.setXRange(0, 1)
                # else:
                self.window.signal_input_graph.setXRange(x_data[-1] - 1, x_data[-1])
                # self.window.signal_input_graph.plot(x_data, self.y_data[: self.data_index + 1])
                self.data_index += 1
            else:
                self.is_plotting = False
                self.timer.stop()
        