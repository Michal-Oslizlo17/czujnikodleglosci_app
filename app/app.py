import serial
import matplotlib.pyplot as plt
from collections import deque
import time
import tkinter as tk
from tkinter import ttk

# Parametry do konfiguracji portu szeregowego
COM_PORT = 'COM3'
BAUD_RATE = 9600

# Parametry do konfiguracji wykresu
MAX_POINTS = 50  # Maksymalna liczba punktów na wykresie
PLOT_DELAY = 100
PROGRAM_DELAY = 100

# Globalne zmienne
is_running = False

# Inicjalizacja portu szeregowego
ser = serial.Serial(COM_PORT, BAUD_RATE)

# Inicjalizacja wykresu
plt.ion()  # Tryb interaktywny
fig, ax = plt.subplots()
line, = ax.plot([], [])  # Inicjalizacja pustego wykresu
data_buffer = deque(maxlen=MAX_POINTS)  # Bufor danych

# Funkcja do aktualizacji wykresu
def update_plot(new_data):
    data_buffer.append(new_data)
    line.set_xdata(range(len(data_buffer)))
    line.set_ydata(data_buffer)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(PLOT_DELAY)

# Funkcje obsługujące zdarzenia przycisków
def toggle_plotting():
    global is_running
    is_running = not is_running
    if is_running:
        start_button["state"] = "disabled"
        stop_button["state"] = "normal"
        root.after(0, start_plotting)
    else:
        start_button["state"] = "normal"
        stop_button["state"] = "disabled"

def start_plotting():
    if is_running:
        try:
            odczyt = ser.readline().decode('utf-8').strip()
            try:
                odczyt_liczba = int(odczyt)
                print(odczyt_liczba)
                update_plot(odczyt_liczba)
                root.after(PROGRAM_DELAY, start_plotting)
            except ValueError as e:
                print(f"Błąd przetwarzania danych: {e}")
        except KeyboardInterrupt:
            pass

# Tworzenie interfejsu graficznego
root = tk.Tk()
root.title("Serial Plotter")

start_button = ttk.Button(root, text="Start", command=toggle_plotting)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(root, text="Stop", command=toggle_plotting, state="disabled")
stop_button.pack(side=tk.LEFT, padx=10)

try:
    root.mainloop()
except KeyboardInterrupt:
    pass
finally:
    # Zamykanie portu szeregowego
    ser.close()
    print("Port szeregowy zamknięty.")
