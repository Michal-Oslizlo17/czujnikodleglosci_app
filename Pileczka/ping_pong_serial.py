import pygame
import sys
import random
import serial
from colorama import Style, Fore, init

# Inicjalizacja colorama
init(autoreset=True)

# Inicjalizacja Pygame
pygame.init()

# Definiowanie kolorów
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Ustawienia początkowe
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
BALL_SIZE = 20
PADDLE_WIDTH = 8
PADDLE_HEIGHT = 80

# Ustawienia prędkości
BALL_SPEED_X = 3
BALL_SPEED_Y = 3
PADDLE_SPEED = 8

# Ustawienia AI
AI_SPEED = 3.25       # Default: 3.25
MISTAKE_CHANCE = 10   # Chance of AI making a mistake (10%)

show_exclamation = False
exclamation_timer = 120

def draw_exclamation():
    global show_exclamation, exclamation_timer
    if show_exclamation:
        # Ładowanie czcionki
        font_size = 500
        font = pygame.font.SysFont('Consolas', font_size)

        text = font.render('!', True, ORANGE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

        font_size = 50
        font = pygame.font.SysFont('Consolas', font_size)

        text = font.render('[Wartość poza zakresem]', True, ORANGE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250))
        screen.blit(text, text_rect)

        exclamation_timer -= 1
        if exclamation_timer <= 0:
            show_exclamation = False

# Ustawienie ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong AI")

# Zegar do kontroli fps
clock = pygame.time.Clock()

# Inicjalizacja połączenia z portem szeregowym
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
except serial.SerialException as e:
    print(f"{Fore.RED}Nie można połączyć z portem COM3. Upewnij się, że urządzenie jest podłączone i spróbuj ponownie.{Style.RESET_ALL}")
    print(f"{Fore.RED}Error code: {e}{Style.RESET_ALL}")
    sys.exit()

def ball_init():
    global ball_pos, ball_vel
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    ball_vel = [random.choice((-1, 1)) * BALL_SPEED_X, random.choice((-1, 1)) * BALL_SPEED_Y]

def init():
    global paddle1_pos, paddle2_pos, paddle2_vel, score1, score2
    paddle1_pos = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
    paddle2_pos = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
    paddle2_vel = 0  # Inicjalizacja prędkości paletki gracza
    score1 = 0
    score2 = 0
    ball_init()

def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, score1, score2

    canvas.fill(BLACK)
    pygame.draw.rect(canvas, WHITE, pygame.Rect(SCREEN_WIDTH // 2 - 1, 0, 2, SCREEN_HEIGHT))
    pygame.draw.ellipse(canvas, WHITE, pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))
    pygame.draw.rect(canvas, GREEN, pygame.Rect(0, paddle1_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(canvas, GREEN, pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, paddle2_pos, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Ruch piłki
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Kolizja z górnym i dolnym brzegiem
    if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - BALL_SIZE:
        ball_vel[1] = -ball_vel[1]

    # Punkt dla gracza 1
    if ball_pos[0] <= PADDLE_WIDTH:
        if paddle1_pos <= ball_pos[1] <= paddle1_pos + PADDLE_HEIGHT:
            ball_vel[0] = -ball_vel[0]
        else:
            score2 += 1
            ball_init()

    # Punkt dla gracza 2
    if ball_pos[0] >= SCREEN_WIDTH - PADDLE_WIDTH - BALL_SIZE:
        if paddle2_pos <= ball_pos[1] <= paddle2_pos + PADDLE_HEIGHT:
            ball_vel[0] = -ball_vel[0]
        else:
            score1 += 1
            ball_init()

    # Wyświetlanie wyników
    font = pygame.font.SysFont("comicsansms", 24)
    score_text = font.render(f"{score1}  {score2}", True, WHITE)
    canvas.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 20))

    pygame.draw.circle(canvas, RED, (int(ball_pos[0] + BALL_SIZE // 2), int(ball_pos[1] + BALL_SIZE // 2)), BALL_SIZE // 2)

# Inicjalizacja gry
init()

# Główna pętla gry
while True:
    # Odczyt danych z portu szeregowego i aktualizacja pozycji paletki
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        if line.isdigit():
            newPos = int(line)
            # Sprawdzenie, czy wartość jest w oczekiwanym zakresie
            if 30 <= newPos <= 90:
                # Zakładamy, że zakres wartości to 0030 - 0090
                newPos = int((newPos - 30) * (SCREEN_HEIGHT - PADDLE_HEIGHT) / (90 - 30))
                paddle2_pos = newPos
                print(f"{Fore.GREEN}[OK]{Style.RESET_ALL}   Otrzymana wartość jest poprawna, value: {newPos}")
                show_exclamation = False
            else:
                print(f"{Fore.LIGHTYELLOW_EX}[WARN]{Style.RESET_ALL} Otrzymana wartość jest poza zakresem 0030 - 0090, value: {newPos}")
                show_exclamation = True
                

    # AI dla lewej paletki
    # Decide randomly if AI will make a mistake this move
    if random.randint(1, 100) <= MISTAKE_CHANCE:
        mistake_modifier = -1  # Invert direction for a mistake
        print(f"{Fore.GREEN}AI popełniło sztuczny błąd.{Style.RESET_ALL}")
    else:
        mistake_modifier = 1  # Keep direction correct if no mistake
        print(f"{Fore.GREEN}AI zagrało normalnie.{Style.RESET_ALL}")
    
    # Ruch AI
    if ball_pos[1] > paddle1_pos + PADDLE_HEIGHT // 2:
        paddle1_pos += AI_SPEED * mistake_modifier  # Move up or mistake down
    else:
        paddle1_pos -= AI_SPEED * mistake_modifier  # Move down or mistake up

    paddle2_pos += paddle2_vel

    # Zapobieganie wyjściu paletki poza ekran
    paddle1_pos = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle1_pos))
    paddle2_pos = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle2_pos))

    draw(screen)
    draw_exclamation()
    pygame.display.flip()
    clock.tick(60)

    print("-"*100)