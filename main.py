from menu import Menu
import pygame
from beat_panda import Game

def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo de Ritmo - Digitação")

    menu = Menu(screen)
    clock = pygame.time.Clock()

    while True:
        menu.draw()
        action = menu.handle_input()

        if action == "Iniciar Jogo":
            game = Game()
            game.run()
            break
        elif action == "Instruções":
            while True:
                menu.show_instructions()
                instructions_action = menu.handle_instructions_input()
                if instructions_action in ("back", "quit"):
                    break
        elif action == "Sair" or action == "quit":
            pygame.quit()
            break

        clock.tick(30)

if __name__ == "__main__":
    main()
