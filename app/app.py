import serial
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Parametry do konfiguracji portu szeregowego
COM_PORT = 'COM3'
BAUD_RATE = 9600

# Parametry do konfiguracji wykresu
MAX_POINTS = 50  # Maksymalna liczba punktów na wykresie
PROGRAM_DELAY = 0

# Stała wartość osi y
Y_AXIS_CONSTANT = 200

# Globalne zmienne
is_running = False
received_value = 0

# Inicjalizacja portu szeregowego
ser = serial.Serial(COM_PORT, BAUD_RATE)

# Inicjalizacja wykresu Plotly
fig = go.FigureWidget()
fig.add_scatter(y=[None] * MAX_POINTS, mode='lines')

# Ustawienia wykresu
fig.update_yaxes(range=[0, Y_AXIS_CONSTANT])
fig.update_layout(title='Serial Plotter', xaxis_title='Index', yaxis_title='Value')

# Tekst z wartością odczytaną z portu szeregowego
value_text = fig.add_annotation(text=f"Received value: {received_value}", xref='paper', yref='paper',
                                x=0.95, y=0.95, showarrow=False, font=dict(size=12))

# Funkcja do aktualizacji wykresu
def update_plot(new_data):
    global received_value
    received_value = new_data
    with fig.batch_update():
        fig.data[0].y = fig.data[0].y[-MAX_POINTS:] + [new_data]
        fig.update_yaxes(range=[0, Y_AXIS_CONSTANT])
        value_text.update(text=f"Received value: {received_value}")

# Funkcja do odczytu danych z portu szeregowego w osobnym wątku
def read_serial():
    global is_running
    while is_running:
        try:
            odczyt = ser.readline().decode('utf-8').strip()
            print(odczyt)
            try:
                odczyt_liczba = int(odczyt)
                update_plot(odczyt_liczba)
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

canvas = fig.show()
canvas_widget = fig.write_html('plot.html', auto_open=False)

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
