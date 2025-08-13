import sys
import os
import io
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFileDialog, QSpinBox, QMessageBox, QTableWidget,
    QGroupBox, QSizePolicy, QGridLayout, QHeaderView, QTableWidgetItem,QFormLayout
)
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IF plot and cal from Spectrum(PyQt5)")
        self.setGeometry(100, 100, 1100, 420)

        self.data = None
        self.meta = {}

        # Central widget + main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Top bar (buttons)
        self.load_1_button = QPushButton("Choose a y-factor file(.dat/.txt)")
        self.load_2_button = QPushButton("Choose Spectrum Hot file(.dat/.txt)")
        self.load_3_button = QPushButton("Choose Spectrum cold file(.dat/.txt)")
        self.load_1_button.clicked.connect(self.load_data)

        self.topleft_layout = QVBoxLayout()
        self.topleft_layout.addWidget(self.load_1_button)
        self.topleft_layout.addWidget(self.load_2_button)
        self.topleft_layout.addWidget(self.load_3_button)


        # Top-center: params (FormLayout)
        self.spin_thot = QSpinBox()
        #self.spin_thot.setRange(1, 10000)
        self.spin_thot.setValue(4)

        self.spin_tcold = QSpinBox()
        #self.spin_tcold.setRange(1, 10000)
        self.spin_tcold.setValue(18)

        self.spin_tsysmax = QSpinBox()
        #self.spin_tsysmax.setRange(10, 10000)
        self.spin_tsysmax.setValue(1)

        #self.topcent_layout = QVBoxLayout()
        #self.topcent_layout.addWidget(QLabel("Star Freq"))
        #self.topcent_layout.addWidget(self.spin_thot)
        #self.topcent_layout.addWidget(QLabel("End Freq"))
        #self.topcent_layout.addWidget(self.spin_tcold)
        #self.topcent_layout.addWidget(QLabel("Gap Freq"))
        #self.topcent_layout.addWidget(self.spin_tsysmax)
        self.topcent_layout = QFormLayout()
        self.topcent_layout.addRow(QLabel("Star Freq"), self.spin_thot)
        self.topcent_layout.addRow(QLabel("End Freq"), self.spin_tcold)
        self.topcent_layout.addRow(QLabel("TsysMax (K)"), self.spin_tsysmax)


        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_data)

        # Top row layout
        top_layout = QHBoxLayout()
        top_layout.addLayout(self.topleft_layout, 6)
        top_layout.addLayout(self.topcent_layout, 2)
        top_layout.addWidget(self.plot_button, 2)


        # Canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # main page, 
        main_layout.addLayout(top_layout, 4)
        main_layout.addWidget(self.canvas, 6)


    def _sanitize_cols(self, cols):
        # make the title more easy
        c = pd.Index(cols).str.strip()
        c = c.str.replace(' ', '_', regex=False)
        c = c.str.replace('(', '_', regex=False)
        c = c.str.replace(')', '', regex=False)
        c = c.str.replace('/', '_per_', regex=False)
        return c

    def load_data(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a file",
            "",
            "DAT/TXT files (*.dat *.txt);;All files (*)"
        )
        if not path:
            return

        try:
            # 先讀原始文字，分出「前置鍵值行」與「資料表」
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().strip().splitlines()

            # find IF(GHz).
            header_idx = None
            for i, line in enumerate(lines):
                # remove space, and sep with tab
                if line.strip().startswith("IF(GHz)"):
                    header_idx = i
                    break

            if header_idx is None:
                raise ValueError("找不到資料欄位標頭（預期以 'IF(GHz)' 開頭的一行）。")

            # sep with tab \t
            self.meta = {}
            for line in lines[:header_idx]:
                if not line.strip():
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    self.meta[key] = val

            # 把資料表（含標頭）組成字串再交給 pandas
            table_text = "\n".join(lines[header_idx:])
            df = pd.read_csv(io.StringIO(table_text), delimiter='\t')

            # 清理欄名
            df.columns = self._sanitize_cols(df.columns)

            # make sure 3 col. 
            if df.shape[1] < 3:
                QMessageBox.warning(self, "Invalid File", "資料表必須至少含 3 欄。")
                self.data = None
                return

            self.data = df

            file_name = os.path.basename(path)
            self.load_1_button.setText(file_name)  # 修正變數名稱
            self.setWindowTitle(f"Plot Generator - {file_name}")

            # 簡單提示已讀到幾筆
            QMessageBox.information(self, "Success", f"File loaded: {file_name}\nRows: {len(self.data)}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
            self.data = None

    def plot_data(self):
        if self.data is None:
            QMessageBox.warning(self, "No Data", "Please load a .dat/.txt file first.")
            return
        #print("Columns:", list(self.data.columns))
        #Columns: ['IF_GHz', 'Hot-Power_dBm', 'Cold-Power_dBm', 'Y-factor', 'Tsys']
        # 優先使用 Hot/Cold-Power，如果找不到就用第 2、3 欄
        cols = list(self.data.columns)
        x_col = cols[0]

        # 嘗試找特定欄位
        def find_col(name_candidates):
            for c in self.data.columns:
                if c in name_candidates:
                    return c
            return None

        hot_p = find_col(["Hot-Power_dBm", "Hot-Power_dBm_"])
        cold_p = find_col(["Cold-Power_dBm", "Cold-Power_dBm_"])
        tsys = find_col(["Tsys", "Tsys_"])

        if hot_p is None or cold_p is None or tsys is None:
            # fallback：用第 2 與第 3 欄
            if len(cols) >= 5:
                hot_p = cols[1]
                cold_p = cols[2]
                tsys_col=cols[4]
            else:
                QMessageBox.warning(self, "Not Enough Columns", "資料不足以繪圖。")
                return

        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        ax1.set_xlabel("Frequency (GHz)")
        ax1.set_ylabel("Power (dBm)")
        l1 = ax1.plot(self.data[x_col],self.data[hot_p], color='r', label="Hot Load Power")
        l2 = ax1.plot(self.data[x_col],self.data[cold_p], color='b', label="Cold Load Power")
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.grid(True)

        ax2 = ax1.twinx()  # 2nd Y-axis（Right）
        show_trx = False
        ax2.plot(self.data[x_col],self.data[tsys], label="Tsys (K)", color="green")
        ax2.set_ylabel("Tsys (K)", color="green")
        ax2.set_ylim(20, 220)  # 固定 Tsys y 軸範圍
        #show_trx = True

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        #lines = l1 + l2
        #labels = [line.get_label() for line in lines]
        #ax1.legend(lines, labels, loc=0)

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotApp()
    window.show()
    sys.exit(app.exec_())
