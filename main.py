import pygame
import sys

pygame.init()

# Tamanho da tela
size_screen = (600, 400)
screen = pygame.display.set_mode(size_screen)
game_clock = pygame.time.Clock()

# Definir o título do jogo
pygame.display.set_caption('Beat Panda')

menu_music = 'assets/menu_music.mp3'
pygame.mixer.init()
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(start=15)

# Carregar a imagem do Panda DJ
try:
    panda_dj = pygame.image.load('assets/panda_dj.png')
    panda_dj = pygame.transform.scale(panda_dj, (600, 400))
except:
    panda_dj = pygame.Surface(size_screen)
    panda_dj.fill((0, 0, 0))

# Carregar a imagem que será exibida ao pressionar ENTER
try:
    imagem_nova = pygame.image.load('assets/maos.jpg')  # Substitua pelo seu arquivo de imagem
    imagem_nova = pygame.transform.scale(imagem_nova, (600, 400))  # Ajuste o tamanho se necessário
except:
    imagem_nova = pygame.Surface(size_screen)
    imagem_nova.fill((255, 0, 0))  # Cor de fundo caso a imagem não seja carregada

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
                    show_new_image()  # Chama a função que exibe a nova imagem
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        draw_menu()
        game_clock.tick(30)


def show_new_image():
    showing_instructions = True
    font = pygame.font.Font(None, 36)

    while showing_instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    showing_instructions = False  # Sai do loop e inicia o jogo
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Exibir fundo e imagem
        screen.fill((0, 0, 0))
        screen.blit(imagem_nova, (0, 50))  # Exibe a nova imagem, deslocada para baixo

        # Exibir instrução acima da imagem
        instruction_text = font.render("Aperte as teclas conforme as cores da imagem", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(size_screen[0] // 2, 30))
        screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()
        game_clock.tick(30)

    # Após pressionar ENTER, inicia o jogo
    import beat_panda
    beat_panda.start_game()


def main():
    while True:
        # Primeiro mostra o menu
        show_menu()

        # Após sair do menu, inicia o jogo
        game_clock.tick(30)


if __name__ == '__main__':
    main()
