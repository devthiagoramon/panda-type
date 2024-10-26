import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Digitação - Nível Difícil")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonte
FONT = pygame.font.SysFont("Arial", 32)

# Lista de palavras para praticar
words = ["paralelepípedo", "mecânico", "ornitorrinco", "presidiário", "austríaco"]
current_word = random.choice(words)  # Palavra atual a ser digitada
typed_word = ""  # Palavra digitada pelo jogador
score = 0  # Pontuação do jogador
vidas = 3  # Chances para errar

# Configuração do temporizador
time_limit = 10000
start_time = pygame.time.get_ticks()
progress_bar_width = 300

# Configuração das teclas (disposição simples)
keys = [
    "1234567890-=", "qwertyuiop[]", "asdfghjklç~", "zxcvbnm,.;/"
]
key_positions = {}  # Dicionário para armazenar a posição de cada tecla

# Função para desenhar o teclado
def draw_keyboard():
    x, y = 100, 300  # Posição inicial do teclado
    row_gap, key_gap = 60, 50
    next_char = current_word[len(typed_word)] if len(typed_word) < len(current_word) else ""

    for row in keys:
        for key in row:
            color = GREEN if key == next_char else WHITE
            pygame.draw.rect(win, color, (x, y, 40, 40))
            pygame.draw.rect(win, BLACK, (x, y, 40, 40), 2)  # Borda preta
            key_text = FONT.render(key, True, BLACK)
            win.blit(key_text, (x + 10, y + 5))
            key_positions[key] = (x, y)
            x += key_gap
        x = 100
        y += row_gap

    # Barra de espaço
    pygame.draw.rect(win, WHITE, (200, y, 300, 40))
    pygame.draw.rect(win, BLACK, (200, y, 300, 40), 2)
    space_text = FONT.render("Espaço", True, BLACK)
    win.blit(space_text, (325, y + 5))
    key_positions[" "] = (200, y)

# Função para exibir a palavra a ser digitada, o progresso do jogador e a pontuação
def draw_word_and_score():
    # Exibe a palavra atual
    word_text = FONT.render("Digite: " + current_word, True, BLACK)
    win.blit(word_text, (100, 200))

    # Exibe a palavra digitada pelo jogador
    typed_text = FONT.render("Digitado: " + typed_word, True, GREEN if typed_word == current_word else RED)
    win.blit(typed_text, (100, 250))

    # Exibe a pontuação
    score_text = FONT.render("Pontuação: " + str(score), True, BLACK)
    win.blit(score_text, (100, 150))

    # Exibe as vidas restantes
    vidas_text = FONT.render("Vidas: " + str(vidas), True, BLACK)
    win.blit(vidas_text, (100, 100))

# Função para desenhar a barra de progresso do temporizador
def draw_progress_bar():
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, time_limit - elapsed_time)
    progress_width = int((remaining_time / time_limit) * progress_bar_width)
    pygame.draw.rect(win, RED, (100, 50, progress_bar_width, 20))
    pygame.draw.rect(win, GREEN, (100, 50, progress_width, 20))

# Função para exibir a tela de vitória
def victory_condition():
    win.fill(WHITE)
    victory_text = FONT.render("Parabéns! Você venceu!", True, GREEN)
    score_text = FONT.render("Pontuação Final: " + str(score), True, BLACK)
    win.blit(victory_text, (250, 250))
    win.blit(score_text, (250, 300))
    pygame.display.flip()
    pygame.time.delay(3000)

# Função para exibir tela de derrota
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
        vidas -= 1
        typed_word = ""
        current_word = random.choice(words)
        start_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            else:
                typed_word += event.unicode

                if typed_word == current_word:
                    score += 1
                    typed_word = ""
                    current_word = random.choice(words)
                    start_time = pygame.time.get_ticks()

            if len(typed_word) == len(current_word):
                if typed_word == current_word:
                    score += 1
                else:
                    vidas -= 1
                typed_word = ""
                current_word = random.choice(words)

    pygame.display.flip()

pygame.quit()
