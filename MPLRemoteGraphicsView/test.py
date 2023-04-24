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
        self.rpv = MPLRemoteGraphicsView()
        self.proc = self.rpv.remoteProcess()
    
        rwidgets = self.proc._import('PyQt5.QtWidgets')
        self._qApp = rwidgets.qApp
        rcore = self.proc._import('PyQt5.QtCore')
        rmpl_figure = self.proc._import("matplotlib.figure")
        rmpl_qtagg = self.proc._import("matplotlib.backends.backend_qtagg")
        figure = rmpl_figure.Figure()
        # figure.show()
        self.dynamic_canvas = rmpl_qtagg.FigureCanvas(figure)
        navbar = rmpl_qtagg.NavigationToolbar2QT(self.dynamic_canvas)
        # dynamic_canvas.show()
        # rbtn = rgui.QPushButton()

        # gv = GraphicsView()
        # gv.setCentralWidget(dynamic_canvas)
        # gv = rpv.pg.GraphicsWidget()
        # dynamic_canvas.zValue = 0
        # dynamic_canvas.geometryChanged = None
        # gv.setLayout(dynamic_canvas)

        self._dynamic_ax = self.dynamic_canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))

        
        # self._timer = dynamic_canvas.new_timer(50)
        # self._timer.add_callback(print_test)
        # self._timer.start()
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_canvas)
        self._timer.start(50)

        layout = QVBoxLayout()
        # self.rgv = self.rpv.pg.GraphicsWidget()
        # rgLayout = rwidgets.QGraphicsGridLayout()
        # rscene = rwidgets.QGraphicsScene()
        # # rgLayout.add
        # self.rgi = rscene.addWidget(self.dynamic_canvas)
        # rgLayout.addItem(self.rgi, 0, 0)
        # rscene1 = rwidgets.QGraphicsScene()
        # self.rgi1 = rscene.addWidget(navbar)
        # rgLayout.addItem(self.rgi1, 1, 0)
        # self.rgv.setLayout(rgLayout)
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
        # Shift the sinusoid as a function of time.
        # self._line.set_data(t, np.sin(t + time.time()))
        # self._line.figure.canvas.draw()
        # self._line.figure.canvas.flush_events()
        self._dynamic_ax.clear()
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self.test = (self.test + 1) % 2
        self._dynamic_ax.autoscale()
        self.dynamic_canvas.draw()
        self.dynamic_canvas.flush_events()

        # self.rpv.remoteSceneChanged([1, 1, 1])
        # self.rpv._view.renderView()
        # self.rpv.scene().update()
        # self.rpv._view.resize(QSize(480+self.test, 320))
        
        # self.rpv.resize(QSize(480+self.test, 320))
        # self._qApp.processEvents()
        # self.rpv._view.repaint()
        # self.dynamic_canvas.update()
        # self.rgv.prepareGeometryChange()
        # self.rgv.informViewBoundsChanged()
        # self.rgv.viewTransformChanged()

        # self.rgv._resetCachedProperties()
        # self.rgv.prepareGeometryChange()
        # self.rgv.informViewBoundsChanged()
        # self.rgv._updateView()

if __name__=="__main__":
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    # rbtn.show()

    def testslot(v):
        print("remote slot test!")

    # rbtn.clicked.connect(multiprocess.remoteproxy.proxy(testslot))   # be sure to send a proxy of the slot


    sys.exit(app.exec_())