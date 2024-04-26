import tkinter as tk
import numpy as np
import smbus2 as smbus

class CellData:
    def __init__(self):
        self.fsr_data = [0, 0, 0, 0]  # Başlangıç değeri

class Buffer:
    def __init__(self, num_cells):
        self.data_buffer = [CellData() for _ in range(num_cells)]

class ArduinoThread:
    def __init__(self, channel=1, num_cells=32):
        self.bus = smbus.SMBus(channel)
        self.buffer = Buffer(num_cells)

    def read_data(self):
        for cell_num in range(len(self.buffer.data_buffer)):
            # Burada her hücre için adres hesaplanmıştır. Arduinodalardaki adresler buna göre düzenlenmelidir.
            start_address = cell_num * 24  

            data = self.bus.read_i2c_block_data(20, start_address, 24)

            # her hücreden gelen ilk dört veri FSR değeri olduğu düşünülmüştür.
            cell_data = self.buffer.data_buffer[cell_num]
            cell_data.fsr_data = data[:4]  # İlk 4 byte FSR değerleri

class Yunus_Emre:
    def __init__(self):
        self.arduino_thread = ArduinoThread()
        self.root = tk.Tk()
        self.root.geometry("1000x800")
        self.root.title("FSR Arayüzü")

        self.label_list = []  

        for cell_num in range(32 * 4):  
            label = tk.Label(self.root, text=f"FSR{cell_num+1}")
            label.grid(row=cell_num // 4, column=cell_num % 4, padx=5, pady=5)
            self.label_list.append(label)

        self.veriyi_guncelle()  
        self.root.after(100, self.guncelle_dongusu)  
        self.root.mainloop()

    def guncelle_dongusu(self):
        self.arduino_thread.read_data()
        self.veriyi_guncelle()
        self.root.after(100, self.guncelle_dongusu) 

    def veriyi_guncelle(self):
        for cell_num in range(len(self.label_list)):
            fsr_degeri = self.arduino_thread.buffer.data_buffer[cell_num // 4].fsr_data[cell_num % 4]
            if fsr_degeri:
                fsr_degeri = int(fsr_degeri)
                scaled_value = int(np.interp(fsr_degeri, [0, 1023], [0, 255]))

                blue_value = 255 - scaled_value
                red_value = scaled_value
                color = f'#{red_value:02x}00{blue_value:02x}'
                self.label_list[cell_num].config(bg=color, bd=0, width=10, height=2, padx=5, pady=5)

if __name__ == "__main__":
    window = Yunus_Emre()
