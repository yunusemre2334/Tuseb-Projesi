from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import serial
import numpy as np

ser = serial.Serial('COM3', 9600) 

index_sozlugu = {"9": 1, "8": 0}

class Yunus_Emre(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 1000, 800) 
        self.setWindowTitle("FSR Arayüzü")
        self.setWindowIcon(QIcon("barkan.jpg"))

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        self.label_list = [QLabel(f"FSR{i+1}") for i in range(0,16)]
        
        for row in range(0,4):
            for col in range(0,4):
                grid_layout.addWidget(self.label_list[row * 4 + col ], row, col)
            
       
        self.setLayout(grid_layout)

        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.veriyi_guncelle)
        self.timer.start(100)
    
    def veriyi_guncelle(self):
        
        # fsr_degeri = ser.readline().decode().strip()
        fsr_degeri = ser.readline().decode("utf-8").strip()
        son_rakam = fsr_degeri[-1]
        if son_rakam in  index_sozlugu:
            #print(fsr_degeri)
            print(fsr_degeri[:-1])
            index = index_sozlugu[son_rakam]
            if len(fsr_degeri) > 1:
                fsr_degeri = int(fsr_degeri[:-1]) * 10

                # scaled_value = int((deger/1023) * 255)
                scaled_value = int(np.interp(fsr_degeri, [0, 1023], [0, 255]))

                blue_value = 255 - scaled_value
                red_value = scaled_value
                color = QColor(red_value, 0 , blue_value)
                self.label_list[index].setStyleSheet(f"background-color: {color.name()};")
                self.label_list[index].setAlignment(Qt.AlignCenter)
        
                    
if __name__ == "__main__":
    yunus_emre = QApplication([])
    pencere = Yunus_Emre()
    pencere.show()
    yunus_emre.exec_()
