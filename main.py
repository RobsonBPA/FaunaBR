# ====================
# IMPORTAÇÕES
# ====================
import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

# ====================
# CONFIGURAÇÕES
# ====================

# ===== Tela =====
tela_lar, tela_alt = 1366, 768
tela = pygame.display.set_mode((tela_lar, tela_alt))

# Tempo do jogo
clock = pygame.time.Clock()

# ===== Nome da janela =====
pygame.display.set_caption("FaunaBR")

# ====================
# TILES
# ====================

TILE_SIZE = 128 # Tamanho do tile

# Carregamento dos tiles
tiles = [
    # Mata Atlântica
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso1.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso2.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso3.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso4.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso5.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso6.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso7.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('images/mata_atlantica/ma_piso8.png'), (TILE_SIZE, TILE_SIZE))
]

# ====================
# MAPA
# ====================

# Tamanho do mapa
MAPA_COLUNAS, MAPA_LINHAS = 50, 50

mapa_lar = MAPA_COLUNAS * TILE_SIZE
mapa_alt = MAPA_LINHAS * TILE_SIZE

# Geração automática do mapa
mapa = []

for linha in range(MAPA_LINHAS):

    nova_linha = []

    for coluna in range(MAPA_COLUNAS):

        # Escolhe um tile aleatório
        tile = random.choices(
            population=[0,1,2,3,4,5,6,7], # Tiles existentes
            weights=[1,1,1,12,1,1,12,1], # Peso de cada tile
            k=1
        )[0]

        nova_linha.append(tile)

    mapa.append(nova_linha)

# ====================
# JOGADOR
# ====================

player = pygame.transform.scale(
    pygame.image.load('images/personagens/pombo/pombo_frente1.png'),
    (96, 96)
)

# Posição inicial
player_x = mapa_lar // 2
player_y = mapa_alt // 2

velocidade = 5

# ====================
# LOOP PRINCIPAL
# ====================

while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # ====================
    # MOVIMENTAÇÃO
    # ====================

    teclas = pygame.key.get_pressed()

    # Subir
    if teclas[K_w] or teclas[K_UP]:
        player_y -= velocidade

    # Descer
    if teclas[K_s] or teclas[K_DOWN]:
        player_y += velocidade

    # Esquerda
    if teclas[K_a] or teclas[K_LEFT]:
        player_x -= velocidade
    
    # Direita
    if teclas[K_d] or teclas[K_RIGHT]:
        player_x += velocidade

    # ====================
    # LIMITES DO MAPA
    # ====================

    if player_x < 0:
        player_x = 0

    if player_y < 0:
        player_y = 0

    if player_x > mapa_lar - 96:
        player_x = mapa_lar - 96

    if player_y > mapa_alt - 96:
        player_y = mapa_alt - 96

    # ====================
    # CÂMERA
    # ====================

    camera_x = player_x - tela_lar // 2
    camera_y = player_y - tela_alt // 2

    camera_x = max(0, min(camera_x, mapa_lar - tela_lar))
    camera_y = max(0, min(camera_y, mapa_alt - tela_alt))

    # ====================
    # DESENHO DO MAPA
    # ====================

    for linha in range(MAPA_LINHAS):

        for coluna in range(MAPA_COLUNAS):

            tile_id = mapa[linha][coluna]

            tile = tiles[tile_id]

            x = coluna * TILE_SIZE
            y = linha * TILE_SIZE

            tela.blit(
                tile,
                (x - camera_x, y - camera_y)
            )

    # ====================
    # DESENHO DO PLAYER
    # ====================

    tela.blit(
        player,
        (player_x - camera_x, player_y - camera_y)
    )

    pygame.display.update()