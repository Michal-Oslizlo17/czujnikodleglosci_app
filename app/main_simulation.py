import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import time
import random

# Parametry programu
PROGRAM_DELAY = 0.05  # Opóźnienie symulacji
UPDATE_INTERVAL = 1  # Czas w ms między automatycznymi aktualizacjami wykresu
MAX_X = 30
Y_RANGE = (0, 400)

# Globalne zmienne
is_running = False
data_queue = []

def read_serial():
    global is_running, data_queue
    while is_running:
        odczyt_liczba = random.randint(Y_RANGE[0], Y_RANGE[1])  # Generowanie losowej liczby
        print(odczyt_liczba)
        data_queue.append(odczyt_liczba)
        if len(data_queue) > MAX_X:
            data_queue.pop(0)
        time.sleep(PROGRAM_DELAY)

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
            ax.legend(["Dane symulowane"], loc="upper right")
            canvas.draw()
        root.after(UPDATE_INTERVAL, update_plot)  # Zaplanuj kolejną aktualizację

def on_closing():
    stop_reading()
    root.destroy()

# Tworzenie interfejsu użytkownika
root = tk.Tk()
root.title("Symulacja odczytu danych i wykres")

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
