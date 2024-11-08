import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beat Panda")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonte
font = pygame.font.Font(None, 36)

# Área de acerto (onde o jogador deve apertar as letras)
TARGET_Y = SCREEN_HEIGHT - 50

# Velocidade das letras e intervalo de aparição
LETTER_SPEED = 2
LETTER_INTERVAL = 1.5  # em segundos

# Lista para armazenar as letras que caem
falling_letters = []
last_letter_time = time.time()

# Pontuação
score = 0

# Função para criar uma nova letra
def create_letter():
    letter = chr(random.randint(65, 90))  # Letras A-Z
    x_pos = random.randint(50, SCREEN_WIDTH - 50)
    y_pos = 0
    return {"letter": letter, "x": x_pos, "y": y_pos, "hit": False}

# Loop principal do jogo
running = True
while running:
    screen.fill(BLACK)
    current_time = time.time()

    # Cria uma nova letra a cada LETTER_INTERVAL segundos
    if current_time - last_letter_time > LETTER_INTERVAL:
        falling_letters.append(create_letter())
        last_letter_time = current_time

    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Verifica se uma letra foi pressionada e se está na área de acerto
            for letter in falling_letters:
                if event.unicode.upper() == letter["letter"] and abs(letter["y"] - TARGET_Y) < 20:
                    letter["hit"] = True
                    score += 10
                    break

    # Atualiza a posição das letras
    for letter in falling_letters:
        if not letter["hit"]:
            letter["y"] += LETTER_SPEED
            # Se a letra passar da área de acerto sem ser pressionada
            if letter["y"] > SCREEN_HEIGHT:
                letter["hit"] = True  # Considera como "falha" e remove depois

    # Desenha as letras na tela
    for letter in falling_letters:
        if letter["hit"]:
            color = GREEN if letter["y"] <= SCREEN_HEIGHT else RED
        else:
            color = WHITE
        text = font.render(letter["letter"], True, color)
        screen.blit(text, (letter["x"], letter["y"]))

    # Remove letras que já foram acertadas ou que passaram
    falling_letters = [letter for letter in falling_letters if letter["y"] <= SCREEN_HEIGHT and not letter["hit"]]

    # Desenha a área de acerto
    pygame.draw.line(screen, GREEN, (0, TARGET_Y), (SCREEN_WIDTH, TARGET_Y), 2)

    # Exibe a pontuação
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
