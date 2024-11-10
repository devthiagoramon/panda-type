import pygame
import sys

# Não importamos beat_panda aqui no início
# Faremos a importação apenas quando necessário

pygame.init()

# Tamanho da tela
size_screen = (600, 400)
screen = pygame.display.set_mode(size_screen)
game_clock = pygame.time.Clock()

# Definir o título do jogo
pygame.display.set_caption('Beat Panda')

# Carregar a imagem do Panda DJ
try:
    panda_dj = pygame.image.load('assets/panda_dj.png')
    panda_dj = pygame.transform.scale(panda_dj, (600, 400))
except:
    panda_dj = pygame.Surface(size_screen)
    panda_dj.fill((0, 0, 0))


def draw_menu():
    screen.fill((0, 0, 0))
    screen.blit(panda_dj, (0, 0))

    font = pygame.font.Font(None, 36)
    title_text = font.render("Beat Panda - Pressione ENTER para começar", True, (255, 255, 255))

    text_rect = title_text.get_rect(center=(size_screen[0] // 2, size_screen[1] // 2))
    screen.blit(title_text, text_rect)

    pygame.display.flip()


def show_menu():
    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    in_menu = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        draw_menu()
        game_clock.tick(30)


def main():
    while True:
        # Primeiro mostra o menu
        show_menu()

        # Só depois que o menu terminar (quando ENTER for pressionado),
        # importamos e iniciamos o jogo
        import beat_panda
        beat_panda.start_game()

        # Se o jogo terminar, voltamos ao menu
        game_clock.tick(30)


if __name__ == '__main__':
    main()