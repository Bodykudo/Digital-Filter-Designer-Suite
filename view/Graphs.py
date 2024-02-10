import pyqtgraph as pg


class PhaseGraph(pg.PlotWidget):
    def __init__(self, parent=None, dark_mode=False) -> None:
        super().__init__(parent=parent)
        if not dark_mode:
            self.setBackground("w")
        self.setLabel("left", "Phase")
        self.setLabel("bottom", "Frequency (Hz)")
        self.showGrid(x=True, y=True)
        self.setMouseEnabled(x=False, y=False)

    def updatePlot(self, x, y):
        self.clear()
        self.plot(x, y, pen=pg.mkPen(color="#BF4040", width=2))


class MagnitudeGraph(pg.PlotWidget):
    def __init__(self, parent=None, dark_mode=False) -> None:
        super().__init__(parent=parent)
        if not dark_mode:
            self.setBackground("w")
        self.setLabel("left", "Magnitude")
        self.setLabel("bottom", "Frequency (Hz)")
        self.showGrid(x=True, y=True)
        self.setMouseEnabled(x=False, y=False)
        self.dark_mode = dark_mode

    def updatePlot(self, x, y):
        self.clear()
        self.plot(x, y, pen=pg.mkPen(color="#BF4040", width=2))
