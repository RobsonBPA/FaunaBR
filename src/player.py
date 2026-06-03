import pygame
from pygame.locals import *

class Jogador:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velocidade = 5
        
        TAMANHO_POMBO = (96, 96)
        self.pombo_frente = pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_frente1.png").convert_alpha(), TAMANHO_POMBO), pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_frente2.png").convert_alpha(), TAMANHO_POMBO),
        self.pombo_costas = pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_costas1.png").convert_alpha(), TAMANHO_POMBO), pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_costas2.png").convert_alpha(), TAMANHO_POMBO),
        self.pombo_dir = pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_dir1.png").convert_alpha(), TAMANHO_POMBO), pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_dir2.png").convert_alpha(), TAMANHO_POMBO),
        self.pombo_esq = pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_esq1.png").convert_alpha(), TAMANHO_POMBO), pygame.transform.scale(pygame.image.load("assets/images/personagens/pombo/pombo_esq2.png").convert_alpha(), TAMANHO_POMBO),

        self.frame = 0
        self.contador_animacao = 0
        self.sprite_atual = self.pombo_frente

        # self.sprite = pygame.transform.scale(
        #     pygame.image.load("assets/images/personagens/pombo/pombo_frente1.png"), (96, 96))
        
    def mover(self):
        teclas = pygame.key.get_pressed()
        movendo = False

        # Subir
        if teclas[K_w] or teclas[K_UP]:
            self.y -= self.velocidade
            self.sprite_atual = self.pombo_costas
            movendo = True

        # Descer
        if teclas[K_s] or teclas[K_DOWN]:
            self.y += self.velocidade
            self.sprite_atual = self.pombo_frente
            movendo = True

        # Esquerda
        if teclas[K_a] or teclas[K_LEFT]:
            self.x -= self.velocidade
            self.sprite_atual = self.pombo_esq
            movendo = True
        
        # Direita
        if teclas[K_d] or teclas[K_RIGHT]:
            self.x += self.velocidade
            self.sprite_atual = self.pombo_dir
            movendo = True

        if movendo:
            self.contador_animacao += 1

            if self.contador_animacao >= 15:  # velocidade da animação
                self.contador_animacao = 0
                self.frame = (self.frame + 1) % 2
        else:
            frame = 0  # parado mostra a imagem 1
            
        self.sprite = self.sprite_atual[self.frame]