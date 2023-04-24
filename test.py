import sys
import time
import numpy as np
import logging

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsLinearLayout, QGraphicsItem, qApp
from PyQt5.QtCore import pyqtSignal as Signal, QTimer, QSize

from pyqtgraph import multiprocess
from pyqtgraph import RemoteGraphicsView
from pyqtgraph import GraphicsView, GraphicsItem
import pyqtgraph as pg
from matplotlib.figure import Figure

from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.style as mplstyle
# mplstyle.use('fast')
# mpl_logger = logging.getLogger("matplotlib")
# mpl_logger.setLevel(logging.INFO)

from MPLRemoteGraphicsView import MPLRemoteGraphicsView

def print_test():
    print("test")

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.rpv = MPLRemoteGraphicsView.MPLRemoteGraphicsView()
        self.proc = self.rpv.remoteProcess()
    
        rwidgets = self.proc._import('PyQt5.QtWidgets')
        self._qApp = rwidgets.qApp
        rcore = self.proc._import('PyQt5.QtCore')
        rmpl_figure = self.proc._import("matplotlib.figure")
        rmpl_qtagg = self.proc._import("matplotlib.backends.backend_qtagg")
        figure = rmpl_figure.Figure()

        self.dynamic_canvas = rmpl_qtagg.FigureCanvas(figure)
        navbar = rmpl_qtagg.NavigationToolbar2QT(self.dynamic_canvas)

        self._dynamic_ax = self.dynamic_canvas.figure.subplots(1, 2, squeeze=False)
        t = np.linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax[0, 0].plot(t, np.sin(t + time.time()))

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_canvas)
        self._timer.start(50)

        layout = QVBoxLayout()

        self.test = 0

        # self.rpv.setCentralItem(self.rgv)
        slayout = rwidgets.QVBoxLayout()
        slayout.addWidget(self.dynamic_canvas)
        slayout.addWidget(navbar)
        self.rpv.setLayout(slayout)
        layout.addWidget(self.rpv)

        self.setLayout(layout)


    def _update_canvas(self):
        t = np.linspace(self.test, 10, 101)
        self.test += 1
        self._dynamic_ax[0, 0].clear()
        self._dynamic_ax[0, 0].plot(t, np.sin(t + time.time()))
        self._dynamic_ax[0, 1].clear()
        self._dynamic_ax[0, 1].plot(t, np.sin(t + time.time()))
        self.test = (self.test + 1) % 2
        self._dynamic_ax[0, 1].autoscale()
        self.dynamic_canvas.draw()
        self.dynamic_canvas.flush_events()

if __name__=="__main__":
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    # rbtn.show()

    def testslot(v):
        print("remote slot test!")

    # rbtn.clicked.connect(multiprocess.remoteproxy.proxy(testslot))   # be sure to send a proxy of the slot


    sys.exit(app.exec_())