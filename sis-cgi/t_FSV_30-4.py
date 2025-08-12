import sys
import pyvisa
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SpectrumPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSV-30 Hot/Cold Load 與 Y-factor 計算")
        self.setGeometry(100, 100, 1000, 700)

        # 按鈕
        self.hot_button = QPushButton("Hot Load")
        self.cold_button = QPushButton("Cold Load")
        self.hot_button.clicked.connect(self.read_hot)
        self.cold_button.clicked.connect(self.read_cold)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.hot_button)
        button_layout.addWidget(self.cold_button)

        # 圖形顯示
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # 表格顯示
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Freq (GHz)", "Hot (W)", "Cold (W)", "Y-factor", "Trx (K)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 資料暫存區
        self.x_data = None
        self.hot_trace = None
        self.cold_trace = None

        # 整體排版
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.table)
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
            x_data = np.linspace(f_start, f_stop, num=points) / 1e9  # 轉 GHz

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

        ax.set_title("Spectrum Trace")
        ax.set_xlabel("Frequency (GHz)")
        ax.set_ylabel("Power (dBm)")
        ax.grid(True)
        ax.legend()
        self.canvas.draw()

        # 如果兩筆資料都有，就計算 Y-factor 和 Trx
        if self.hot_trace is not None and self.cold_trace is not None:
            self.update_table()


    def update_table(self):
        hot_watt = 10 ** ((self.hot_trace - 30) / 10)
        cold_watt = 10 ** ((self.cold_trace - 30) / 10)

        with np.errstate(divide='ignore', invalid='ignore'):
            y_factor = np.where(cold_watt > 0, hot_watt / cold_watt, np.nan)
            trx = (296 - 77 * y_factor) / (y_factor - 1)
            trx = np.where(np.isfinite(trx), trx, np.nan)

        self.table.setRowCount(len(self.x_data))
        for i in range(len(self.x_data)):
            self.table.setItem(i, 0, QTableWidgetItem(f"{self.x_data[i]:.3f}"))
            self.table.setItem(i, 1, QTableWidgetItem(f"{hot_watt[i]:.4e}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{cold_watt[i]:.4e}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{y_factor[i]:.3f}" if np.isfinite(y_factor[i]) else ""))
            self.table.setItem(i, 4, QTableWidgetItem(f"{trx[i]:.2f}" if np.isfinite(trx[i]) else ""))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpectrumPlot()
    window.show()
    sys.exit(app.exec_())


