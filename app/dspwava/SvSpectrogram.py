import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from scipy.signal import spectrogram
class SvSpectrogram(QWidget):
    point_clicked_signal = Signal(list)
    def __init__(self, rm=False):
        super().__init__()
        if rm:
            pg.setConfigOptions(imageAxisOrder='row-major')
        #pg.setConfigOptions(imageAxisOrder='row-major')
        # Create a PlotWidget
        self.imv = pg.ImageView()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.imv)
        self.setLayout(self.main_layout)

        self.hist = self.imv.getHistogramWidget()
        self.imv.view.setBackgroundColor('black')
        #histogram properties
        self.imv.ui.histogram.fillHistogram(fill=False)
        self.imv.view.invertY(False)
        #self.imv.ui.histogram.autoHistogramRange()
        self.imv.ui.histogram.plot.setBrush((200,200,0))
        self.imv.roi.removeHandle(1)
        colormap = pg.ColorMap(
                [0, 0.25, 0.5, 0.75, 1],
                [ (68, 1, 84), (58,82,139), (32,144,140), (94,201,97) , (253, 231, 36)]
            )
        self.imv.setColorMap(colormap)

        self.spect = None
        self.signal = None

