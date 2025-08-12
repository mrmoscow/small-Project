import sys
import pyvisa
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox,QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SpectrumPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSV-30 Hot/Cold Load 比較")
        self.setGeometry(100, 100, 900, 600)

        # 建立兩個按鈕
        self.hot_button = QPushButton("Hot Load")
        self.cold_button = QPushButton("Cold Load")
        self.hot_button.clicked.connect(self.read_hot)
        self.cold_button.clicked.connect(self.read_cold)

        # 建立圖形元件
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # 資料暫存區
        self.x_data = None
        self.hot_trace = None
        self.cold_trace = None

        # 排版
        #layout = QVBoxLayout()
        #layout.addWidget(self.hot_button)
        #layout.addWidget(self.cold_button)
        #layout.addWidget(self.canvas)
        #self.setLayout(layout)
        # 建立按鈕的水平排版
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.hot_button)
        button_layout.addWidget(self.cold_button)

        # 建立主垂直排版，包含按鈕排版和 canvas
        layout = QVBoxLayout()
        layout.addLayout(button_layout)  # 把水平按鈕區加入
        layout.addWidget(self.canvas)    # 把畫布放在按鈕下方
        self.setLayout(layout)

    def read_trace_from_fsv(self):
        try:
            rm = pyvisa.ResourceManager()
            inst = rm.open_resource("GPIB0::18::INSTR")
            inst.timeout = 5000
            inst.write_termination = '\n'
            inst.read_termination = '\n'

            f_start = float(inst.query("FREQ:STAR?"))
            f_stop = float(inst.query("FREQ:STOP?"))
            points = int(inst.query("SWE:POIN?"))

            raw_data = inst.query("TRAC? TRACE1")
            y_data = np.array([float(v) for v in raw_data.strip().split(',')])
            x_data = np.linspace(f_start, f_stop, num=points) / 1e9  # GHz

            inst.close()
            return x_data, y_data

        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"GPIB 讀取失敗：\n{str(e)}")
            return None, None

    def read_hot(self):
        x, y = self.read_trace_from_fsv()
        if x is not None:
            self.x_data = x
            self.hot_trace = y
            self.update_plot()

    def read_cold(self):
        x, y = self.read_trace_from_fsv()
        if x is not None:
            self.x_data = x
            self.cold_trace = y
            self.update_plot()

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.hot_trace is not None:
            ax.plot(self.x_data, self.hot_trace, label="Hot Load", color="red")
        if self.cold_trace is not None:
            ax.plot(self.x_data, self.cold_trace, label="Cold Load", color="blue")

        ax.set_title("Hot/Cold Load Spectrum Trace")
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Power (dBm)")
        ax.grid(True)
        ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpectrumPlot()
    window.show()
    sys.exit(app.exec_())
