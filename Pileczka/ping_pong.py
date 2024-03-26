import pygame
import sys
import random

# Inicjalizacja Pygame
pygame.init()

# Definiowanie kolorów
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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
AI_SPEED = 4

# Ustawienie ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong AI")

# Zegar do kontroli fps
clock = pygame.time.Clock()

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
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle2_vel = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                paddle2_vel = PADDLE_SPEED
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2_vel = 0
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # AI dla lewej paletki
    if ball_pos[1] > paddle1_pos + PADDLE_HEIGHT // 2:
        paddle1_pos += AI_SPEED
    else:
        paddle1_pos -= AI_SPEED

    paddle2_pos += paddle2_vel

    # Zapobieganie wyjściu paletki poza ekran
    paddle1_pos = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle1_pos))
    paddle2_pos = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle2_pos))

    draw(screen)
    pygame.display.flip()
    clock.tick(60)
