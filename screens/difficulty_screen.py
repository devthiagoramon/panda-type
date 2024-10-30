import pygame

import nivel_1
import nivel_2
import nivel_3
from utils import constants


def main():
    size_screen = (800, 600)
    screen = pygame.display.set_mode(size_screen)
    game_clock = pygame.time.Clock()
    screen.fill(constants.COLOR_BG)
    running = True
    # Buttons
    button_rect_easy = pygame.Rect((screen.get_width() / 2) - (300 / 2), screen.get_height() / 2 - 100, 300, 75)
    button_rect_medium = pygame.Rect((screen.get_width() / 2) - (300 / 2), screen.get_height() / 2, 300, 75)
    button_rect_hard = pygame.Rect((screen.get_width() / 2) - (300 / 2), screen.get_height() / 2 + 100, 300, 75)

    def draw_button(screen_obj, rect, text_obj):
        pygame.draw.rect(screen_obj, constants.COLOR_BUTTON, rect)
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(text_obj, True, constants.COLOR_TEXT_BUTTON)
        text_rect = text_surface.get_rect(center=rect.center)
        screen_obj.blit(text_surface, text_rect)

    # Texts
    sans_bold = pygame.font.Font('fonts/OpenSans-Bold.ttf', 48)
    title_label = sans_bold.render("Selecione uma dificuldade", True, constants.COLOR_BUTTON)
    title_label_rect = title_label.get_rect()
    title_label_pos = (screen.get_width() / 2 - (title_label_rect.width / 2), 100)

    while running:
        screen.blit(title_label, title_label_pos)

        draw_button(screen, button_rect_easy, 'Fácil')
        draw_button(screen, button_rect_medium, 'Médio')
        draw_button(screen, button_rect_hard, 'Difícil')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_rect_easy.collidepoint(pos):
                    running = False
                    nivel_1.main()
                if button_rect_medium.collidepoint(pos):
                    running = False
                    nivel_2.main()
                if button_rect_hard.collidepoint(pos):
                    running = False
                    nivel_3.main()
        pygame.display.update()
        game_clock.tick(60)
