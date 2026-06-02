# ====================
# IMPORTAÇÕES
# ====================

import pygame
from pygame.locals import *
from sys import exit

from src.player import Jogador # Classe jogador
from src.mapa import gerar_mapa # Função para gerar mapa
from src.camera import atualizar_camera # Câmera
from src.config import * # Configurações

pygame.init()

# ====================
# CONFIGURAÇÕES
# ====================

# ===== Tela =====
tela = pygame.display.set_mode((TELA_LAR, TELA_ALT))
pygame.display.set_caption("FaunaBR") # Nome da janela

clock = pygame.time.Clock() # Tempo do jogo

# ====================
# TILES
# ====================

# Carregamento dos tiles
tiles = [
    # Mata Atlântica
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso1.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso2.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso3.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso4.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso5.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso6.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso7.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso8.png'), (TILE_SIZE, TILE_SIZE))
]

# ====================
# MAPA
# ====================

mapa_lar = MAPA_COLUNAS * TILE_SIZE
mapa_alt = MAPA_LINHAS * TILE_SIZE

mapa = gerar_mapa(MAPA_COLUNAS, MAPA_LINHAS)

# ====================
# JOGADOR
# ====================

player = Jogador()
player.x = mapa_lar // 2
player.y = mapa_alt //2

# ====================
# LOOP PRINCIPAL
# ====================

while True:

    clock.tick(60)

    # ====================
    # EVENTOS
    # ====================

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            exit()

    # ====================
    # MOVIMENTAÇÃO
    # ====================

    player.mover()

    # ====================
    # LIMITES DO MAPA
    # ====================

    if player.x < 0:
        player.x = 0

    if player.y < 0:
        player.y = 0

    if player.x > mapa_lar - 96:
        player.x = mapa_lar - 96

    if player.y > mapa_alt - 96:
        player.y = mapa_alt - 96

    # ====================
    # CÂMERA
    # ====================

    camera_x, camera_y = atualizar_camera(
        player.x,
        player.y,
        TELA_LAR,
        TELA_ALT,
        mapa_lar,
        mapa_alt
    )

    # ====================
    # DESENHO
    # ====================

    tela.fill((0, 0, 0))

    # Mapa
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

    # Jogador
    tela.blit(
        player.sprite,
        (
            player.x - camera_x,
            player.y - camera_y
        )
    )

    pygame.display.update()