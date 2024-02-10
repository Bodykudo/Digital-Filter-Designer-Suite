from PyQt6.QtCore import Qt, QPointF
import pyqtgraph as pg

import numpy as np

from view.TargetItms import Pole, Zero


class Designer(pg.PlotWidget):
    def __init__(
        self,
        filter,
        phaseGraph,
        magnitudeGraph,
        correctedPhaseGraph,
        allPassPhaseGraph,
        dark_mode=False,
    ):
        super().__init__()
        if not dark_mode:
            self.setBackground("w")
        self.showGrid(x=True, y=True)
        self.setMouseEnabled(x=False, y=False)
        self.initGraph()
        self.currentItem = "pole"
        self.isPair = False
        self.filter = filter
        self.phaseGraph = phaseGraph
        self.magnitudeGraph = magnitudeGraph
        self.correctedPhaseGraph = correctedPhaseGraph
        self.allPassPhaseGraph = allPassPhaseGraph
        self.dark_mode = dark_mode

    def initGraph(self):
        a = np.cos(np.linspace(0, 2 * np.pi, 200))
        b = np.sin(np.linspace(0, 2 * np.pi, 200))
        self.plot(a, b, pen=pg.mkPen(color="#60a5fa", width=2))

    def setItem(self, item):
        self.currentItem = item

    def togglePair(self):
        self.isPair = not self.isPair

    def mousePressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            pos = event.pos()
            posF = QPointF(pos)
            x = self.plotItem.vb.mapSceneToView(posF).x()
            y = self.plotItem.vb.mapSceneToView(posF).y()

            if self.currentItem == "pole":
                pole = Pole(
                    self,
                    x=x,
                    y=y,
                    filter=self.filter,
                    phaseGraph=self.phaseGraph,
                    magnitudeGraph=self.magnitudeGraph,
                    correctedPhaseGraph=self.correctedPhaseGraph,
                    allPassPhaseGraph=self.allPassPhaseGraph,
                    dark_mode=self.dark_mode,
                )
                self.filter.add_pole(pole)
                if self.isPair:
                    pole2 = Pole(
                        self,
                        x=x,
                        y=-y,
                        filter=self.filter,
                        phaseGraph=self.phaseGraph,
                        magnitudeGraph=self.magnitudeGraph,
                        correctedPhaseGraph=self.correctedPhaseGraph,
                        allPassPhaseGraph=self.allPassPhaseGraph,
                        is_linked=True,
                        linked_item=pole,
                        dark_mode=self.dark_mode,
                    )
                    self.filter.add_pole(pole2)
            elif self.currentItem == "zero":
                zero = Zero(
                    self,
                    x=x,
                    y=y,
                    filter=self.filter,
                    phaseGraph=self.phaseGraph,
                    magnitudeGraph=self.magnitudeGraph,
                    correctedPhaseGraph=self.correctedPhaseGraph,
                    allPassPhaseGraph=self.allPassPhaseGraph,
                    dark_mode=self.dark_mode,
                )
                self.filter.add_zero(zero)
                if self.isPair:
                    zero2 = Zero(
                        self,
                        x=x,
                        y=-y + 0.4,
                        filter=self.filter,
                        phaseGraph=self.phaseGraph,
                        magnitudeGraph=self.magnitudeGraph,
                        correctedPhaseGraph=self.correctedPhaseGraph,
                        allPassPhaseGraph=self.allPassPhaseGraph,
                        is_linked=True,
                        linked_item=zero,
                        dark_mode=self.dark_mode,
                    )
                    self.filter.add_zero(zero2)

            w, magnitude, phase = self.filter.response()
            self.phaseGraph.updatePlot(w, phase)
            self.magnitudeGraph.updatePlot(w, magnitude)

            w_all_pass, _, phase_all_pass = self.filter.all_pass_response()
            self.correctedPhaseGraph.updatePlot(w_all_pass, phase_all_pass)

        else:
            super().mousePressEvent(event)
