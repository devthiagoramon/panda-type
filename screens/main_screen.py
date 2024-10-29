import pygame
import random as rand

from utils import constants

size_screen = (800, 600)
screen = pygame.display.set_mode(size_screen)
game_clock = pygame.time.Clock()
random_words = []


def read_random_words():
    with open('utils/br-sem-acentos.txt', 'r') as file:
        for linha in file:
            linha = linha.strip()
            random_words.append(linha)


# A função main screen vai exibir a tela principal do jogo e oferecer como opção
# iniciar (1) ou sair (0) do jogo
def main_screen():
    read_random_words()

    running = True
    screen.fill(constants.COLOR_BG)

    container_screen = pygame.Rect((screen.get_width()/2)-(400/2), (screen.get_height() / 2)-(450/2), 400, 450)

    # Buttons
    button_rect_init = pygame.Rect((screen.get_width() / 2) - (300 / 2), screen.get_height() / 2 - 100, 300, 75)
    button_rect_tuto = pygame.Rect((screen.get_width() / 2) - (300 / 2), screen.get_height() / 2, 300, 75)
    button_rect_quit = pygame.Rect((screen.get_width() / 2) - (300 / 2), screen.get_height() / 2 + 100, 300, 75)

    # Texts
    sans_bold = pygame.font.Font('fonts/OpenSans-Bold.ttf', 64)
    sans_regular = pygame.font.Font('fonts/OpenSans-Regular.ttf', 32)
    game_label = sans_bold.render("Panda Type", True, constants.COLOR_BUTTON)
    game_label_rect = game_label.get_rect()
    game_label_pos = (screen.get_width() / 2 - (game_label_rect.width / 2), 100)

    def draw_button(screen_obj, rect, text_obj):
        pygame.draw.rect(screen_obj, constants.COLOR_BUTTON, rect)
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(text_obj, True, constants.COLOR_TEXT_BUTTON)
        text_rect = text_surface.get_rect(center=rect.center)
        screen_obj.blit(text_surface, text_rect)

    def get_random_word():
        return random_words[rand.randint(0, len(random_words) - 1)]

    # Draw the text animation in background
    # Temporizador para controlar o efeito de digitação
    full_text = get_random_word()
    displayed_text = ''
    letter_index = 0
    typing_speed = 100
    time_next_word = 500
    last_update = pygame.time.get_ticks()
    # Margens e altura máxima
    x_margin = 16
    y_margin = 16
    max_height = screen.get_height() - y_margin
    lines = []

    def split_text_into_lines(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '
            line_width, _ = font.size(test_line)
            if line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '

        if current_line:
            lines.append(current_line)

        return lines

    while running:
        current_time = pygame.time.get_ticks()  # Tempo atual em milissegundos
        if current_time - last_update > typing_speed:

            if letter_index < len(full_text):
                displayed_text += full_text[letter_index]
                letter_index += 1
                last_update = current_time
                lines = split_text_into_lines(displayed_text, sans_regular, screen.get_width() - 2 * x_margin)
            else:
                if current_time - last_update > time_next_word:
                    letter_index = 0
                    full_text = " " + get_random_word()

        y_offset = y_margin
        for line in lines:
            text_surface = sans_regular.render(line, True, constants.COLOR_TEXT)
            screen.blit(text_surface, (x_margin, y_offset))
            y_offset += sans_regular.get_height()

        if y_offset > max_height:
            displayed_text = ''
            lines = []
            letter_index = 0

        pygame.draw.rect(screen, constants.COLOR_BG, container_screen)

        screen.blit(game_label, game_label_pos)

        draw_button(screen, button_rect_init, 'Iniciar jogo')
        draw_button(screen, button_rect_tuto, 'Tutorial')
        draw_button(screen, button_rect_quit, 'Sair do jogo')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_rect_init.collidepoint(pos):
                    running = False
                    return 1
                if button_rect_tuto.collidepoint(pos):
                    return 2
                if button_rect_quit.collidepoint(pos):
                    running = False
                    return 0
        pygame.display.update()
        game_clock.tick(60)
