import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Digitação - Nível Difícil")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

FONT = pygame.font.SysFont("Arial", 32)

words = ["paralelepípedo", "mecânico", "ornitorrinco", "presidiário", "austríaco"]
current_word = random.choice(words)
typed_word = ""
score = 0
vidas = 3
error_made = False

time_limit = 10000
start_time = pygame.time.get_ticks()
progress_bar_width = 300

def draw_keyboard():
    x, y = 100, 300
    row_gap, key_gap = 60, 50
    keys = [
        "1234567890-=", "qwertyuiop[]", "asdfghjklç~", "zxcvbnm,.;/"
    ]

    next_letter = current_word[len(typed_word)] if len(typed_word) < len(current_word) else ""

    for row in keys:
        for key in row:
            color = GREEN if key == next_letter else WHITE
            pygame.draw.rect(win, color, (x, y, 40, 40))
            pygame.draw.rect(win, BLACK, (x, y, 40, 40), 2)
            key_text = FONT.render(key, True, BLACK)
            win.blit(key_text, (x + 10, y + 5))
            x += key_gap
        x = 100
        y += row_gap


    pygame.draw.rect(win, WHITE, (200, y, 300, 40))
    pygame.draw.rect(win, BLACK, (200, y, 300, 40), 2)
    space_text = FONT.render("Espaço", True, BLACK)
    win.blit(space_text, (325, y + 5))


    backspace_color = RED if error_made else WHITE
    pygame.draw.rect(win, backspace_color, (600, 300, 100, 40))
    pygame.draw.rect(win, BLACK, (600, 300, 100, 40), 2)
    backspace_text = FONT.render("Backspace", True, BLACK)
    win.blit(backspace_text, (610, 305))


    pygame.draw.rect(win, WHITE, (600, 360, 100, 40))
    pygame.draw.rect(win, BLACK, (600, 360, 100, 40), 2)
    enter_text = FONT.render("Enter", True, BLACK)
    win.blit(enter_text, (620, 365))

# Função para exibir a palavra e a pontuação
def draw_word_and_score():
    word_text = FONT.render("Digite: " + current_word, True, BLACK)
    win.blit(word_text, (100, 200))

    typed_text = FONT.render("Digitado: " + typed_word, True, GREEN if typed_word == current_word else RED)
    win.blit(typed_text, (100, 250))

    score_text = FONT.render("Pontuação: " + str(score), True, BLACK)
    win.blit(score_text, (100, 150))

    vidas_text = FONT.render("Vidas: " + str(vidas), True, BLACK)
    win.blit(vidas_text, (100, 100))


def draw_progress_bar():
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, time_limit - elapsed_time)
    progress_width = int((remaining_time / time_limit) * progress_bar_width)
    pygame.draw.rect(win, RED, (100, 50, progress_bar_width, 20))
    pygame.draw.rect(win, GREEN, (100, 50, progress_width, 20))


def victory_condition():
    win.fill(WHITE)
    victory_text = FONT.render("Parabéns! Você venceu!", True, GREEN)
    score_text = FONT.render("Pontuação Final: " + str(score), True, BLACK)
    win.blit(victory_text, (250, 250))
    win.blit(score_text, (250, 300))
    pygame.display.flip()
    pygame.time.delay(3000)


def defeat_condition():
    win.fill(WHITE)
    defeat_text = FONT.render("Você perdeu", True, RED)
    score_text = FONT.render("Pontuação Final: " + str(score), True, BLACK)
    win.blit(defeat_text, (250, 250))
    win.blit(score_text, (250, 300))
    pygame.display.flip()
    pygame.time.delay(3000)

# Loop principal do jogo
running = True
while running:
    win.fill(WHITE)
    draw_keyboard()
    draw_word_and_score()
    draw_progress_bar()

    if score >= 10:
        victory_condition()
        running = False
    elif vidas <= 0:
        defeat_condition()
        running = False

    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= time_limit:
        vidas = 0
        typed_word = ""
        current_word = random.choice(words)
        start_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
                error_made = False
            elif event.key == pygame.K_RETURN:
                if typed_word == current_word:
                    score += 1
                    typed_word = ""
                    current_word = random.choice(words)
                    start_time = pygame.time.get_ticks()
                    error_made = False
                else:
                    vidas -= 1
                    typed_word = ""
                    current_word = random.choice(words)
            else:
                char = event.unicode
                if char not in "´`~^¨":
                    typed_word += char
                    if typed_word[-1] != current_word[len(typed_word) - 1]:
                        error_made = True
                    else:
                        error_made = False


                if typed_word[-1] != current_word[len(typed_word) - 1]:
                    error_made = True
                else:
                    error_made = False

    pygame.display.flip()

pygame.quit()
