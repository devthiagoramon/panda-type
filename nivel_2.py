import pygame
import random


def main():
    WIDTH, HEIGHT = 1000, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Panda Type - Nível Fácil")

    # Cores e fonte
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    FONT = pygame.font.SysFont("Arial", 32)

    panda_img = pygame.image.load("assets/panda.jpg")
    panda_img = pygame.transform.scale(panda_img, (100, 100))

    mao_esquerda = pygame.image.load("assets/left_hand.png")
    mao_direita = pygame.image.load("assets/right_hand.png")
    mao_esquerda = pygame.transform.scale(mao_esquerda, (150, 200))
    mao_direita = pygame.transform.scale(mao_direita, (150, 200))


    words = ["Girafa","Bicicleta","Comida","Futebol","Careca","Maleta","Limonada","Levado","Estojo","Elogio", "Panda", "Sapato", "Cozinha", "Mangueira"]
    current_word = random.choice(words)
    typed_word = ""
    score = 0
    vidas = 4
    error_made = False

    # Temporizador
    time_limit = 20000
    start_time = pygame.time.get_ticks()
    progress_bar_width = 300

    tecla_para_dedo = {
        'q': 'left_pinky', 'a': 'left_pinky', 'z': 'left_pinky',
        'w': 'left_ring', 's': 'left_ring', 'x': 'left_ring',
        'e': 'left_middle', 'd': 'left_middle', 'c': 'left_middle',
        'r': 'left_index', 'f': 'left_index', 'v': 'left_index',
        'u': 'right_index', 'j': 'right_index', 'm': 'right_index',
        'i': 'right_middle', 'k': 'right_middle',
        'o': 'right_ring', 'l': 'right_ring',
        'p': 'right_pinky'
    }

    # Função para desenhar o teclado
    def draw_keyboard():
        x, y = 200, 300  # Ajuste para centralizar o teclado
        row_gap, key_gap = 60, 50
        keys = [
            "1234567890-=", "qwertyuiop[]", "asdfghjklç~", "zxcvbnm,.;/"
        ]

        next_letter = current_word[len(typed_word)] if len(typed_word) < len(current_word) else ""
        highlight_shift = next_letter.isupper()

        # Desenhar as teclas do teclado
        for row in keys:
            for key in row:
                color = GREEN if key.lower() == next_letter.lower() else WHITE
                pygame.draw.rect(win, color, (x, y, 40, 40))
                pygame.draw.rect(win, BLACK, (x, y, 40, 40), 2)
                key_text = FONT.render(key, True, BLACK)
                win.blit(key_text, (x + 10, y + 5))
                x += key_gap
            x = 200
            y += row_gap

        # Teclas especiais
        if highlight_shift and next_letter:
            key_text = FONT.render(next_letter, True, GREEN)
            win.blit(key_text, (x + 10, y + 5))

        pygame.draw.rect(win, WHITE, (300, y, 300, 40))
        pygame.draw.rect(win, BLACK, (300, y, 300, 40), 2)
        space_text = FONT.render("Espaço", True, BLACK)
        win.blit(space_text, (425, y + 5))

        shift_color = GREEN if highlight_shift else WHITE
        pygame.draw.rect(win, shift_color, (200, y, 80, 40))
        pygame.draw.rect(win, BLACK, (200, y, 80, 40), 2)
        shift_text = FONT.render("Shift", True, BLACK)
        win.blit(shift_text, (210, y + 5))

        backspace_color = RED if error_made else WHITE
        pygame.draw.rect(win, backspace_color, (700, 300, 100, 40))
        pygame.draw.rect(win, BLACK, (700, 300, 100, 40), 2)
        backspace_text = FONT.render("Backspace", True, BLACK)
        win.blit(backspace_text, (710, 305))

        pygame.draw.rect(win, WHITE, (700, 360, 100, 40))
        pygame.draw.rect(win, BLACK, (700, 360, 100, 40), 2)
        enter_text = FONT.render("Enter", True, BLACK)
        win.blit(enter_text, (720, 365))

    # Função para desenhar as imagens das mãos
    def draw_hands():
        # Exibir a mão esquerda à esquerda do teclado
        win.blit(mao_esquerda, (30, 320))
        # Exibir a mão direita à direita do teclado
        win.blit(mao_direita, (820, 320))

        # Determinar o dedo a marcar
        next_letter = current_word[len(typed_word)].lower() if len(typed_word) < len(current_word) else ""
        dedo_marcado = tecla_para_dedo.get(next_letter)

        # Dicionário com ajustes mais para cima e à direita
        posicoes_dedos = {
            'left_pinky': (40, 400),  # Dedo mínimo esquerdo
            'left_ring': (60, 360),  # Dedo anelar esquerdo
            'left_middle': (100, 340),  # Dedo médio esquerdo
            'left_index': (135, 370),  # Dedo indicador esquerdo
            'right_index': (865, 370),  # Dedo indicador direito
            'right_middle': (900, 350),  # Dedo médio direito
            'right_ring': (940, 360),  # Dedo anelar direito
            'right_pinky': (960, 390)  # Dedo mínimo direito
        }

        # Desenhar a marcação na ponta do dedo correto
        if dedo_marcado and dedo_marcado in posicoes_dedos:
            pos_x, pos_y = posicoes_dedos[dedo_marcado]
            pygame.draw.circle(win, BLUE, (pos_x, pos_y), 10)



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
        win.blit(panda_img, (WIDTH - 110, 10))
        pygame.display.flip()
        pygame.time.delay(3000)

    def defeat_condition():
        win.fill(WHITE)
        defeat_text = FONT.render("Você perdeu", True, RED)
        score_text = FONT.render("Pontuação Final: " + str(score), True, BLACK)
        win.blit(defeat_text, (250, 250))
        win.blit(score_text, (250, 300))
        win.blit(panda_img, (WIDTH - 110, 10))
        pygame.display.flip()
        pygame.time.delay(3000)

    # Loop principal do jogo
    running = True
    while running:
        win.fill(WHITE)
        draw_keyboard()
        draw_word_and_score()
        draw_progress_bar()
        draw_hands()  # Desenhar as imagens das mãos

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
                elif event.key not in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    char = event.unicode
                    if len(typed_word) < len(current_word):
                        typed_word += char
                    if typed_word[-1] != current_word[len(typed_word) - 1]:
                        error_made = True
                    else:
                        error_made = False

        pygame.display.flip()

    pygame.quit()