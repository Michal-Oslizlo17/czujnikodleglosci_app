import serial
import matplotlib.pyplot as plt
from collections import deque
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

# Parametry do konfiguracji portu szeregowego
COM_PORT = 'COM3'
BAUD_RATE = 9600

# Parametry do konfiguracji wykresu
MAX_POINTS = 50  # Maksymalna liczba punktów na wykresie
PLOT_DELAY = 0.01
PROGRAM_DELAY = 0.01

# Stała wartość osi y
Y_AXIS_CONSTANT = 200

# Globalne zmienne
is_running = False
received_value = 0

# Inicjalizacja portu szeregowego
ser = serial.Serial(COM_PORT, BAUD_RATE)

# Inicjalizacja wykresu
fig, ax = plt.subplots()
line, = ax.plot([], [])  # Inicjalizacja pustego wykresu
data_buffer = deque(maxlen=MAX_POINTS)  # Bufor danych

# Ustawienie osi y na stałą wartość 200
ax.set_ylim([0, Y_AXIS_CONSTANT])

# Tekst z wartością odczytaną z portu szeregowego
value_text = ax.text(0.95, 0.95, "", transform=ax.transAxes, ha="right", va="top", fontsize=12)

# Funkcja do aktualizacji wykresu
def update_plot(new_data, line):
    global received_value
    received_value = new_data
    data_buffer.append(new_data)
    line.set_xdata(range(len(data_buffer)))
    line.set_ydata(data_buffer)
    ax.relim()
    ax.autoscale_view()
    
    # Ustawienie osi y na stałą wartość 200
    ax.set_ylim([0, Y_AXIS_CONSTANT])
    
    value_text.set_text(f"Received value: {received_value}")

# Funkcja do odczytu danych z portu szeregowego w osobnym wątku
def read_serial():
    global is_running
    while is_running:
        try:
            odczyt = ser.readline().decode('utf-8').strip()
            print(odczyt)
            try:
                odczyt_liczba = int(odczyt)
                update_plot(odczyt_liczba, line)
                time.sleep(PROGRAM_DELAY)
            except ValueError as e:
                print(f"Błąd przetwarzania danych: {e}")
        except KeyboardInterrupt:
            pass

# Funkcje obsługujące zdarzenia przycisków
def toggle_plotting():
    global is_running
    is_running = not is_running
    if is_running:
        start_button["state"] = "disabled"
        stop_button["state"] = "normal"
        # Uruchomienie wątku odczytu danych z portu szeregowego
        thread = Thread(target=read_serial)
        thread.start()
    else:
        start_button["state"] = "normal"
        stop_button["state"] = "disabled"

# Tworzenie interfejsu graficznego
root = tk.Tk()
root.title("Serial Plotter")

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

start_button = ttk.Button(root, text="Start", command=toggle_plotting)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(root, text="Stop", command=toggle_plotting, state="disabled")
stop_button.pack(side=tk.LEFT, padx=10)

# Funkcja animacji dla aktualizacji wykresu
def animate(frame):
    line.set_xdata(range(len(data_buffer)))
    line.set_ydata(data_buffer)
    ax.relim()
    ax.autoscale_view()
    
    # Ustawienie osi y na stałą wartość 200
    ax.set_ylim([0, Y_AXIS_CONSTANT])
    
    value_text.set_text(f"Received value: {received_value}")

ani = FuncAnimation(fig, animate, frames=None, interval=PLOT_DELAY)

try:
    root.mainloop()
except KeyboardInterrupt:
    pass
finally:
    # Zamykanie portu szeregowego
    ser.close()
    print("Port szeregowy zamknięty.")
