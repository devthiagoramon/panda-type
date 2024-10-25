import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da janela
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Digitação - Nível Fácil")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonte
FONT = pygame.font.SysFont("Arial", 32)

# Lista de palavras para praticar
words = ["exemplo", "palavra", "digitação", "fácil", "programar"]
current_word = random.choice(words)  # Palavra atual a ser digitada
typed_word = ""  # Palavra digitada pelo jogador

# Configuração das teclas (disposição simples)
keys = [
    "1234567890-=", "qwertyuiop[]", "asdfghjklç~", "zxcvbnm,.;/"
]
key_positions = {}  # Dicionário para armazenar a posição de cada tecla

# Função para desenhar o teclado
def draw_keyboard():
    x, y = 100, 300  # Posição inicial do teclado
    row_gap, key_gap = 60, 50

    for row in keys:
        for key in row:
            # Define a cor com base no dedo sugerido
            color = BLUE  # Ajuste de cores conforme o dedo a ser usado
            pygame.draw.rect(win, color, (x, y, 40, 40))
            key_text = FONT.render(key, True, BLACK)
            win.blit(key_text, (x + 10, y + 5))
            key_positions[key] = (x, y)
            x += key_gap
        x = 100  # Reinicia a posição x para a próxima linha
        y += row_gap

    # Barra de espaço
    pygame.draw.rect(win, BLUE, (200, y, 300, 40))
    space_text = FONT.render("Espaço", True, BLACK)
    win.blit(space_text, (325, y + 5))
    key_positions[" "] = (200, y)  # Adiciona a posição da barra de espaço

# Função para exibir a palavra a ser digitada e o progresso do jogador
def draw_word():
    # Exibe a palavra atual
    word_text = FONT.render("Digite: " + current_word, True, BLACK)
    win.blit(word_text, (100, 200))

    # Exibe a palavra digitada pelo jogador
    typed_text = FONT.render("Digitado: " + typed_word, True, GREEN if typed_word == current_word else RED)
    win.blit(typed_text, (100, 250))

# Loop principal do jogo
running = True
while running:
    win.fill(WHITE)  # Limpa a tela
    draw_keyboard()  # Desenha o teclado
    draw_word()      # Desenha a palavra e a entrada do jogador

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Detecta a tecla pressionada
            if event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]  # Remove o último caractere
            else:
                typed_word += event.unicode  # Adiciona o caractere pressionado

            # Verifica se a palavra está completa e correta
            if typed_word == current_word:
                typed_word = ""  # Limpa a entrada
                current_word = random.choice(words)  # Seleciona nova palavra

    pygame.display.flip()

pygame.quit()
