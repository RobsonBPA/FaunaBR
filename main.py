# ====================
# IMPORTAÇÕES
# ====================

import os
import sys

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

import pygame
from pygame.locals import *
from sys import exit

import pytmx
from pytmx.util_pygame import load_pygame

from src.player import Jogador
from src.camera import atualizar_camera
from src.config import *
from src.npc import NPC

pygame.init()

# ====================
# CONFIGURAÇÕES
# ====================

tela = pygame.display.set_mode((TELA_LAR, TELA_ALT))
pygame.display.set_caption("FaunaBR")

clock = pygame.time.Clock()

# ====================
# MAPA TILED
# ====================

mata_atlantica = pytmx.util_pygame.load_pygame(
    resource_path("assets/images/maps/mata_atlantica.tmx")
)

#mata_atlantica = load_pygame("assets/images/maps/mata_atlantica.tmx")

mapa_lar = mata_atlantica.width * TILE_SIZE
mapa_alt = mata_atlantica.height * TILE_SIZE

tile_cache = {}

def obter_tile(gid):
    if gid not in tile_cache:
        imagem = mata_atlantica.get_tile_image_by_gid(gid)

        if imagem is None:
            tile_cache[gid] = None
        else:
            tile_cache[gid] = pygame.transform.scale(
                imagem,
                (TILE_SIZE, TILE_SIZE)
            )

    return tile_cache[gid]

# ====================
# CASA
# ====================

casa_img = pygame.transform.scale(
    pygame.image.load(
        resource_path("assets/images/construcoes/casa.png")
    ).convert_alpha(),
    (384, 384)
)

casa_x = mapa_lar // 2 + 200
casa_y = mapa_alt // 2

casa_rect = pygame.Rect(casa_x, casa_y, 372, 372)

# ====================
# JOGADOR
# ====================

player = Jogador()
player.x = mapa_lar // 2
player.y = mapa_alt // 2

# ====================
# NPCs
# ====================

npcs = [
    NPC(
        "Capivara",
        resource_path("assets/images/personagens/capivara/capivara_frente1.png"),
        450,
        3400,
        [
            "Ola! Eu sou uma capivara.",
            "Sou o maior roedor do mundo.",
            "Gosto de viver perto da agua.",
            "No Brasil, posso ser encontrada em varios biomas."
        ]
    ),

    NPC(
        "Pombo",
        resource_path("assets/images/personagens/pombo/pombo_frente1.png"),
        3000,
        3000,
        [
            "Fala 1",
            "Fala 2",
            "Fala 3",
            "Fala 4"
        ]
    ),

    NPC(
        "Escorpião",
        resource_path("assets/images/personagens/escorpiao/escorpiao_frente1.png"),
        350,
        550,
        [
            "Fala 1",
            "Fala 2",
            "Fala 3",
            "Fala 4"
        ]
    ),

    NPC(
        "Cachorro",
        resource_path("assets/images/personagens/cachorro/cachorro1.png"),
        400,
        400,
        [
            "Fala 1",
            "Fala 2",
            "Fala 3",
            "Fala 4"
        ]
    ),
]

# ====================
# DIÁLOGO
# ====================

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

    x_antigo = player.x
    y_antigo = player.y

    if not dialogo_ativo:
        player.mover()

    # ====================
    # COLISÃO
    # ====================

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
    coluna_inicial = camera_x // TILE_SIZE
    coluna_final = (camera_x + TELA_LAR) // TILE_SIZE + 1

    linha_inicial = camera_y // TILE_SIZE
    linha_final = (camera_y + TELA_ALT) // TILE_SIZE + 1

    coluna_inicial = max(0, coluna_inicial)
    linha_inicial = max(0, linha_inicial)

    coluna_final = min(mata_atlantica.width, coluna_final)
    linha_final = min(mata_atlantica.height, linha_final)

    for layer in mata_atlantica.visible_layers:
        if hasattr(layer, "data"):
            for y in range(linha_inicial, linha_final):
                for x in range(coluna_inicial, coluna_final):
                    gid = layer.data[y][x]
                    tile = obter_tile(gid)

                    if tile:
                        tela.blit(tile, (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y))

    # ===== CASA =====
    tela.blit(
        casa_img,
        (
            casa_x - camera_x,
            casa_y - camera_y
        )
    )

    # ===== NPCs =====
    for npc in npcs:
        npc.desenhar(tela, camera_x, camera_y)

    # ===== JOGADOR =====
    tela.blit(
        player.sprite,
        (
            player.x - camera_x,
            player.y - camera_y
        )
    )

    # ===== DIÁLOGO =====
    if dialogo_ativo and npc_atual is not None:
        caixa = pygame.Rect(80, TELA_ALT - 180, TELA_LAR - 160, 130)

        pygame.draw.rect(tela, (20, 20, 20), caixa)
        pygame.draw.rect(tela, (255, 255, 255), caixa, 4)

        nome_texto = fonte_dialogo.render(
            npc_atual.nome,
            True,
            (255, 255, 0)
        )

        fala_texto = fonte_dialogo.render(
            npc_atual.dialogos[fala_atual],
            True,
            (255, 255, 255)
        )

        tela.blit(nome_texto, (caixa.x + 25, caixa.y + 20))
        tela.blit(fala_texto, (caixa.x + 25, caixa.y + 65))

    pygame.display.update()