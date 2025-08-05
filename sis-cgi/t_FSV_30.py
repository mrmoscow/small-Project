import sys
import pyvisa
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)

class GPIBApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSV-30 Marker 讀取")
        self.setGeometry(100, 100, 400, 400)

        # 標題
        self.label = QLabel("按下按鈕讀取 FSV 上的 Marker 頻率與功率", self)

        # 按鈕
        self.button = QPushButton("讀取 Marker", self)
        self.button.clicked.connect(self.read_markers)

        # 表格：9 行 2 欄
        self.table = QTableWidget()
        self.table.setRowCount(9)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Frequency (GHz)", "Power (dBm)"])

        # 排版
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def read_markers(self):
        try:
            rm = pyvisa.ResourceManager()
            inst = rm.open_resource("GPIB0::18::INSTR")

            inst.timeout = 2000
            inst.write_termination = '\n'
            inst.read_termination = '\n'

            for i in range(1, 10):  # M1 ~ M9
                try:
                    freq = float(inst.query(f"CALC:MARK{i}:X?"))
                    power = float(inst.query(f"CALC:MARK{i}:Y?"))
                    freq_ghz = freq / 1e9

                    self.table.setItem(i - 1, 0, QTableWidgetItem(f"{freq_ghz:.3f}"))
                    self.table.setItem(i - 1, 1, QTableWidgetItem(f"{power:.2f}"))
                except Exception as e:
                    self.table.setItem(i - 1, 0, QTableWidgetItem("Error"))
                    self.table.setItem(i - 1, 1, QTableWidgetItem(str(e)))

            inst.close()

        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"GPIB 通訊失敗：\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPIBApp()
    window.show()
    sys.exit(app.exec_())
