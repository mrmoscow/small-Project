import sys
import pyvisa
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox,
    QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
    QTextEdit,QLabel
)

class GPIBApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPIB Precision Platform")
        self.setGeometry(100, 100, 500, 400)

        # Label
        self.label = QLabel("GPIB ID 未連線")

        # Buttons
        self.home_button = QPushButton("Home Load")
        self.hot_button = QPushButton("Hot Load")
        self.cold_button = QPushButton("Cold Load")

        self.home_button.clicked.connect(self.handle_home)
        self.hot_button.clicked.connect(self.handle_hot)
        self.cold_button.clicked.connect(self.handle_cold)

        # Response Windows
        self.output1 = QTextEdit()
        self.output2 = QTextEdit()
        self.output1.setReadOnly(True)
        self.output2.setReadOnly(True)

        # Layouts
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.home_button)
        h_layout.addWidget(self.hot_button)
        h_layout.addWidget(self.cold_button)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(h_layout)
        layout.addWidget(QLabel("Response 1:"))
        layout.addWidget(self.output1)
        layout.addWidget(QLabel("Response 2:"))
        layout.addWidget(self.output2)

        self.setLayout(layout)

        # Initialize GPIB
        try:
            self.rm = pyvisa.ResourceManager()
            self.inst = self.rm.open_resource("GPIB0::8::INSTR")
            idn = self.inst.query("*IDN?")
            self.label.setText(f"Connected: {idn.strip()}")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"GPIB 初始化失敗：\n{e}")
            self.inst = None

    def handle_home(self):
        if not self.inst:
            self.output1.setText("未連接 GPIB 裝置")
            return
        try:
            self.output1.setText("Sending: H:W(For Move to Home Posisiton)")
            self.inst.write("H:W")

            response1 = self.inst.read()
            self.output1.append(f"Received 1: {response1}")

            self.output2.setText("等待第2筆資料...")
            #time.sleep(2)  # 可調整等待時間

            response2 = self.inst.read()
            self.output2.setText(f"Received 2: {response2}")

        except Exception as e:
            self.output1.setText(f"錯誤：{str(e)}")

    def handle_hot(self):
        if not self.inst:
            self.output1.setText("未連接 GPIB 裝置")
            return
        try:
            self.output1.setText("Sending: M:1-P70000 and G")
            self.inst.write("M:1-P70000")
            response1 = self.inst.read()
            self.output1.append(f"Received 1: {response1}")
            self.inst.write("G:")
            response1 = self.inst.read()
            self.output1.append(f"Received 1: {response1}")

            self.output2.setText("等待第2筆資料...")
            #time.sleep(1)  # 可調整等待時間
            response2 = self.inst.read()
            self.output2.setText(f"Received 2: {response2}")

        except Exception as e:
            self.output1.setText(f"錯誤：{str(e)}")
            self.output2.clear()


    def handle_cold(self):
        if not self.inst:
            self.output1.setText("未連接 GPIB 裝置")
            return
        try:
            self.output1.setText("Sending: M:1+P70000 and G")
            self.inst.write("M:1+P70000")
            response1 = self.inst.read()
            self.output1.append(f"Received 1: {response1}")
            self.inst.write("G:")
            response1 = self.inst.read()
            self.output1.append(f"Received 1: {response1}")


            self.output2.setText("等待第2筆資料...")
            #time.sleep(1)  # 可調整等待時間

            response2 = self.inst.read()
            self.output2.setText(f"Received 2: {response2}")

        except Exception as e:
            self.output1.setText(f"錯誤：{str(e)}")
            self.output2.clear()

    def closeEvent(self, event):
        if hasattr(self, "inst") and self.inst:
            self.inst.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPIBApp()
    window.show()
    sys.exit(app.exec_())

