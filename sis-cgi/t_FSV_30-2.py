import sys
import pyvisa
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SpectrumPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSV-30 Spectrum Plot")
        self.setGeometry(100, 100, 800, 600)

        # 建立圖形與按鈕
        self.button = QPushButton("Download Spectrum and plot", self)
        self.button.clicked.connect(self.read_and_plot)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def read_and_plot(self):
        try:
            rm = pyvisa.ResourceManager()
            inst = rm.open_resource("GPIB0::18::INSTR")

            inst.timeout = 5000
            inst.write_termination = '\n'
            inst.read_termination = '\n'

            # 取得掃描資訊
            f_start = float(inst.query("FREQ:STAR?"))
            f_stop = float(inst.query("FREQ:STOP?"))
            points = int(inst.query("SWE:POIN?"))

            # 取得 spectrum 資料
            raw_data = inst.query("TRAC? TRACE1")
            y_data = np.array([float(v) for v in raw_data.strip().split(',')])
            x_data = np.linspace(f_start, f_stop, num=points) / 1e9  # 轉 GHz

            inst.close()

            # 畫圖
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_data, y_data)
            ax.set_title("Spectrum Trace (FSV-30)")
            ax.set_xlabel("Frequency (GHz)")
            ax.set_ylabel("Power (dBm)")
            ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "error", f"reading failed：\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpectrumPlot()
    window.show()
    sys.exit(app.exec_())
