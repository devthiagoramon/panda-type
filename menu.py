import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.PURPLE = (128, 0, 128)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.font = pygame.font.Font(None, 36)
        self.menu_options = ["Iniciar Jogo", "Instruções", "Sair"]
        self.selected_option = 0

    def draw(self):
        self.screen.fill(self.BLACK)
        for i, option in enumerate(self.menu_options):
            color = self.WHITE if i == self.selected_option else (100, 100, 100)
            text = self.font.render(option, True, color)
            self.screen.blit(
                text,
                (self.screen.get_width() // 2 - text.get_width() // 2, 150 + i * 50)
            )
        pygame.display.flip()

    def show_instructions(self):
        self.screen.fill(self.BLACK)
        instructions = [
            ("Dedos e teclas:", self.WHITE),
            ("Mindinho Esquerdo (Q, A, Z)", self.PURPLE),
            ("Anelar Esquerdo (W, S, X)", self.YELLOW),
            ("Médio Esquerdo (E, D, C)", self.BLUE),
            ("Indicador Esquerdo (R, F, V, T, G, B)", self.GREEN),
            ("Indicador Direito (Y, H, N, U, J, M)", self.GREEN),
            ("Médio Direito (I, K)", self.BLUE),
            ("Anelar Direito (O, L)", self.YELLOW),
            ("Mindinho Direito (P)", self.PURPLE),
        ]
        y_offset = 50
        for text, color in instructions:
            rendered_text = self.font.render(text, True, color)
            self.screen.blit(
                rendered_text,
                (self.screen.get_width() // 2 - rendered_text.get_width() // 2, y_offset)
            )
            y_offset += 40

        back_text = self.font.render("Pressione ESC para voltar", True, self.WHITE)
        self.screen.blit(
            back_text,
            (self.screen.get_width() // 2 - back_text.get_width() // 2, y_offset + 20)
        )
        pygame.display.flip()

    def handle_instructions_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"
        return None

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    return self.menu_options[self.selected_option]
        return None