import pygame
import sys
import serial

# Inicjalizacja pygame
pygame.init()

# Ustawienia ekranu
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Kolory
black = (0, 0, 0)
white = (255, 255, 255)

# Ustawienia piłeczki
ball_pos = [screen_width // 2, screen_height - 15]
ball_radius = 15
ball_speed = [0, -15]  # x, y - prędkość i kierunek

# Wysokość, do której ma odbić się piłka (inicjalnie na dole ekranu)
target_height = screen_height - ball_radius

# Ustawienia portu szeregowego
port = "COM3"
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print("Połączono z portem: ", ser.portstr)
except serial.SerialException:
    print("Nie można połączyć z portem ", port)
    sys.exit()

def move_ball():
    global ball_pos, ball_speed, target_height

    next_pos = ball_pos[1] + ball_speed[1]

    # Odbicie od dolnej krawędzi (piłka porusza się w dół)
    if next_pos + ball_radius > screen_height and ball_speed[1] > 0:
        ball_speed[1] = -ball_speed[1]
        
    # Odbicie od ustalonej wysokości (piłka porusza się w górę)
    elif next_pos - ball_radius < target_height and ball_speed[1] < 0:
        ball_speed[1] = -ball_speed[1]

    # Aktualizacja pozycji piłeczki
    ball_pos[1] += ball_speed[1]

# Pętla gry
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Odczyt danych z portu szeregowego
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if line.isdigit():
            simulated_value = int(line)
            target_height = screen_height - (simulated_value * screen_height // 125) - ball_radius

    move_ball()

    # Rysowanie
    screen.fill(black)
    pygame.draw.circle(screen, white, ball_pos, ball_radius)
    pygame.display.flip()

    clock.tick(30)  # Ustawienie FPS na 30

# Zamykanie
pygame.quit()
ser.close()
