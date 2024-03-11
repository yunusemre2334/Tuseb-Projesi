import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
import serial
import time

class ArduinoThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ArduinoThread, self).__init__(parent)
        self.serial_port = serial.Serial('COM3', 9600, timeout=1)

    def run(self):
        while True:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode('utf-8').strip()
                self.data_received.emit(data)
            time.sleep(0.1)

    def send_data(self, data):
        self.serial_port.write(data.encode('utf-8'))

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.arduino_thread = ArduinoThread()
        self.arduino_thread.start()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        send_button = QPushButton('Send to Arduino', self)
        send_button.clicked.connect(self.send_to_arduino)
        layout.addWidget(send_button)

        self.setLayout(layout)

        self.arduino_thread.data_received.connect(self.update_text)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Arduino Serial Communication')
        self.show()

    def send_to_arduino(self):
        data_to_send = "Hello Arduino!\n"
        self.arduino_thread.send_data(data_to_send)

    def update_text(self, data):
        self.text_edit.append(f"Received from Arduino: {data}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
