import sys
import pyvisa
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SpectrumPlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSV-30 Hot/Cold Load 與 Y-factor 計算")
        self.setGeometry(100, 100, 1100, 750)

        # 按鈕
        self.hot_button = QPushButton("Hot Load")
        self.cold_button = QPushButton("Cold Load")
        self.save_button = QPushButton("儲存資料與圖")
        self.hot_button.clicked.connect(self.read_hot)
        self.cold_button.clicked.connect(self.read_cold)
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setEnabled(False)  # 開始時關閉儲存功能

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.hot_button)
        button_layout.addWidget(self.cold_button)
        button_layout.addWidget(self.save_button)

        # 圖形
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Freq (GHz)", "Hot (W)", "Cold (W)", "Y-factor", "Trx (K)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 資料暫存
        self.x_data = None
        self.hot_trace = None
        self.cold_trace = None
        self.trx_array = None

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
        ax1 = self.figure.add_subplot(111)

        if self.hot_trace is not None:
            ax1.plot(self.x_data, self.hot_trace, label="Hot Load", color="red")
        if self.cold_trace is not None:
            ax1.plot(self.x_data, self.cold_trace, label="Cold Load", color="blue")

        ax1.set_xlabel("Frequency (GHz)")
        ax1.set_ylabel("Power (dBm)")
        ax1.grid(True)

        ax2 = ax1.twinx()  # 第二 Y 軸（右邊）
        show_trx = False

        if self.hot_trace is not None and self.cold_trace is not None:
            self.update_table()  # 計算 trx
            if self.trx_array is not None:
                ax2.plot(self.x_data, self.trx_array, label="Tsys (K)", color="green")
                ax2.set_ylabel("Tsys (K)", color="green")
                show_trx = True
                self.save_button.setEnabled(True)

        ax1.legend(loc="upper left")
        if show_trx:
            ax2.legend(loc="upper right")

        self.canvas.draw()

    def update_table(self):
        hot_watt = 10 ** ((self.hot_trace - 30) / 10)
        cold_watt = 10 ** ((self.cold_trace - 30) / 10)

        with np.errstate(divide='ignore', invalid='ignore'):
            y_factor = np.where(cold_watt > 0, hot_watt / cold_watt, np.nan)
            trx = (296 - 77 * y_factor) / (y_factor - 1)
            trx = np.where(np.isfinite(trx), trx, np.nan)
            self.trx_array = trx  # 存下來畫圖用

        self.table.setRowCount(len(self.x_data))
        for i in range(len(self.x_data)):
            self.table.setItem(i, 0, QTableWidgetItem(f"{self.x_data[i]:.3f}"))
            self.table.setItem(i, 1, QTableWidgetItem(f"{hot_watt[i]:.4e}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{cold_watt[i]:.4e}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{y_factor[i]:.3f}" if np.isfinite(y_factor[i]) else ""))
            self.table.setItem(i, 4, QTableWidgetItem(f"{trx[i]:.2f}" if np.isfinite(trx[i]) else ""))

        # 同步存成 DataFrame 供儲存用
        self.result_df = pd.DataFrame({
            "IF": self.x_data,
            "Hot(dBm)": self.hot_trace,
            "Cold(dBm)": self.cold_trace,
            "Y-factor": y_factor,
            "Tsys": trx
        })
    def save_results(self):
        try:
            # 讓使用者選擇要儲存的 .dat 檔名
            dat_path, _ = QFileDialog.getSaveFileName(self, "儲存資料", "spectrum_data.dat", "DAT Files (*.dat)")
            if not dat_path:
                return

            with open(dat_path, 'w', encoding='utf-8') as f:
                # 自訂 header 5 行（可自由調整數值）
                f.write("SIS V(mV)\t-0.1\n")
                f.write("SIS C(uA)\t25.2\n")
                f.write("SIS Mag (mA)\t-0.1\n")
                f.write("LO PA Vd (V)\t0.00\n")
                f.write("LO PA Id (mA)\t0.00\n")

                # 寫入資料表頭
                f.write("IF(GHz)\tHot-Power(dBm)\tCold-Power(dBm)\tY-factor\tTsys\n")
                #f.write("IF(GHz)\tHot(dBm)\tCold(dBm)\tY-factor\tTsys(K)\n")

                # 寫入每一列資料
                for i in range(len(self.result_df)):
                    row = self.result_df.iloc[i]
                    f.write(f"{row['IF']:.2f}\t{row['Hot(dBm)']:.2f}\t{row['Cold(dBm)']:.2f}\t{row['Y-factor']:.2f}\t{row['Tsys']:.2f}\n")

            # 圖檔儲存（與資料同路徑，副檔名為 .png）
            png_path = dat_path.rsplit('.', 1)[0] + ".png"
            self.figure.savefig(png_path, dpi=300)

            QMessageBox.information(self, "儲存成功", "資料與圖檔已儲存完成！")

        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"儲存失敗：\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpectrumPlot()
    window.show()
    sys.exit(app.exec_())
