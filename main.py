import pygame
from pygame.locals import *
from sys import exit

pygame.init()

# ====================
# CONFIGURAÇÕES
# ====================

# ===== Tela =====
tela_lar, tela_alt = 1366, 768
tela = pygame.display.set_mode((tela_lar, tela_alt))

clock = pygame.time.Clock()

# ===== Nome da janela =====
pygame.display.set_caption("FaunaBR")

# ===== Mapa =====
mapa_lar, mapa_alt = 3000, 3000
background = pygame.transform.scale(pygame.image.load('images/background.jpg'), (mapa_lar, mapa_alt))
x, y = 0, 0

# ===== Jogador =====
player = pygame.transform.scale(pygame.image.load('images/pombo.png'), (96,96))

# Posição inicial do jogador
player_x, player_y = mapa_lar // 2, mapa_alt // 2

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
    
    if teclas[K_w] or teclas[K_UP]:
        player_y -= velocidade
    if teclas[K_a] or teclas[K_LEFT]:
        player_x -= velocidade
    if teclas[K_s] or teclas[K_DOWN]:
        player_y += velocidade
    if teclas[K_d] or teclas[K_RIGHT]:
        player_x += velocidade
    
    # ====================
    # LIMITES DO MAPA
    # ====================
    if player_x < 0:
        player_x = 0

    if player_y < 0:
        player_y = 0

    if player_x > mapa_alt - 96:
        player_x = mapa_lar - 96

    if player_y > mapa_lar - 96:
        player_y = mapa_lar - 96

    # ====================
    # CÂMERA
    # ====================

    camera_x = player_x - tela_lar // 2
    camera_y = player_y - tela_alt // 2

    # Limites da câmera
    camera_x = max(0, min(camera_x, mapa_lar - tela_lar))
    camera_y = max(0, min(camera_y, mapa_alt - tela_alt))

    # ====================
    # DESENHO
    # ====================

    tela.blit(background, (-camera_x, -camera_y))

    tela.blit(
        player,
        (player_x - camera_x, player_y - camera_y)
    )

    pygame.display.update()