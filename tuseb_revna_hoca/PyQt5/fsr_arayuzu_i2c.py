from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time 
import sys 
import numpy as np 
import smbus2 as smbus


#buraya adres degerleri fsr lerin indexlerine göre arduino ide üzerinde 0 dan 32 ye belirlenmeli ardından gönderilmeli
def verileri_donustur(veri):
    
    fsr_reading = (veri[0] << 8) + veri[1] 
    adresim = veri[2]
    
    return adresim, fsr_reading

class ArduinoThread(QThread):
    data_received = pyqtSignal(tuple)

    def __init__(self,channel=1, parent=None):
        super(ArduinoThread, self).__init__(parent)
        self.bus = smbus.SMBus(channel)
        

    def run(self):
        while True:
            if self.bus.in_waiting:
                for addr in range(0,32):
                    self.gelen_veri = self.bus.read_i2c_block_data(addr, 0, 3)
                    self.data_received.emit(tuple(self.gelen_veri))
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
        adres, fsr_degeri = verileri_donustur(self.arduino_thread.gelen_veri)
                
        if fsr_degeri:
            fsr_degeri = int(fsr_degeri) 
            scaled_value = int(np.interp(fsr_degeri, [0, 1023], [0, 255]))

            blue_value = 255 - scaled_value
            red_value = scaled_value
            color = QColor(red_value, 0, blue_value)
            self.label_list[adres].setStyleSheet(f"background-color: {color.name()};")
            self.label_list[adres].setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Yunus_Emre()
    window.show()
    sys.exit(app.exec_())
