import librosa
import pygame
import random
import time

# Carregar a música e identificar os tempos das batidas
audio_path = 'assets/Travelers.mp3'  # Caminho para o arquivo de áudio
y, sr = librosa.load(audio_path, sr=None)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Converter os frames das batidas em tempos em segundos
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

tecla_para_dedo = {
    'q': 'left_pinky', 'a': 'left_pinky', 'z': 'left_pinky',
    'w': 'left_ring', 's': 'left_ring', 'x': 'left_ring',
    'e': 'left_middle', 'd': 'left_middle', 'c': 'left_middle',
    'r': 'left_index', 'f': 'left_index', 'v': 'left_index', 't': 'left_index', 'g': 'left_index', 'b': 'left_index',
    'y': 'right_index', 'h': 'right_index', 'n': 'right_index', 'u': 'right_index', 'j': 'right_index', 'm': 'right_index',
    'i': 'right_middle', 'k': 'right_middle',
    'o': 'right_ring', 'l': 'right_ring',
    'p': 'right_pinky'
}

# Inicializar o Pygame
pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Ritmo - Digitação")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Cores dos dedos
dedo_cores = {
    'left_pinky': PURPLE,
    'right_pinky': PURPLE,
    'left_ring': YELLOW,
    'right_ring': YELLOW,
    'left_middle': BLUE,
    'right_middle': BLUE,
    'left_index': GREEN,
    'right_index': GREEN
}

font = pygame.font.Font(None, 36)

TARGET_Y = SCREEN_HEIGHT - 50
LETTER_SPEED = 2

falling_letters = []
score = 0
max_health = 100
current_health = max_health
health_loss_per_miss = 20

# Variáveis de combo
combo_multiplier = 1
combo_streak = 0
combo_levels = [1, 2, 4, 8]

# Música e sincronização com ritmo
pygame.mixer.init()
pygame.mixer.music.load(audio_path)
pygame.mixer.music.play()
start_time = time.time()

# Carregar as imagens
mao_esquerda = pygame.image.load("assets/left_hand.png")
mao_direita = pygame.image.load("assets/right_hand.png")



# Função para criar uma letra
def create_letter():
    letter = chr(random.randint(65, 90))  # Cria uma letra aleatória
    x_pos = random.randint(50, SCREEN_WIDTH - 50)  # Posição X aleatória
    y_pos = 0  # Começa no topo da tela
    return {"letter": letter, "x": x_pos, "y": y_pos, "hit": False}

# Barra de saúde
def draw_health_bar():
    bar_width = 200
    bar_height = 20
    health_ratio = current_health / max_health
    pygame.draw.rect(screen, RED, (10, 40, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (10, 40, bar_width * health_ratio, bar_height))

# Atualizar multiplicador
def update_multiplier(hit):
    global combo_streak, combo_multiplier
    if hit:
        combo_streak += 1
        if combo_streak >= 8:
            combo_multiplier = 8
        elif combo_streak >= 4:
            combo_multiplier = 4
        elif combo_streak >= 2:
            combo_multiplier = 2
    else:
        combo_streak = max(0, combo_streak - 1)
        if combo_multiplier > 1:
            combo_multiplier = combo_levels[combo_levels.index(combo_multiplier) - 1]

# Tela de derrota
def game_over_screen():
    pygame.mixer.music.stop()  # Interrompe a música ao exibir a tela de derrota
    screen.fill(BLACK)
    game_over_text = font.render("Você perdeu :(", True, RED)
    score_text = font.render(f"Sua Pontuação: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(4000)  # Mantém a tela de derrota por 4 segundos

# Tela de vitória
def victory_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Você ganhou!", True, GREEN)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(4000)  # Mantém a tela de vitória por 4 segundos


# Loop principal do jogo
running = True
while running:
    screen.fill(BLACK)
    current_time = time.time() - start_time

    # Victory condition
    if current_time >= 212:
        victory_screen()
        print("Música terminou!")
        running = False  # Finaliza o jogo

    # Criar menos letras de acordo com as batidas
    if beat_times.size > 0 and current_time >= beat_times[0]:
        if len(falling_letters) < 3:  # Limite no número de letras caindo
            falling_letters.append(create_letter())  # Cria uma única letra para cada batida
        beat_times = beat_times[1:]  # Remover o tempo já usado

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            letter_hit = False
            for letter in falling_letters:
                if event.unicode.upper() == letter["letter"] and abs(letter["y"] - TARGET_Y) < 20:
                    letter["hit"] = True
                    score += 10 * combo_multiplier
                    letter_hit = True
                    break
            update_multiplier(letter_hit)

    for letter in falling_letters:
        if not letter["hit"]:
            letter["y"] += LETTER_SPEED
            if letter["y"] > SCREEN_HEIGHT:
                letter["hit"] = True
                current_health -= health_loss_per_miss
                update_multiplier(False)

    if current_health <= 0:
        print("Game Over!")
        game_over_screen()
        running = False

    # Desenhar as letras com cores diferentes conforme o dedo
    for letter in falling_letters:
        if letter["hit"]:
            color = GREEN if letter["y"] <= SCREEN_HEIGHT else RED
        else:
            # Obter o dedo correspondente à letra e pegar a cor associada
            dedo = tecla_para_dedo.get(letter["letter"].lower(), None)
            if dedo:
                color = dedo_cores.get(dedo, RED)  # Usar cor do dedo ou vermelho como padrão
            else:
                color = RED
        text = font.render(letter["letter"], True, color)
        screen.blit(text, (letter["x"], letter["y"]))

    falling_letters = [letter for letter in falling_letters if letter["y"] <= SCREEN_HEIGHT and not letter["hit"]]

    pygame.draw.line(screen, GREEN, (0, TARGET_Y), (SCREEN_WIDTH, TARGET_Y), 2)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    multiplier_text = font.render(f"Multiplier: x{combo_multiplier}", True, WHITE)
    screen.blit(multiplier_text, (10, 60))

    draw_health_bar()

    pygame.display.flip()
    pygame.time.delay(15)

pygame.quit()
