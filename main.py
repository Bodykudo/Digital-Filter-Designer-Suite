from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QFileDialog, QWidget
import pyqtgraph as pg

import numpy as np
import pandas as pd
from scipy import signal

from view.mainwindow import Ui_MainWindow
from view.Designer import Designer
from view.Graphs import MagnitudeGraph, PhaseGraph
from view.FilterItem import FilterItem
from view.ListItem import ListItem

from model.Filter import AllPass, Filter
from utils.constants import filters, all_pass_list


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # Initialize the filter and graphs
        self.filter = Filter()
        self.filterPhaseGraphWidget.setLayout(QVBoxLayout())
        self.filterMagnitudeGraphWidget.setLayout(QVBoxLayout())
        self.phaseGraph = PhaseGraph(dark_mode=self.isDarkMode())
        self.magnitudeGraph = MagnitudeGraph(dark_mode=self.isDarkMode())
        self.filterPhaseGraphWidget.layout().addWidget(self.phaseGraph)
        self.filterMagnitudeGraphWidget.layout().addWidget(self.magnitudeGraph)

        # Initialize the corrected phase and magnitude graphs
        self.correctedPhaseGraph = PhaseGraph(dark_mode=self.isDarkMode())
        self.correctedPhaseGraphWidget.setLayout(QVBoxLayout())
        self.correctedPhaseGraphWidget.layout().addWidget(self.correctedPhaseGraph)
        self.correctedPhaseGraph.setTitle("Corrected phase")

        self.allPassPhaseGraph = PhaseGraph(dark_mode=self.isDarkMode())
        self.allPassPhaseGraphWidget.setLayout(QVBoxLayout())
        self.allPassPhaseGraphWidget.layout().addWidget(self.allPassPhaseGraph)
        self.allPassPhaseGraph.setTitle("All-pass phase")

        # Initialize the designer
        self.designer = Designer(
            filter=self.filter,
            phaseGraph=self.phaseGraph,
            magnitudeGraph=self.magnitudeGraph,
            correctedPhaseGraph=self.correctedPhaseGraph,
            allPassPhaseGraph=self.allPassPhaseGraph,
            dark_mode=self.isDarkMode(),
        )
        self.designerWidget.setLayout(QVBoxLayout())
        self.designerWidget.layout().addWidget(self.designer)

        # Connect the buttons to their respective functions
        self.addPoleButton.clicked.connect(lambda: self.designer.setItem("pole"))
        self.addZeroButton.clicked.connect(lambda: self.designer.setItem("zero"))
        self.deletePolesButton.clicked.connect(self.filter.delete_poles)
        self.deleteZerosButton.clicked.connect(self.filter.delete_zeros)
        self.deleteAllButton.clicked.connect(self.filter.delete_all)
        self.addPairs.stateChanged.connect(self.designer.togglePair)

        # Connect the tabs to their respective functions
        self.allPassTab.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.mousePadTab.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        # Initialize the mouse pad
        self.mousePadPlot = pg.PlotWidget()
        self.mousePadPlot.setBackground("black")
        self.mousePadGraphWidget.setLayout(QVBoxLayout())
        self.mousePadGraphWidget.layout().addWidget(self.mousePadPlot)
        self.mousePadPlot.getPlotItem().hideAxis("bottom")
        self.mousePadPlot.getPlotItem().hideAxis("left")
        self.x_coordinates = []
        self.y_coordinates = []
        self.points_plotted = 0
        self.mousePadPlot.mouseMoveEvent = self.handlePadMouseEvent

        # Initialize the current filter
        self.currentFilter = filters[0]["filter"]

        # Initialize the signal graphs
        self.signalGraphsWidget.setLayout(QVBoxLayout())
        self.originalSignalGraph = pg.PlotWidget()
        if not self.isDarkMode():
            self.originalSignalGraph.setBackground("w")
        self.originalSignalGraph.showGrid(x=True, y=True)
        self.originalSignalGraph.setTitle("Original Signal")
        self.signalGraphsWidget.layout().addWidget(self.originalSignalGraph)

        self.filteredSignalGraph = pg.PlotWidget()
        if not self.isDarkMode():
            self.filteredSignalGraph.setBackground("w")
        self.filteredSignalGraph.showGrid(x=True, y=True)
        self.filteredSignalGraph.setTitle(f"Filterd Signal ({filters[0]['name']})")
        self.signalGraphsWidget.layout().addWidget(self.filteredSignalGraph)
        self.uploadButton.clicked.connect(self.handleUploadSignal)

        # Initialize the all-pass filters
        self.allpassFilterSelect.addItems(
            str(all_pass_filter) for all_pass_filter in all_pass_list
        )

        self.selectAllPassButton.clicked.connect(self.handleAddAllPass)
        self.allpassFilterScrollAreaContents.setLayout(QVBoxLayout())
        self.scrollAreaWidgetContents.setLayout(QVBoxLayout())
        self.saveAllPassButton.clicked.connect(self.handleSaveAllPass)

        # Add the filters to the list of filters
        for filter in filters:
            self.addNewFilter(filter)

        # Connect the buttons to their respective functions
        self.deleteSignalButton.clicked.connect(self.handleClearSignal)
        self.saveFilterButton.clicked.connect(self.saveFilter)

        self.isUploadedSignal = False

    def handleUploadSignal(self):
        """Uploads a signal from a CSV file."""
        file, _ = QFileDialog.getOpenFileName(
            self, "Open file", ".\\", "CSV files (*.csv)"
        )
        if file:
            self.isUploadedSignal = True
            df = pd.read_csv(file)
            data_x = df.iloc[:, 0].values
            data_y = df.iloc[:, 1].values

            self.originalSignalGraph.getViewBox().setXRange(data_x[0], data_x[-1])
            self.originalSignalGraph.getViewBox().setYRange(min(data_y), max(data_y))
            self.filteredSignalGraph.getViewBox().setXRange(data_x[0], data_x[-1])
            self.filteredSignalGraph.getViewBox().setYRange(min(data_y), max(data_y))

            numerator, denominator = signal.zpk2tf(
                self.currentFilter.get_zeros(),
                self.currentFilter.get_poles(),
                self.currentFilter.get_gain(),
            )
            filtered_signal_y = np.real(
                signal.lfilter(numerator, denominator, data_y.copy())
            )

            self.originalSignalGraph.clear()
            self.originalSignalGraph.plot(data_x, data_y, pen="b")

            self.filteredSignalGraph.clear()
            self.filteredSignalGraph.plot(data_x, filtered_signal_y, pen="r")

    def handleClearSignal(self):
        """Clears the signal from the graph."""
        self.isUploadedSignal = False
        self.originalSignalGraph.clear()
        self.filteredSignalGraph.clear()
        self.originalSignalGraph.getViewBox().setXRange(0, 1)
        self.originalSignalGraph.getViewBox().setYRange(0, 1)
        self.filteredSignalGraph.getViewBox().setXRange(0, 1)
        self.filteredSignalGraph.getViewBox().setYRange(0, 1)
        self.x_coordinates = []
        self.y_coordinates = []
        self.points_plotted = 0

    def addNewAllPass(self, allPass, allPassString):
        """Adds a new all-pass filter to the list of all-pass filters."""
        newListItem = ListItem(allPassString)
        self.allpassFilterScrollAreaContents.layout().addWidget(newListItem)
        newListItem.deleteButton.clicked.connect(
            lambda: self.deleteAllPass(allPass, newListItem)
        )
        self.updateCorrectedGraphs()

    def handleAddAllPass(self):
        """Adds the selected all-pass filter to the list of all-pass filters."""
        new_all_pass = AllPass(complex(self.allpassFilterSelect.currentText()))
        self.filter.add_all_pass(new_all_pass)
        self.addNewAllPass(new_all_pass, self.allpassFilterSelect.currentText())

    def handleSaveAllPass(self):
        """Saves the all-pass filter to the list of all-pass filters."""
        try:
            complex_value = complex(self.allpassFilterInput.text())
            new_all_pass = AllPass(complex_value)
            self.filter.add_all_pass(new_all_pass)
            self.addNewAllPass(new_all_pass, self.allpassFilterInput.text())
            self.allpassFilterInput.setText("")
        except ValueError:
            print("Invalid input: Please enter a valid complex number.")

    def deleteAllPass(self, allPass, listItem):
        """Deletes the selected all-pass filter from the list of all-pass filters."""
        self.filter.delete_all_pass(allPass)
        listItem.hide()
        self.updateCorrectedGraphs()

    def updateCorrectedGraphs(self):
        """Updates the corrected phase and magnitude graphs with the current filter's response."""
        w_all_pass, _, phase_all_pass = self.filter.all_pass_response()
        self.correctedPhaseGraph.updatePlot(w_all_pass, phase_all_pass)

        all_pass_list = self.filter.get_all_pass()
        all_pass_poles = [all_pass.a for all_pass in all_pass_list]
        all_pass_zeros = [1 / np.conj(all_pass.a) for all_pass in all_pass_list]
        w, response = signal.freqz_zpk(
            all_pass_zeros, all_pass_poles, self.filter.get_gain()
        )
        phase = np.unwrap(np.angle(response))
        self.allPassPhaseGraph.updatePlot(w, phase)

    def addNewFilter(self, filter):
        """Adds a new filter to the list of filters"""
        newFilterItem = FilterItem(filter["name"])
        newFilterItem.applyButton.clicked.connect(
            lambda: self.handleChangeFilter(filter["name"], filter["filter"])
        )
        self.scrollAreaWidgetContents.layout().addWidget(newFilterItem)

    def saveFilter(self):
        """Saves the current filter to the list of filters"""
        newFilterObj = Filter(
            poles=[*self.filter.get_poles()],
            zeros=[*self.filter.get_zeros()],
            gain=0.05,
        )

        newFilter = {"name": self.filterNameInput.text(), "filter": newFilterObj}

        self.filterNameInput.setText("")
        self.addNewFilter(newFilter)
        self.filter.delete_all()
        self.filter.delete_all_passes()
        self.updateCorrectedGraphs()
        layout = self.allpassFilterScrollAreaContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.stackedWidget.setCurrentIndex(1)

    def handleChangeFilter(self, name: str, filter: Filter):
        """Changes the current filter to the selected filter"""
        self.currentFilter = filter
        self.filteredSignalGraph.clear()
        numerator, denominator = signal.zpk2tf(
            self.currentFilter.get_zeros(),
            self.currentFilter.get_poles(),
            self.currentFilter.get_gain(),
        )
        filtered_signal_y = np.real(
            signal.lfilter(numerator, denominator, self.y_coordinates.copy())
        )
        self.filteredSignalGraph.setLimits(xMin=0, xMax=float("inf"))
        self.filteredSignalGraph.setTitle(f"Filtered Signal ({name})")
        self.filteredSignalGraph.plot(self.x_coordinates, filtered_signal_y, pen="r")

    def handlePadMouseEvent(self, event):
        """Handles the mouse movement on the mouse pad to draw new signal"""
        if not self.isUploadedSignal:
            self.points_plotted += 1
            cursor_position = event.pos()
            cursor_y = cursor_position.y()

            self.y_coordinates.append(cursor_y)
            self.x_coordinates = np.arange(len(self.y_coordinates))

            numerator, denominator = signal.zpk2tf(
                self.currentFilter.get_zeros(),
                self.currentFilter.get_poles(),
                self.currentFilter.get_gain(),
            )
            filtered_signal_y = np.real(
                signal.lfilter(numerator, denominator, self.y_coordinates.copy())
            )

            self.originalSignalGraph.clear()
            self.originalSignalGraph.setLimits(xMin=0, xMax=float("inf"))
            self.originalSignalGraph.plot(
                self.x_coordinates, self.y_coordinates, pen="b"
            )

            self.filteredSignalGraph.setLimits(xMin=0, xMax=float("inf"))
            self.filteredSignalGraph.plot(
                self.x_coordinates, filtered_signal_y, pen="r"
            )

            if self.points_plotted < 100:
                self.originalSignalGraph.getViewBox().setXRange(
                    self.x_coordinates[0], self.x_coordinates[-1]
                )
                self.filteredSignalGraph.getViewBox().setXRange(
                    self.x_coordinates[0], self.x_coordinates[-1]
                )
            else:
                self.originalSignalGraph.getViewBox().setXRange(
                    self.x_coordinates[self.points_plotted - 100],
                    self.x_coordinates[-1],
                )
                self.filteredSignalGraph.getViewBox().setXRange(
                    self.x_coordinates[self.points_plotted - 100],
                    self.x_coordinates[-1],
                )

    def isDarkMode(self):
        """
        Checks if the application is in dark mode
        """
        widget = QWidget()
        color = widget.palette().color(QWidget().backgroundRole())
        brightness = color.red() * 0.299 + color.green() * 0.587 + color.blue() * 0.114
        return brightness < 128


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
