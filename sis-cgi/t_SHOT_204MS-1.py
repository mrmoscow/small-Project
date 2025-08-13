import sys
import pyvisa
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox

class GPIBApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPIB Device Search")
        self.setGeometry(100, 100, 300, 150)

        # 設計 UI 元件
        self.label = QLabel("Botton for GPIB ID", self)
        self.button = QPushButton("Reading ID", self)
        self.button.clicked.connect(self.query_idn)

        # 垂直排列
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def query_idn(self):
        try:
            rm = pyvisa.ResourceManager()
            resources = rm.list_resources()
            print("Available deivce：", resources)

            if not resources:
                QMessageBox.warning(self, "Error", "Can not find any VISA device")
                return

            inst = rm.open_resource("GPIB0::8::INSTR")
            idn = inst.query("*IDN?")
            inst.close()

            self.label.setText(f"Deivce ID：\n{idn}")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"讀取失敗：\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPIBApp()
    window.show()
    sys.exit(app.exec_())
