from PyQt6.QtCore import QTimer
from helper.get_signal_from_file import get_signal_from_file
from math import floor
from models.filter import Filter
from models.signal import Signal

class SignalViewer:
    def __init__(self, window , filter = None):
        self.signal = None
        self.timer = QTimer()
        self.window = window
        self._initialize_signals_slots()
        self.x_data = []
        self.y_data = []
        self.largest_x_data = []
        self.largest_y_data = []
        self.x_filtered_data = []
        self.y_filtered_data = []
        self.largest_x_filtered_data = []
        self.largest_y_filtered_data = []
        self.data_index = 0
        self.is_plotting = False
        self.speed = 1
        self.filter = filter
        self.filtered_signal = None

    def _initialize_signals_slots(self):
        self.window.pushButton_6.clicked.connect(self.import_signal)
        self.timer.timeout.connect(self.update_plot)

    def import_signal(self):
        self.signal = get_signal_from_file(self.window)
        self.filtered_signal = Signal(x_vec=self.signal.x_vec, y_vec=self.filter.apply_filter(self.signal.y_vec))
        
        self.render(self.window.signal_input_graph,self.window.filter_output_graph)

    def render(self,channel1,channel2):
        self.timer.start(floor(8 / self.speed))  # Update every 8/speed ms
        self.x_data.extend(self.signal.x_vec)
        self.y_data.extend(self.signal.y_vec)
        self.largest_x_data = self.signal.x_vec
        self.x_filtered_data.extend(self.filtered_signal.x_vec)
        self.y_filtered_data.extend(self.filtered_signal.y_vec)
        self.largest_x_filtered_data = self.filtered_signal.x_vec
        channel1.plot(self.x_data, self.y_data)
        channel2.plot(self.x_filtered_data, self.y_filtered_data)
        self.data_index = 0
        self.is_plotting = True


    def update_plot(self):
        if self.is_plotting:
            if self.data_index < len(self.largest_x_data):
                x_data = self.largest_x_data[: self.data_index + 1]
                self.x_filtered_data = self.largest_x_filtered_data[: self.data_index + 1]
                self.window.signal_input_graph.setXRange(x_data[-1] - 1, x_data[-1])
                self.window.filter_output_graph.setXRange(self.x_filtered_data[-1] - 1, self.x_filtered_data[-1])
                self.data_index += 1
            else:
                self.is_plotting = False
                self.timer.stop()
