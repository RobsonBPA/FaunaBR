import pygame
from pygame.locals import *

class Jogador:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velocidade = 5

        self.sprite = pygame.transform.scale(
            pygame.image.load("assets/images/personagens/pombo/pombo_frente1.png"), (96, 96))
        
    def mover(self):
        teclas = pygame.key.get_pressed()

        # Subir
        if teclas[K_w] or teclas[K_UP]:
            self.y -= self.velocidade

        # Descer
        if teclas[K_s] or teclas[K_DOWN]:
            self.y += self.velocidade

        # Esquerda
        if teclas[K_a] or teclas[K_LEFT]:
            self.x -= self.velocidade
        
        # Direita
        if teclas[K_d] or teclas[K_RIGHT]:
            self.x += self.velocidade