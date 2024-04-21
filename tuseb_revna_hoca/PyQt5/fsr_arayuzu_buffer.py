from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time 
import sys 
import numpy as np 
import smbus2 as smbus


def convert_data(data):
    fsr_list = []
    for i in range(0,7):
        fsr_reading = (data[i] << 8) + data[i+1]
        fsr_list.append(fsr_reading)

    return fsr_list


class ArduinoThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self,channel=1, parent=None):
        super(ArduinoThread, self).__init__(parent)
        self.bus = smbus.SMBus(channel)
        self.buffer = [[i*j for j in range(1, 8)] for i in range(1, 32)]

    def run(self):
        while True:
            if self.bus.in_waiting:
                for addr in range(0,32):
                    data = self.bus.read_i2c_block_data(addr+8, 0, 24)
                    self.buffer[addr] = convert_data(data)
                    self.data_received.emit(self.buffer)
            time.sleep(0.1)


class Yunus_Emre(QWidget):
    def __init__(self):
        super().__init__()

        self.arduino_thread = ArduinoThread()
        self.arduino_thread.start()

        self.setGeometry(200, 200, 1000, 800) 
        self.setWindowTitle("FSR Arayüzü")
        

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        self.label_list = [QLabel(f"FSR{i+1}") for i in range(0, 32)]
        
        for row in range(0, 8):
            for col in range(0, 4):
                grid_layout.addWidget(self.label_list[row * 4 + col], row, col)
            
        self.setLayout(grid_layout)

        self.arduino_thread.data_received.connect(self.veriyi_guncelle)
        
    def veriyi_guncelle(self):
        fsr_list = self.arduino_thread.buffer
        for i in range(0,32):
            for j in range(0,7):
                for k in range(0,4):
                    fsr_degeri = fsr_list[i][k]
                
                    if fsr_degeri:
                        fsr_degeri = int(fsr_degeri) 
                        scaled_value = int(np.interp(fsr_degeri, [0, 1023], [0, 255]))

                        blue_value = 255 - scaled_value
                        red_value = scaled_value
                        color = QColor(red_value, 0, blue_value)
                        self.label_list[i * 4 + k].setStyleSheet(f"background-color: {color.name()};")
                        self.label_list[i * 4 + k].setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Yunus_Emre()
    window.show()
    sys.exit(app.exec_())
