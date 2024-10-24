import pygame
import screens.main_screen as ms

pygame.init()
size_screen = (800, 600)
screen = pygame.display.set_mode(size_screen)
game_clock = pygame.time.Clock()
pygame.display.set_caption('Panda Type')


def main():
    option = ms.main_screen()
    if option == 1:
        pass
    else:
        pygame.quit()


if __name__ == '__main__':
    main()
