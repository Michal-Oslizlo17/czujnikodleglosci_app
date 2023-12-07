import serial
import matplotlib.pyplot as plt
from collections import deque
import time

# Parametry do konfiguracji portu szeregowego
COM_PORT = 'COM3'
BAUD_RATE = 9600

# Parametry do konfiguracji wykresu
MAX_POINTS = 50  # Maksymalna liczba punktów na wykresie
PLOT_DELAY = 100
PROGRAM_DELAY = 100

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

try:
    while True:
        # Odczyt danych z portu szeregowego
        odczyt = ser.readline().decode('utf-8').strip()

        # Przetwarzanie i aktualizacja wykresu
        try:
            odczyt_liczba = int(odczyt)
            print(odczyt_liczba)
            update_plot(odczyt_liczba)
            time.sleep(PROGRAM_DELAY)  # Dodaj opóźnienie (np. 0.1 sekundy)
        except ValueError as e:
            print(f"Błąd przetwarzania danych: {e}")

except KeyboardInterrupt:
    # Obsługa przerwania przez użytkownika (Ctrl+C)
    print("Przerwano przez użytkownika.")
finally:
    # Zamykanie portu szeregowego
    ser.close()
    print("Port szeregowy zamknięty.")
