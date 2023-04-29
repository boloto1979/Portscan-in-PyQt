import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QPlainTextEdit, QFrame
from PyQt5.QtCore import Qt
import concurrent.futures
import socket
import subprocess

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

        self.line = QFrame(self)
        self.line.setGeometry(10, 40, 380, 2)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.timeout_label = QLabel("Timeout (seconds):", self)
        self.timeout_label.move(10, 60)

        self.timeout_input = QLineEdit(self)
        self.timeout_input.move(150, 60)

        self.result_label = QLabel("Result:", self)
        self.result_label.move(10, 90)

        self.result_output = QPlainTextEdit(self)
        self.result_output.move(10, 110)
        self.result_output.setReadOnly(True)

        self.scan_button = QPushButton("Scan", self)
        self.scan_button.move(300, 250)
        self.scan_button.clicked.connect(self.start_scan)

        self.setGeometry(300, 300, 400, 300)
        self.show()

    def start_scan(self):
        host = self.host_input.text()
        timeout = float(self.timeout_input.text())
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 587, 993, 995]

        self.result_output.clear()

        asyncio.run(self.scan_async(host, ports, timeout))

    async def scan_async(self, host, ports, timeout):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, self.scan_port, host, port, timeout)
                for port in ports
            ]
            port_results = await asyncio.gather(*tasks)

        ping_result = await self.ping(host)

        self.process_results(ports, port_results, ping_result)

    def scan_port(self, host, port, timeout):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result

    async def ping(self, host):
        try:
            process = await asyncio.create_subprocess_shell(
                f"ping -c 1 {host}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            _, _ = await process.communicate()
            return process.returncode == 0
        except Exception:
            return False

    def process_results(self, ports, port_results, ping_result):
        for port, result in zip(ports, port_results):
            if result == 0:
                self.result_output.appendPlainText(f"Port {port} is open")
            else:
                self.result_output.appendPlainText(f"Port {port} is closed")

        if ping_result:
            self.result_output.appendPlainText("Ping successful")
        else:
            self.result_output.appendPlainText("Ping failed")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PortScan()
    sys.exit(app.exec_())
