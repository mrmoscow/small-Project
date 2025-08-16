import sys
import os
import io
import numpy as np
import pandas as pd
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
        self.hotdata = None
        self.colddata = None
        self.meta = {}

        # Central widget + main layout

        # Top bar (buttons)
        self.load_1_button = QPushButton("Choose a y-factor file(.dat/.txt)")
        self.load_2_button = QPushButton("Choose Spectrum Hot file(.dat/.txt)")
        self.load_3_button = QPushButton("Choose Spectrum cold file(.dat/.txt)")
        self.load_1_button.clicked.connect(self.load_data)
        self.load_2_button.clicked.connect(self.load_hot_data)
        self.load_3_button.clicked.connect(self.load_cold_data)

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
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout, 4)
        main_layout.addWidget(self.canvas, 6)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)


    def _sanitize_cols(self, cols):
        c = pd.Index(cols).str.strip()
        c = c.str.replace(' ', '_', regex=False)
        c = c.str.replace('(', '_', regex=False)
        c = c.str.replace(')', '', regex=False)
        c = c.str.replace('/', '_per_', regex=False)
        return c  # ← 一定要回傳


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

    def load_hot_data(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Spectrum Hot file",
            "",
            "DAT files (*.DAT);;All files (*)"
        )
        if not path:
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().strip().splitlines()

            # 找到 "Values;" 這行，後面才是數據
            values_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith("Values;"):
                    values_idx = i
                    break

            if values_idx is None or values_idx + 1 >= len(lines):
                raise ValueError("找不到 Values; 標記或沒有數據。")

            # 解析前面的 meta 設定
            self.meta = {}
            for line in lines[:values_idx]:
                if not line.strip():
                    continue
                parts = line.split(';')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    self.meta[key] = val

            # 數據部分：以分號分隔，並強制三欄
            data_lines = lines[values_idx+1:]
            df = pd.read_csv(
                io.StringIO("\n".join(data_lines)),
                sep=';',
                header=None,
                names=['Frequency_Hz', 'Hot_Power_dBm', 'Extra_Col_dBm']
            )

            # 型別轉換
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            self.hotdata = df

            file_name = os.path.basename(path)
            self.load_2_button.setText(file_name)
            self.setWindowTitle(f"Plot Generator - {file_name}")
            QMessageBox.information(self, "Success",
                                    f"File loaded: {file_name}\nRows: {len(self.hotdata)}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
            self.hotdata = None


    def load_cold_data(self):
        if self.hotdata is None:
            QMessageBox.warning(self, "No Hot Data", "Please load Hot file first.")
            return
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Spectrum Cold file",
            "",
            "DAT files (*.DAT);;All files (*)"
        )
        if not path:
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().strip().splitlines()

            # 找到 "Values;" 這行，後面才是數據
            values_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith("Values;"):
                    values_idx = i
                    break

            if values_idx is None or values_idx + 1 >= len(lines):
                raise ValueError("找不到 Values; 標記或沒有數據。")

            # 解析前面的 meta 設定
            self.meta = {}
            for line in lines[:values_idx]:
                if not line.strip():
                    continue
                parts = line.split(';')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    val = parts[1].strip()
                    self.meta[key] = val

            # 數據部分：以分號分隔，並強制三欄
            data_lines = lines[values_idx+1:]
            df = pd.read_csv(
                io.StringIO("\n".join(data_lines)),
                sep=';',
                header=None,
                names=['Frequency_Hz', 'Cold_Power_dBm', 'Extra_Col_dBm']
            )

            # 型別轉換
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            self.colddata = df

            file_name = os.path.basename(path)
            self.load_3_button.setText(file_name)
            self.setWindowTitle(f"Plot Generator - {file_name}")
            QMessageBox.information(self, "Success",
                                    f"File loaded: {file_name}\nRows: {len(self.colddata)}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
            self.colddata = None
            # ===== 關鍵：確定 hotdata & colddata 都存在才做合併 =====
        if self.hotdata is not None and self.colddata is not None:
            try:
                hot_df = self.hotdata.rename(columns={'Hot_Power_dBm': 'Hot-Power_dBm'}).copy()
                cold_df = self.colddata.rename(columns={'Cold_Power_dBm': 'Cold-Power_dBm'}).copy()

                hot_df = hot_df[['Frequency_Hz', 'Hot-Power_dBm']].dropna()
                cold_df = cold_df[['Frequency_Hz', 'Cold-Power_dBm']].dropna()

                merged = pd.merge(hot_df, cold_df, on='Frequency_Hz', how='inner')
                merged['IF_GHz'] = merged['Frequency_Hz'] / 1e9

                hot_mW = 10 ** (merged['Hot-Power_dBm'] / 10.0)
                cold_mW = 10 ** (merged['Cold-Power_dBm'] / 10.0)
                Y = hot_mW / cold_mW

                HotT = 296.0
                ColdT = 77.0

                merged['Y-factor'] = Y
                merged['Tsys'] = (HotT - ColdT * Y) / (Y - 1.0)

                self.data = merged[['IF_GHz', 'Hot-Power_dBm', 'Cold-Power_dBm', 'Y-factor', 'Tsys']].copy()

                QMessageBox.information(
                    self, "Success",
                    f"Hot/Cold merged successfully.\nRows: {len(self.data)}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to merge hot & cold data: {e}")
                self.data = None


    def plot_data(self):
        if self.data is None:
            QMessageBox.warning(self, "No Data", "Please load a .dat/.txt file first.")
            return
        print("Columns:", list(self.data.columns))
        #Columns: ['IF_GHz', 'Hot-Power_dBm', 'Cold-Power_dBm', 'Y-factor', 'Tsys']
        # 優先使用 Hot/Cold-Power，如果找不到就用第 2、3 欄
        cols = list(self.data.columns)

        x_col = cols[0]
        hot_p = cols[1]
        cold_p = cols[2]
        tsys=cols[4]

        self.data[x_col] = pd.to_numeric(self.data[x_col], errors='coerce')
        self.data[hot_p] = pd.to_numeric(self.data[hot_p], errors='coerce')
        self.data[cold_p] = pd.to_numeric(self.data[cold_p], errors='coerce')
        self.data[tsys] = pd.to_numeric(self.data[tsys], errors='coerce')

        # 2) 丟掉有 NaN 的列，避免 matplotlib 再噴其他錯
        dfp = self.data[[x_col, hot_p, cold_p] + ([cols[4]] if len(cols) > 4 else [])].dropna()

        # 3) 關鍵：轉成 numpy 一維陣列後再 plot
        x = dfp[x_col].to_numpy()
        y_hot = dfp[hot_p].to_numpy()
        y_cold = dfp[cold_p].to_numpy()

        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        ax1.set_xlabel("Frequency (GHz)")
        ax1.set_ylabel("Power (dBm)")
        ax1.grid(True)

        ax1.plot(x, y_hot, label="Hot Load Power")   # 不要直接丟 pandas Series
        ax1.plot(x, y_cold, label="Cold Load Power")


        ax2 = ax1.twinx()  # 2nd Y-axis（Right）
        show_trx = False
        ax2.plot(self.data[x_col],self.data[tsys], label="Tsys (K)", color="green")
        ax2.set_ylabel("Tsys (K)", color="green")
        ax2.set_ylim(20, 420)  # 固定 Tsys y 軸範圍
        show_trx = True

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
