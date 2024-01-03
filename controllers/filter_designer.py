import numpy as np
import pyqtgraph as pg
from scipy import signal

from models.filter import PointType, Filter


class FilterDesigner:
    def __init__(self, window) -> None:
        self.window = window
        self.designer_graph = self.window.zeroes_poles_edit_graph
        self.zeros = []
        self.poles = []
        self.next_point_type = PointType.ZERO
        self._setup_zeroes_poles_graph()
        self._initialize_signals_slots()

        self.filter = Filter(zeros=self.zeros, poles=self.poles)

    def _initialize_signals_slots(self) -> None:
        self.window.zeroes_poles_edit_graph.scene().sigMouseClicked.connect(
            self._on_designer_clicked
        )
        self.window.zeros_rb.clicked.connect(self._on_radio_button_clicked)
        self.window.poles_rb.clicked.connect(self._on_radio_button_clicked)
        self.window.clear_points_btn.clicked.connect(self._plot_responses)

    def _on_radio_button_clicked(self):
        if self.window.zeros_rb.isChecked():
            self.next_point_type = PointType.ZERO
        if self.window.poles_rb.isChecked():
            self.next_point_type = PointType.POLE

    def compute_magnitude_phase_response(self, zeros, poles, frequencies):
        print(zeros, poles)
        zeros = [complex(x, y) for x, y in zeros]
        poles = [complex(x, y) for x, y in poles]
        print(zeros, poles)
        system = signal.TransferFunction(zeros, poles)

        # Evaluate transfer function on the unit circle
        omega, h = signal.freqresp(system)

        # Calculate magnitude and phase responses
        magnitude_response = np.abs(h)
        phase_response = np.angle(h, deg=True)  # Convert phase to degrees

        return omega, magnitude_response, phase_response
    
    def frequencyResponse(self,zeros, poles, gain):
        zeros = [complex(x, y) for x, y in zeros]
        poles = [complex(x, y) for x, y in poles]
        gain = 1
        w, h = signal.freqz_zpk(zeros, poles, gain)
        magnitude = 20 * np.log10(np.abs(h))
        angels = np.unwrap(np.angle(h))
        return w/max(w), angels, magnitude
    
    def _plot_responses(self):
        print("plotting")
        frequencies = np.linspace(0, 3, 1000)  # Adjust frequency range as needed
        (
            frequencies,
            magnitude_response,
            phase_response,
        ) = self.frequencyResponse(self.zeros, self.poles, 1.5)
        # TODO: Refactor to state
        self.window.mag_response_garph.plot(
            frequencies, magnitude_response, pen="b"
        )
        self.window.phase_response_garph.plot(frequencies, phase_response, pen="r")

        self.window.mag_response_garph.showGrid(x=True, y=True)
        self.window.phase_response_garph.showGrid(x=True, y=True)

    def _add_point_to_designer(self, pos, type: PointType) -> None:
        if self._is_inside_unit_circle(pos):
            x, y = pos.x(), pos.y()
            if type == PointType.ZERO:
                self.zeros.append((x, y))
                self.filter.set_zeros([complex(x, y)])
            if type == PointType.POLE:
                self.poles.append((x, y))
                self.filter.set_poles([complex(x, y)])
            self.designer_graph.plot(
                [x],
                [y],
                pen=None,
                symbol="o" if type == PointType.ZERO else "x",
                symbolPen="r",
                symbolBrush=0.2,
            )

    def _on_designer_clicked(self, event):
        pos = self.designer_graph.plotItem.vb.mapToView(event.pos())

        self._add_point_to_designer(pos, self.next_point_type)

    def _is_inside_unit_circle(self, pos) -> bool:
        # Check if the distance from the origin is less than or equal to 1
        return np.sqrt(pos.x() ** 2 + pos.y() ** 2) <= 1

    def _setup_zeroes_poles_graph(self) -> None:
        self.designer_graph.setYRange(-1, 1)
        self.designer_graph.setXRange(-1, 1)

        vertical_line = pg.InfiniteLine(pos=0, angle=90, movable=False)
        horizontal_line = pg.InfiniteLine(pos=0, angle=0, movable=False)
        self.designer_graph.addItem(vertical_line)
        self.designer_graph.addItem(horizontal_line)
        self._draw_unit_circle(self.designer_graph)

    def _draw_unit_circle(self, graph) -> None:
        # 100 points around the circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        graph.plot(x, y, pen="r")
