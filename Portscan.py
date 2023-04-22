import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QPlainTextEdit
from PyQt5.QtCore import Qt
import socket

class PortScan(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Port Scan")

        self.host_label = QLabel("IP Address:", self)
        self.host_label.move(10, 10)

        self.host_input = QLineEdit(self)
        self.host_input.move(100, 10)

        self.result_label = QLabel("Result:", self)
        self.result_label.move(10, 50)

        self.result_output = QPlainTextEdit(self)
        self.result_output.move(10, 70)
        self.result_output.setReadOnly(True)

        self.scan_button = QPushButton("Scan", self)
        self.scan_button.move(10, 250)
        self.scan_button.clicked.connect(self.start_scan)

        self.setGeometry(300, 300, 400, 300)
        self.show()

    def start_scan(self):
        host = self.host_input.text()
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 587, 993, 995]

        self.result_output.clear()

        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                self.result_output.appendPlainText("Port {} is open".format(port))
            else:
                self.result_output.appendPlainText("Port {} is closed".format(port))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PortScan()
    sys.exit(app.exec_())
