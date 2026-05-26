import pygame
from pygame.locals import *
from sys import exit

import pygame.transform

pygame.init()

# Tamanho da tela
largura, altura = 1366, 768

x, y = 0, 0

tela = pygame.display.set_mode((largura, altura)) # Criação da tela

# ===== Carregamento de imagens =====

# Background
background = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(background, (1366,768))

# Pombo
pombo = pygame.image.load('images/pombo.png')
pombo = pygame.transform.scale(pombo, (128,128))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    tela.blit(background)

    if event.type == KEYDOWN:
        if event.key == K_w or event.key == K_UP:
            y = y - 0.5
        elif event.key == K_a or event.key == K_LEFT:
            x = x - 0.5
        elif event.key == K_s or event.key == K_DOWN:
            y = y + 0.5
        elif event.key == K_d or event.key == K_RIGHT:
            x = x + 0.5

    tela.blit(pombo, (x,y))
    pygame.display.update()