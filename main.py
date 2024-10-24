import pygame

pygame.init()
size_screen = (800, 600)
screen = pygame.display.set_mode(size_screen)
game_clock = pygame.time.Clock()


def main():
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

    pygame.display.flip()
    game_clock.tick(60)


if __name__ == '__main__':
    main()
