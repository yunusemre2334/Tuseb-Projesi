from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import serial
import time 
import sys 
import numpy as np 
import smbus2 as smbus

satir_sayisi = 32
sutun_sayisi = 24

matris = [[0] * sutun_sayisi for _ in range(satir_sayisi)]

#sadece fsr değeri alınıyor diğer istenen değerler eklenebilir.
def request_data(slave_address, channel):
    bus = smbus.SMBus(channel)
    data = bus.read_i2c_block_data(slave_address, 0, 2)
    fsr_reading = (data[0] << 8) + data[1]
    return fsr_reading

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

        #fsr sayısını arttırmak için range kısmından 16 değeri arttırılabilir.
        self.label_list = [QLabel(f"FSR{i+1}") for i in range(0, 16)]
        
        for row in range(0, 4):
            for col in range(0, 4):
                grid_layout.addWidget(self.label_list[row * 4 + col], row, col)
            
        self.setLayout(grid_layout)

        self.arduino_thread.data_received.connect(self.veriyi_guncelle)
        
    def veriyi_guncelle(self, fsr_degeri):
        #surekli gelen her fsr değeri yazılıyor mu kontrol edilmeli test edilirken.
        for i in range(satir_sayisi):
            for j in range(sutun_sayisi):
                matris[i][j] = fsr_degeri
        #range(3) -> matrisin 24 byte lık her satırının ilk 3 elemanı fsr değeri olarak düşünüldü eğer farklı ise değiştirilebilir. 
        for index in range(32):
            fsr_degeri = int(''.join([str(matris[index][k]) for k in range(3)]))

            if len(str(fsr_degeri)) > 1:
                fsr_degeri = int(str(fsr_degeri)[:-1]) * 10
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
