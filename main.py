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
from src.npc import NPC # NPC

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
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/ma_piso8.png'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/agua_areia1.jpeg'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/agua1.jpeg'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/agua2.jpeg'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/agua3.jpeg'), (TILE_SIZE, TILE_SIZE)),
    pygame.transform.scale(pygame.image.load('assets/images/tiles/mata_atlantica/agua4.jpeg'), (TILE_SIZE, TILE_SIZE)),
]

# ====================
# MAPA
# ====================

mapa_lar = MAPA_COLUNAS * TILE_SIZE
mapa_alt = MAPA_LINHAS * TILE_SIZE

mapa = gerar_mapa(MAPA_COLUNAS, MAPA_LINHAS)

# ======= CASA =======
casa_img = pygame.transform.scale(pygame.image.load("assets/images/construcoes/casa.png").convert_alpha(), (512, 512))
casa_x = mapa_lar // 2 + 200
casa_y = mapa_alt // 2

casa_rect = pygame.Rect(casa_x, casa_y, 512, 512)

# ====================
# JOGADOR
# ====================

player = Jogador()
player.x = mapa_lar // 2
player.y = mapa_alt // 2

# ====================
# NPC
# ====================

from src.npc import NPC

# ===== Mensagens do Diálogo =====
npcs = [
    NPC(
        # Capivara
        "Capivara",
        "assets/images/personagens/capivara/capivara_frente1.png", 3200, 3200,
        [
            "Ola! Eu sou uma capivara.",
            "Sou o maior roedor do mundo.",
            "Gosto de viver perto da agua.",
            "No Brasil, posso ser encontrada em varios biomas."
        ]
    )
]

# ===== Configurações dos Diálogos =====
fonte_dialogo = pygame.font.Font(None, 36)

dialogo_ativo = False
npc_atual = None
fala_atual = 0

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

        # ===================
        # DIÁLOGO
        # ====================
        if event.type == KEYDOWN:
            if event.key == K_e:
                if dialogo_ativo:
                    fala_atual += 1

                    if fala_atual >= len(npc_atual.dialogos):
                        dialogo_ativo = False
                        npc_atual = None
                        fala_atual = 0

                else:
                    player_rect = pygame.Rect(player.x, player.y, 96, 96)

                    for npc in npcs:
                        area_interacao = npc.get_rect().inflate(80, 80)

                        if player_rect.colliderect(area_interacao):
                            dialogo_ativo = True
                            npc_atual = npc
                            fala_atual = 0
                            break

    # ====================
    # MOVIMENTAÇÃO
    # ====================

    # Posição antiga do jogador
    x_antigo = player.x
    y_antigo = player.y

    if not dialogo_ativo:
        player.mover()

    # Colisão
    player_rect = pygame.Rect(player.x, player.y, 96, 96)
    if player_rect.colliderect(casa_rect):
        player.x = x_antigo
        player.y = y_antigo

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

    # ===== MAPA =====
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

    # ===== JOGADOR =====
    tela.blit(
        player.sprite,
        (
            player.x - camera_x,
            player.y - camera_y
        )
    )

    # ===== Geração dos NPCs =====
    for npc in npcs:
        npc.desenhar(tela, camera_x, camera_y)

    # ===== CASA =====
    tela.blit(
    casa_img,
    (
        casa_x - camera_x,
        casa_y - camera_y
    )
)

    # ===== Geração do Diálogo =====
    if dialogo_ativo and npc_atual is not None:
        caixa = pygame.Rect(80, TELA_ALT - 180, TELA_LAR - 160, 130)

        pygame.draw.rect(tela, (20, 20, 20), caixa)
        pygame.draw.rect(tela, (255, 255, 255), caixa, 4)

        nome_texto = fonte_dialogo.render(npc_atual.nome, True, (255, 255, 0))
        fala_texto = fonte_dialogo.render(
            npc_atual.dialogos[fala_atual],
            True,
            (255, 255, 255)
        )

        tela.blit(nome_texto, (caixa.x + 25, caixa.y + 20))
        tela.blit(fala_texto, (caixa.x + 25, caixa.y + 65))

    pygame.display.update()