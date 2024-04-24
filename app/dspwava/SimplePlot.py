import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import Signal
class SvSimplePlot(QWidget):
    point_clicked_signal = Signal(list)
    def __init__(self):
        super().__init__()

        # Create a PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.plot_widget)
        self.setLayout(self.main_layout)

        self.scatter = None
        # flip y axis
        #self.plot_widget.invertY(True)
        


    def draw_signal(self, xs, ys):
        if self.scatter is not None:
            self.plot_widget.removeItem(self.scatter)
        self.scatter = pg.PlotCurveItem()
        self.plot_widget.addItem(self.scatter)
        self.scatter.setData(xs, ys)
        self.scatter.setPen(pg.mkPen(color=(171, 70, 188), width=1))
        
        #self.scatter.scene().sigMouseClicked.connect(self.on_point_clicked)

    def on_point_clicked(self, event):
        pos = event.pos()
        clicked_points = self.scatter.pointsAt(pos)
        if len(clicked_points) > 0 :
            print("Clicked on point at position:", clicked_points[0].pos())
            # Add your click event handling code here
            # get index of point
            pt = clicked_points[0].pos()
            i = self.data[str(pt[0])+' '+str(pt[1])]
            print(f'Point {i} clicked.')
            self.point_clicked_signal.emit(i)
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    signal = SvSignal(filepath='test_samples/ex_wav.wav')
    signal.toMono()
    plot = SvSimplePlot()
    plot.draw_signal(signal)
    plot.show()
    sys.exit(app.exec())