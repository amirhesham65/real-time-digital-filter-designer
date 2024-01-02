import numpy as np
import pyqtgraph as pg


class FilterDesigner:
    def __init__(self, window) -> None:
        self.window = window

        self._setup_zeroes_poles_graph()

    def _setup_zeroes_poles_graph(self):
        graph = self.window.zeroes_poles_edit_graph
        graph.setYRange(-1, 1)
        graph.setXRange(-1, 1)

        vertical_line = pg.InfiniteLine(pos=0, angle=90, movable=False)
        horizontal_line = pg.InfiniteLine(pos=0, angle=0, movable=False)
        graph.addItem(vertical_line)
        graph.addItem(horizontal_line)
        self._draw_unit_circle(graph)

    def _draw_unit_circle(self, graph) -> None:
        # 100 points around the circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        graph.plot(x, y, pen="r")
