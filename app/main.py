import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import serial  # Import biblioteki pyserial
import time

# Parametry programu
UPDATE_INTERVAL = 1  # Czas w ms między automatycznymi aktualizacjami wykresu
MAX_X = 30
Y_RANGE = (0, 150)

# Globalne zmienne
is_running = False
data_queue = []
ser = serial.Serial('COM4', 9600, timeout=1)  # Ustawienie portu szeregowego

def read_serial():
    global is_running, data_queue
    while is_running:
        if ser.in_waiting:
            odczyt = ser.readline().decode('utf-8').strip()
            #print(odczyt)
            try:
                odczyt_liczba = int(odczyt)
                data_queue.append(odczyt_liczba)
                if len(data_queue) > MAX_X:
                    data_queue.pop(0)
            except ValueError as e:
                print(f"Błąd przetwarzania danych: {e}")

def start_reading():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=read_serial, daemon=True).start()
        update_plot()

def stop_reading():
    global is_running
    is_running = False

def update_plot():
    if is_running:
        if data_queue:
            ax.clear()
            ax.plot(data_queue, '-o', linewidth=5)
            ax.set_ylim(Y_RANGE)
            ax.legend(["Dane z COM4"], loc="upper right")
            canvas.draw()
        root.after(UPDATE_INTERVAL, update_plot)  # Zaplanuj kolejną aktualizację

def on_closing():
    stop_reading()
    ser.close()  # Zamknij port szeregowy
    root.destroy()

# Tworzenie interfejsu użytkownika
root = tk.Tk()
root.title("Odczyt danych z portu COM4 i wykres")

# Konfiguracja wykresu
fig = Figure()
ax = fig.add_subplot(111)
ax.set_ylim(Y_RANGE)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Przyciski start/stop
start_button = ttk.Button(root, text="Start", command=start_reading)
start_button.pack(side=tk.LEFT, padx=5, pady=5)

stop_button = ttk.Button(root, text="Stop", command=stop_reading)
stop_button.pack(side=tk.LEFT, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
