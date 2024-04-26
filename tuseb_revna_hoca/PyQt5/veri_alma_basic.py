import tkinter as tk
import numpy as np
import smbus2 as smbus
import time

def convert_data(data):
    fsr_list = []
    for i in range(0,3):
        fsr_reading = (data[i * 2] << 8) + data[i * 2 + 1]
        fsr_list.append(fsr_reading)

    return fsr_list

class ArduinoThread:
    def __init__(self, channel=1):
        self.bus = smbus.SMBus(channel)
        self.data = [0, 0, 0]  # Başlangıç değeri

    def read_data(self):
        self.data = self.bus.read_i2c_block_data(20, 0, 6)
        self.data = convert_data(self.data)
        print(self.data)

class Yunus_Emre:
    def __init__(self):
        self.arduino_thread = ArduinoThread()
        self.root = tk.Tk()
        self.root.geometry("1000x800")
        self.root.title("FSR Arayüzü")

        self.label_list = [tk.Label(self.root, text=f"FSR{i+1}") for i in range(0, 2)]
        
        for row in range(0, 1):
            for col in range(0, 2):
                self.label_list[row * 2 + col].grid(row=row, column=col, padx=5, pady=5)
            
        self.veriyi_guncelle()  
        self.root.after(100, self.guncelle_loop)  
        self.root.mainloop()

    def guncelle_loop(self):
        self.arduino_thread.read_data()
        self.veriyi_guncelle()
        self.root.after(100, self.guncelle_loop)  

    def veriyi_guncelle(self):
        fsr_list = self.arduino_thread.data
        for i in range(0, 2):
            fsr_degeri = fsr_list[i]
            if fsr_degeri:
                fsr_degeri = int(fsr_degeri) 
                scaled_value = int(np.interp(fsr_degeri, [0, 1023], [0, 255]))

                blue_value = 255 - scaled_value
                red_value = scaled_value
                color = f'#{red_value:02x}00{blue_value:02x}'
                self.label_list[i].config(bg=color, bd=0, width=10, height=2, padx=5, pady=5)

if __name__ == "__main__":
    window = Yunus_Emre()
