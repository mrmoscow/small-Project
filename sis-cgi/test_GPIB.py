import sys
import pyvisa
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox

class GPIBApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPIB 裝置識別")
        self.setGeometry(100, 100, 300, 150)

        # 設計 UI 元件
        self.label = QLabel("按下按鈕讀取 GPIB 裝置 ID", self)
        self.button = QPushButton("讀取 ID", self)
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
            print("可用資源：", resources)

            if not resources:
                QMessageBox.warning(self, "錯誤", "找不到任何 VISA 裝置")
                return

            # 假設你使用 GPIB0::18::INSTR（請視實際情況修改）
            inst = rm.open_resource("GPIB0::18::INSTR")
            idn = inst.query("*IDN?")
            inst.close()

            self.label.setText(f"裝置 ID：\n{idn}")
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"讀取失敗：\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPIBApp()
    window.show()
    sys.exit(app.exec_())
