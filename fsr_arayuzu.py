from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import serial
import time 
import sys 
import numpy as np  # Ekledim, numpy kütüphanesini import ettim.

index_sozlugu = {"9": 1, "8": 0}

class ArduinoThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ArduinoThread, self).__init__(parent)
        self.serial_port = serial.Serial("COM3", 9600, timeout=1)

    def run(self):
        while True:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode('utf-8').strip()
                self.data_received.emit(data)
            time.sleep(0.1)

    def send_data(self, data):
        self.serial_port.write(data.encode('utf-8'))

class Yunus_Emre(QWidget):
    def __init__(self):
        super().__init__()

        self.arduino_thread = ArduinoThread()
        self.arduino_thread.start()

        self.setGeometry(200, 200, 1000, 800) 
        self.setWindowTitle("FSR Arayüzü")
        

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        self.label_list = [QLabel(f"FSR{i+1}") for i in range(0, 16)]
        
        for row in range(0, 4):
            for col in range(0, 4):
                grid_layout.addWidget(self.label_list[row * 4 + col], row, col)
            
        self.setLayout(grid_layout)

        self.arduino_thread.data_received.connect(self.veriyi_guncelle)
        
    def veriyi_guncelle(self):
        fsr_degeri = self.arduino_thread.serial_port.readline().decode("utf-8").strip()
        son_rakam = fsr_degeri[-1]

        if son_rakam in index_sozlugu:
            print(fsr_degeri[:-1])
            index = index_sozlugu[son_rakam]
            
            if len(fsr_degeri) > 1:
                fsr_degeri = int(fsr_degeri[:-1]) * 10
                scaled_value = int(np.interp(fsr_degeri, [0, 1023], [0, 255]))

                blue_value = 255 - scaled_value
                red_value = scaled_value
                color = QColor(red_value, 0, blue_value)
                self.label_list[index].setStyleSheet(f"background-color: {color.name()};")
                self.label_list[index].setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Yunus_Emre()
    window.show()
    sys.exit(app.exec_())
