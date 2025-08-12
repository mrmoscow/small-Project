import sys
import os
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFileDialog, QSpinBox, QMessageBox, QTableWidget,
    QGroupBox, QSizePolicy, QGridLayout, QHeaderView, QTableWidgetItem
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

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        left_layout = QVBoxLayout()
        topleft_layout = QHBoxLayout()
        self.load_1_button = QPushButton("Choose a y-factor file(.dat)")
        #self.load_2_button = QPushButton("Choose Spectrum Hot file (.??)")
        #self.load_3_button = QPushButton("Choose Spectrum Colt file (.??)")

        self.load_1_button.clicked.connect(self.load_data)

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_data)

        #save_button = QPushButton("Save")
        #save_button.clicked.connect(self.save)

        topleft_layout.addWidget(self.load_1_button, 6)
        topleft_layout.addWidget(self.plot_button, 4)
        #topleft_layout.addWidget(save_button, 1)
        left_layout.addLayout(topleft_layout)

        # Middle: plot and control
        center_layout = QHBoxLayout()
        main_layout.addLayout(center_layout)

        # Left: plot area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(self.canvas)
        center_layout.addLayout(left_layout, 3)

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
            # self.data.columns = self.data.columns.str.strip()
            self.data.columns = self.data.columns.str.replace(' ', '_')
            self.data.columns = self.data.columns.str.replace('(', '_')
            self.data.columns = self.data.columns.str.replace(')', '')

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
        iv = ax1.plot(self.data.iloc[:, 0], self.data.iloc[:, 1], color='b', label='IV')
        ax1.tick_params(axis='y', labelcolor='b')
        ax1.grid(True)

        ax2 = ax1.twinx()
        ax2.set_ylabel(self.data.columns[2], color='r')
        pv = ax2.plot(self.data.iloc[:, 0], self.data.iloc[:, 2], color='r', label='PV')
        ax2.tick_params(axis='y', labelcolor='r')

        lines = iv + pv
        labels = [line.get_label() for line in lines]
        ax1.legend(lines, labels, loc=0)

        self.canvas.draw()

        # Save to file
        # self.figure.savefig(f"{os.path.basename(path)}_plot.png")
        # print(f"Saved: {os.path.basename(path)}_plot.png")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotApp()
    window.show()
    sys.exit(app.exec_())
