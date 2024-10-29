import pygame
from utils import constants


size_screen = (800, 600)
screen = pygame.display.set_mode(size_screen)
game_clock = pygame.time.Clock()


def main():
    pygame.init()
    running = True
    screen.fill(constants.COLOR_BG)

    sans_bold = pygame.font.Font('fonts/OpenSans-Bold.ttf', 64)
    tutorial_label = sans_bold.render("Bem vindo ao tutorial", True, constants.COLOR_BUTTON)
    tutorial_rect = tutorial_label.get_rect()
    tutorial_label_pos = (screen.get_width() / 2 - (tutorial_rect.width / 2), 50)

    text_image = pygame.image.load('assets/tutorial_main_screen_text.png')
    image_width, image_height = text_image.get_size()

    posicao_x = (screen.get_width() - image_width) // 2
    posicao_y = (screen.get_height() - image_height - 60) // 2

    button_rect_init_tutorial = pygame.Rect((screen.get_width() / 2) - (300 / 2), screen.get_height() / 2 + 125, 300, 75)

    def draw_button(screen_obj, rect, text_obj):
        pygame.draw.rect(screen_obj, constants.COLOR_BUTTON, rect)
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(text_obj, True, constants.COLOR_TEXT_BUTTON)
        text_rect = text_surface.get_rect(center=rect.center)
        screen_obj.blit(text_surface, text_rect)

    while running:
        screen.blit(tutorial_label, tutorial_label_pos)
        draw_button(screen, button_rect_init_tutorial, 'Iniciar tutorial')
        screen.blit(text_image, (posicao_x, posicao_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_rect_init_tutorial.collidepoint(pos):
                    running = False
                    return 1
        pygame.display.update()
        game_clock.tick(60)
