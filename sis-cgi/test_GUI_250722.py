import sys
import os
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFileDialog, QSpinBox, QMessageBox, QTableWidget,
    QGroupBox, QSizePolicy, QGridLayout, QHeaderView, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#from scipy import stats

class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plot Generator (PyQt5)")
        self.setGeometry(100, 100, 1400, 1000)

        # self.data = None
        # self.range_inputs = []

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Top: Load + plot
        top_layout = QHBoxLayout()
        self.load_button = QPushButton("Choose a file (.dat)")
        self.load_button.clicked.connect(self.load_data)

        self.plot_button = QPushButton("Plot Data")
        self.plot_button.clicked.connect(self.plot_data)

        top_layout.addWidget(self.load_button)
        top_layout.addWidget(self.plot_button)
        main_layout.addLayout(top_layout)

        # Middle: plot and control
        center_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)

        # Left: plot area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(self.canvas, 3)

        # Right: controls
        control_layout = QVBoxLayout()
        # center_layout.addLayout(control_layout, 1)

        self.method_combo = QComboBox()
        self.method_combo.addItems(["Ordinary Least Squares", "Least Absolute Residual", "Bisquare"])
        control_layout.addWidget(QLabel("Method to fit:"))
        control_layout.addWidget(self.method_combo)

        # Unit Group
        self.unit_group = QGroupBox("Units:")
        unit_layout = QGridLayout()
        self.unit_group.setLayout(unit_layout)
        self.unit_v = QComboBox(); self.unit_v.addItems(["V", "mV"])
        self.unit_i = QComboBox(); self.unit_i.addItems(["A", "mA", "μA"])
        self.unit_p = QComboBox(); self.unit_p.addItems(["W", "mW"])
        unit_layout.addWidget(QLabel("Voltage:"), 0, 0)
        unit_layout.addWidget(self.unit_v, 0, 1)
        unit_layout.addWidget(QLabel("Current:"), 1, 0)
        unit_layout.addWidget(self.unit_i, 1, 1)
        unit_layout.addWidget(QLabel("Power:"), 2, 0)
        unit_layout.addWidget(self.unit_p, 2, 1)
        control_layout.addWidget(self.unit_group)

        self.scale_v = self.unit_scale(self.unit_v.currentText())
        self.scale_i = self.unit_scale(self.unit_i.currentText())
        self.scale_p = self.unit_scale(self.unit_p.currentText())

        # Mode Group
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Manually", "Automatically"])
        control_layout.addWidget(QLabel("Fit mode:"))
        control_layout.addWidget(self.mode_combo) 

        # Control for I-V and P-V fit ranges
        range_container = QHBoxLayout()
        self.iv_range_spin = QSpinBox(); self.iv_range_spin.setRange(1, 5); self.iv_range_spin.setValue(3)
        self.iv_range_spin.valueChanged.connect(self.update_iv_table)
        self.pv_range_spin = QSpinBox(); self.pv_range_spin.setRange(1, 2); self.pv_range_spin.setValue(1)
        self.pv_range_spin.valueChanged.connect(self.update_pv_table)

        iv_layout = QVBoxLayout()
        iv_layout.addWidget(QLabel("No. of I-V ranges:"))
        iv_layout.addWidget(self.iv_range_spin)
        self.iv_table = QTableWidget(3, 2)
        self.iv_table.setHorizontalHeaderLabels(["V_start", "V_end"])
        iv_layout.addWidget(QLabel("I-V Fit Ranges:"))
        iv_layout.addWidget(self.iv_table)

        pv_layout = QVBoxLayout()
        pv_layout.addWidget(QLabel("No. of P-V ranges:"))
        pv_layout.addWidget(self.pv_range_spin)
        self.pv_table = QTableWidget(1, 2)
        self.pv_table.setHorizontalHeaderLabels(["V_start", "V_end"])
        pv_layout.addWidget(QLabel("P-V Fit Ranges:"))
        pv_layout.addWidget(self.pv_table)

        range_container.addLayout(iv_layout)
        range_container.addLayout(pv_layout)
        control_layout.addLayout(range_container)

        self.fit_btn = QPushButton("Fit")
        self.fit_btn.clicked.connect(self.fit_data)
        control_layout.addWidget(self.fit_btn)
        center_layout.addLayout(control_layout, 2)

        # Result box
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels([
            "Segment", "Voltage Range", "No. of data points",
            "Slope dI/dV", "Slope dP/dV", "Intercept", "StdErr", "R²"
        ])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.result_tif = QTableWidget()
        self.result_tif.setRowCount(6)
        self.result_tif.setColumnCount(2)
        self.result_tif.setHorizontalHeaderLabels(["Value", "Unit"])
        self.result_tif.setVerticalHeaderLabels(["Tif", "R_diff", "R_c", "P_0", "Slope_P", "Gamma"])
        self.result_tif.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_tif.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_tif.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        main_layout.addWidget(QLabel("Fitting result:"))
        main_layout.addWidget(self.result_table)
        # main_layout.addWidget(QLabel("Tif calculation:"))
        main_layout.addWidget(self.result_tif)

        self.update_iv_table()
        self.update_pv_table()

    def update_iv_table(self):
        self.iv_table.setRowCount(self.iv_range_spin.value())

    def update_pv_table(self):
        self.pv_table.setRowCount(self.pv_range_spin.value())

    def unit_scale(self, unit):
        return {"V": -1e3, "mV": 1, "A": -1e3, "mA": 1, "μA": 1e3, "W": 1, "mW": 1e3}.get(unit, 1)

    def load_data(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose a file",
            "",
            "DAT files (*.dat);;All files (*)"
        )
        if not path:
            return

        try:
            self.data = pd.read_csv(path, delimiter='\t')

            if self.data.shape[1] < 3:
                QMessageBox.warning(self, "Invalid File", "File must contain at least 3 columns.")
                self.data = None
                return

            file_name = os.path.basename(path)
            self.load_button.setText(file_name)
            self.setWindowTitle(f"Plot Generator - {file_name}")

            QMessageBox.information(self, "Success", f"File loaded: {file_name}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file: {e}")
            self.data = None

    def plot_data(self):
        if self.data is None:
            QMessageBox.warning(self, "No Data", "Please load a .dat file first.")
            return
        
        self.figure.clear()
        ax1 = self.figure.add_subplot(111)
        ax1.set_ylabel(self.data.columns[1], color='b')
        ax1.set_xlabel(self.data.columns[0])
        iv = ax1.plot(self.data.iloc[:, 0].values.flatten(), self.data.iloc[:, 1].values.flatten(), color='b', label='IV')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.grid(True)

        ax2 = ax1.twinx()
        ax2.set_ylabel(self.data.columns[2], color='r')
        pv = ax2.plot(self.data.iloc[:, 0].values.flatten(), self.data.iloc[:, 2].values.flatten(), color='r', label='PV')
        ax2.tick_params(axis='y', labelcolor='r')

        lines = iv + pv
        labels = [line.get_label() for line in lines]
        ax1.legend(lines, labels, loc=0)

        self.canvas.draw()

        # Save to file
        # self.figure.savefig(f"{os.path.basename(path)}_plot.png")
        # print(f"Saved: {os.path.basename(path)}_plot.png")


    def fit_data(self):
        if self.data is None:
            self.result_box.setPlainText("Please load data first.")
            return

        mode = self.mode_combo.currentText()
        if mode == "Automatically":
            QMessageBox.warning(self, "Mode Error", "Automatic mode is not implemented yet.")
            return

        elif mode == "Manually":
            method = self.method_combo.currentText()
            if method == "Ordinary Least Squares":
                # self.figure.clear()

                ax1 = self.figure.axes[0]
                ax2 = self.figure.axes[1]

                colors = ['g', 'm', 'c', 'y']
                seg_id = 1
                results = []

                # I-V
                for r in range(self.iv_table.rowCount()):
                    v_start = float(self.iv_table.item(r, 0).text())
                    v_end = float(self.iv_table.item(r, 1).text())
                    if v_start >= v_end:
                        QMessageBox.warning(self, "Invalid Range", f"Invalid range for segment {seg_id}: ({v_start}, {v_end})")
                        continue
                    seg = self.data[(self.data.iloc[:, 0].values.flatten() >= v_start) & (self.data.iloc[:, 0].values.flatten() <= v_end)]
                    if len(seg) < 2: continue
                    res = stats.linregress(seg[self.data.columns[0]], seg[self.data.columns[1]])
                    fit_I = res.slope * seg.iloc[:, 0].values.flatten() + res.intercept
                    ax1.plot(seg.iloc[:, 0], fit_I, color=colors[seg_id % 4], lw=6,
                        label=f"Seg {seg_id} dI/dV = {res.slope * self.scale_i / self.scale_v:.2g} {self.unit_i.currentText()}/{self.unit_v.currentText()}",
                        alpha = 0.6)
                    results.append([
                        f"Seg {seg_id}", 
                        f"({v_start},{v_end})", 
                        len(seg.iloc[:, 0]),
                        f"{res.slope * self.scale_i / self.scale_v:.4g}",
                        "",
                        f"{res.intercept * self.scale_i:.4g}", 
                        f"{res.stderr:.2e}",
                        f"{res.rvalue**2:.4f}"
                    ])
                    seg_id += 1

                # P-V
                for r in range(self.pv_table.rowCount()):
                    try:
                        v_start = float(self.pv_table.item(r, 0).text())
                        v_end = float(self.pv_table.item(r, 1).text())
                        seg = self.data[(self.data.iloc[:, 0] >= v_start) & (self.data.iloc[:, 0] <= v_end)]
                        if len(seg) < 2: continue
                        res = stats.linregress(seg[self.data.columns[0]], seg[self.data.columns[2]])
                        fit_P = res.slope * seg.iloc[:, 0] + res.intercept
                        ax2.plot(seg.iloc[:, 0], fit_P, color=colors[seg_id % 4], lw=6,
                                label=f"Seg {seg_id} dP/dV = {res.slope * self.scale_p / self.scale_v:.2e} {self.unit_p.currentText()}/{self.unit_v.currentText()}",
                                alpha=0.6)
                        results.append([
                            f"Seg {seg_id}", 
                            f"({v_start},{v_end})", 
                            len(seg.iloc[:, 0]),
                            "",
                            f"{res.slope * self.scale_p / self.scale_v:.4g}",
                            f"{res.intercept * self.scale_p:.4g}",
                            f"{res.stderr:.2e}",
                            f"{res.rvalue**2:.4f}"
                        ])
                        seg_id += 1
                    except: continue

                self.result_table.setRowCount(len(results))
                for row, items in enumerate(results):
                    for col, val in enumerate(items):
                        self.result_table.setItem(row, col, QTableWidgetItem(str(val)))
                ax1.legend(loc='upper left')
                ax2.legend(loc='upper right')
                self.canvas.draw()

                rdiff = 1 / float(results[2][3]) # results[2, 3] is the slope dI/dV for the third segment
                rc = 1 / float(results[1][3]) # results[1, 3] is the slope dI/dV for the second segment
                p0 = float(results[3][5]) # results[3, 5] is the intercept for the fourth segment
                slopep = float(results[3][4]) # results[3, 4] is the slope dP/dV for the fourth segment
                
                tn = (p0 / slopep) * (5.8 / 1) * (rdiff / (rdiff + rc))
                gamma = abs((50 - rdiff) / (50 + rdiff))

                tif = (tn - 4.2 * gamma**2) * (1 - gamma**2)

                for i in range(self.result_tif.rowCount()):
                    self.result_tif.setItem(i, 0, QTableWidgetItem(f"{[tif, rdiff, rc, p0, slopep, gamma][i]:.4g}"))
                    self.result_tif.setItem(i, 1, QTableWidgetItem(["K", "Ω", "Ω", "W", "Ωe-1", ""][i]))
                    # self.result_tif.setItem(i, 1, QTableWidgetItem(["K", 
                    #                                                 f"{self.unit_v.currentText()}/{self.unit_i.currentText()}", 
                    #                                                 f"{self.unit_v.currentText()}/{self.unit_i.currentText()}", 
                    #                                                 f"{self.unit_p.currentText()}", 
                    #                                                 f"{self.unit_i.currentText()}/{self.unit_v.currentText()}", 
                    #                                                 ""][i]))

        
            elif method == "Least Absolute Residual":
                self.result_box.setPlainText("Least Absolute Residual fitting is not implemented yet.")
                return
            
            elif method == "Bisquare":
                self.result_box.setPlainText("Bisquare fitting is not implemented yet.")
                return



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotApp()
    window.show()
    sys.exit(app.exec_())
