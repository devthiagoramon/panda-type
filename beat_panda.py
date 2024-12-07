import pygame
import time
import librosa

from letter import Letter
from healthbar import HealthBar
from multiplier import Multiplier


class Game:

    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 600
        self.SCREEN_HEIGHT = 400
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Beat Panda")

        self.wallpaper = pygame.image.load("assets/wallpaper.jpg")
        self.wallpaper = pygame.transform.scale(self.wallpaper, (1000, 435))

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.PURPLE = (128, 0, 128)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)

        self.mao_esquerda = pygame.image.load("assets/left_hand.png")
        self.mao_direita = pygame.image.load("assets/right_hand.png")

        self.font = pygame.font.Font(None, 36)

        self.TARGET_Y = self.SCREEN_HEIGHT - 50
        self.LETTER_SPEED = 2
        self.falling_letters = []
        self.score = 0

        # Barra de saúde
        self.health_bar = HealthBar(max_health=100, position=(10, 40), size=(200, 20))
        self.health_loss_per_miss = 20

        # Multiplicador de combo
        self.multiplier = Multiplier()

        # Música e sincronização com ritmo
        self.audio_path = 'assets/Travelers.mp3'  # Caminho para o arquivo de áudio
        self.y_audio, self.sr_audio = librosa.load(self.audio_path, sr=None)
        self.tempo, self.beat_frames = librosa.beat.beat_track(y=self.y_audio, sr=self.sr_audio)
        self.beat_times = librosa.frames_to_time(self.beat_frames, sr=self.sr_audio)

        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play()
        self.start_time = time.time()

        # Mapeamento de teclas para dedos
        self.tecla_para_dedo = {
            'q': 'left_pinky', 'a': 'left_pinky', 'z': 'left_pinky',
            'w': 'left_ring', 's': 'left_ring', 'x': 'left_ring',
            'e': 'left_middle', 'd': 'left_middle', 'c': 'left_middle',
            'r': 'left_index', 'f': 'left_index', 'v': 'left_index', 't': 'left_index', 'g': 'left_index',
            'b': 'left_index',
            'y': 'right_index', 'h': 'right_index', 'n': 'right_index', 'u': 'right_index', 'j': 'right_index',
            'm': 'right_index',
            'i': 'right_middle', 'k': 'right_middle',
            'o': 'right_ring', 'l': 'right_ring',
            'p': 'right_pinky'
        }

        # Cores dos dedos
        self.dedo_cores = {
            'left_pinky': self.PURPLE,
            'right_pinky': self.PURPLE,
            'left_ring': self.YELLOW,
            'right_ring': self.YELLOW,
            'left_middle': self.RED,
            'right_middle': self.RED,
            'left_index': self.GREEN,
            'right_index': self.GREEN
        }

    def create_letter(self):
        x_range = (50, self.SCREEN_WIDTH - 50)
        return Letter(x_range)

    def game_over_screen(self):
        pygame.mixer.music.stop()
        self.screen.fill(self.BLACK)
        game_over_text = self.font.render("Você perdeu :(", True, self.RED)
        score_text = self.font.render(f"Sua Pontuação: {self.score}", True, self.WHITE)
        self.screen.blit(game_over_text,
                         (self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, self.SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text,
                         (self.SCREEN_WIDTH // 2 - score_text.get_width() // 2, self.SCREEN_HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(4000)

    def victory_screen(self):
        self.screen.fill(self.BLACK)
        victory_text = self.font.render("Você ganhou!", True, self.GREEN)
        self.screen.blit(victory_text,
                         (self.SCREEN_WIDTH // 2 - victory_text.get_width() // 2, self.SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(4000)

    def run(self):
        running = True
        while running:
            self.screen.blit(self.wallpaper, (0, 0))
            current_time = time.time() - self.start_time

            # Condição de vitória
            if current_time >= 212:
                self.victory_screen()
                print("Música terminou!")
                running = False  # Finaliza o jogo

            # Criar letras de acordo com as batidas
            if self.beat_times.size > 0 and current_time >= self.beat_times[0]:
                if len(self.falling_letters) < 3:
                    self.falling_letters.append(self.create_letter())
                self.beat_times = self.beat_times[1:]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    letter_hit = False
                    for letter in self.falling_letters:
                        if event.unicode.upper() == letter.letter and abs(letter.y - self.TARGET_Y) < 20:
                            letter.hit = True
                            self.score += 10 * self.multiplier.combo_multiplier
                            letter_hit = True
                            break
                    self.multiplier.update(letter_hit)

            # Atualizar e desenhar letras
            for letter in self.falling_letters:
                if not letter.hit:
                    letter.update_position(self.LETTER_SPEED)
                    if letter.y > self.SCREEN_HEIGHT:
                        letter.hit = True
                        self.health_bar.reduce_health(self.health_loss_per_miss)
                        self.multiplier.update(False)

            if self.health_bar.current_health <= 0:
                print("Game Over!")
                self.game_over_screen()
                running = False

            # Desenhar letras
            for letter in self.falling_letters:
                if letter.hit:
                    color = self.GREEN if letter.y <= self.SCREEN_HEIGHT else self.RED
                else:
                    dedo = self.tecla_para_dedo.get(letter.letter.lower(), None)
                    if dedo:
                        color = self.dedo_cores.get(dedo, self.RED)
                    else:
                        color = self.RED
                letter.draw(self.screen, self.font, color)

            # Remover letras que saíram da tela ou foram acertadas
            self.falling_letters = [letter for letter in self.falling_letters if
                                    letter.y <= self.SCREEN_HEIGHT and not letter.hit]

            # Linha alvo
            pygame.draw.line(self.screen, self.GREEN, (0, self.TARGET_Y), (self.SCREEN_WIDTH, self.TARGET_Y), 2)

            # Exibir pontuação e multiplicador
            score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
            self.screen.blit(score_text, (10, 10))

            multiplier_text = self.font.render(f"Multiplier: x{self.multiplier.combo_multiplier}", True, self.WHITE)
            self.screen.blit(multiplier_text, (10, 60))

            # Desenhar barra de saúde
            self.health_bar.draw(self.screen)

            pygame.display.flip()
            pygame.time.delay(15)

        pygame.quit()
