from typing import Optional
import pyqtgraph as pg


class CustomTargetItem(pg.TargetItem):
    def __init__(
        self,
        designer,
        symbol,
        filter,
        phaseGraph,
        magnitudeGraph,
        correctedPhaseGraph,
        allPassPhaseGraph,
        is_linked=False,
        linked_item: Optional["CustomTargetItem"] = None,
        x=0,
        y=0,
        dark_mode=False,
        *args,
        **kwargs
    ):
        super().__init__(
            symbol=symbol,
            pen=pg.mkPen("yellow" if dark_mode else "black", width=1),
            *args,
            **kwargs
        )
        self.symbol = symbol
        self.is_linked = is_linked
        self.setPos(x, y)
        designer.addItem(self)
        self.filter = filter
        self.phaseGraph = phaseGraph
        self.magnitudeGraph = magnitudeGraph
        self.correctedPhaseGraph = correctedPhaseGraph
        self.allPassPhaseGraph = allPassPhaseGraph

        if is_linked and linked_item:
            self.linked_item = linked_item
            linked_item.is_linked = True
            linked_item.linked_item = self

    def mouseDragEvent(self, event):
        super().mouseDragEvent(event)
        w, magnitude, phase = self.filter.response()
        self.phaseGraph.updatePlot(w, phase)
        self.magnitudeGraph.updatePlot(w, magnitude)

        w_all_pass, _, phase_all_pass = self.filter.all_pass_response()
        self.correctedPhaseGraph.updatePlot(w_all_pass, phase_all_pass)

        if self.is_linked:
            x, y = self.pos()
            self.linked_item.setPos(x, -y)

    def delete(self):
        self.scene().removeItem(self)
        (
            self.filter.delete_pole(self)
            if self.symbol == "x"
            else self.filter.delete_zero(self)
        )
        w, magnitude, phase = self.filter.response()
        self.phaseGraph.updatePlot(w, phase)
        self.magnitudeGraph.updatePlot(w, magnitude)

        w_all_pass, _, phase_all_pass = self.filter.all_pass_response()
        self.correctedPhaseGraph.updatePlot(w_all_pass, phase_all_pass)

    def mouseDoubleClickEvent(self, event):
        self.delete()
        if self.is_linked and self.linked_item:
            self.linked_item.delete()


class Pole(CustomTargetItem):
    def __init__(self, designer, *args, **kwargs):
        super().__init__(designer, symbol="x", *args, **kwargs)


class Zero(CustomTargetItem):
    def __init__(self, designer, *args, **kwargs):
        super().__init__(designer, symbol="o", *args, **kwargs)
