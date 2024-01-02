import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QRadioButton

from models.filter import PointType


class FilterDesigner:
    def __init__(self, window) -> None:
        self.window = window
        self.designer_graph = self.window.zeroes_poles_edit_graph
        self.zeros = []
        self.poles = []
        self.next_point_type = PointType.ZERO
        self._setup_zeroes_poles_graph()
        self._initialize_signals_slots()

    def _initialize_signals_slots(self) -> None:
        self.window.zeroes_poles_edit_graph.scene().sigMouseClicked.connect(
            self._on_designer_clicked
        )
        self.window.zeros_rb.clicked.connect(self._on_radio_button_clicked)
        self.window.poles_rb.clicked.connect(self._on_radio_button_clicked)

    def _on_radio_button_clicked(self):
        if self.window.zeros_rb.isChecked():
            self.next_point_type = PointType.ZERO
        if self.window.poles_rb.isChecked():
            self.next_point_type = PointType.POLE

    def _add_point_to_designer(self, pos, type: PointType) -> None:
        if self._is_inside_unit_circle(pos):
            x, y = pos.x(), pos.y()
            if type == PointType.ZERO:
                self.zeros.append((x, y))
            if type == PointType.POLE:
                self.poles.append((x, y))
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
