import pygame
from pygame.locals import *

class Jogador:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velocidade = 5

        TAMANHO_PLAYER = (96, 96)

        # Sprites
        self.angelo_frente = [
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_frente1.png").convert_alpha(), TAMANHO_PLAYER),
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_frente2.png").convert_alpha(), TAMANHO_PLAYER),
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_frente3.png").convert_alpha(), TAMANHO_PLAYER)
        ]

        self.angelo_costas = [
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_costas1.png").convert_alpha(), TAMANHO_PLAYER),
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_costas2.png").convert_alpha(), TAMANHO_PLAYER)
        ]

        self.angelo_dir = [
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_dir1.png").convert_alpha(), TAMANHO_PLAYER),
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_dir2.png").convert_alpha(), TAMANHO_PLAYER),
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_dir3.png").convert_alpha(), TAMANHO_PLAYER)
        ]

        self.angelo_esq = [
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_esq1.png").convert_alpha(), TAMANHO_PLAYER),
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_esq2.png").convert_alpha(), TAMANHO_PLAYER),
            pygame.transform.scale(pygame.image.load("assets/images/personagens/angelo/angelo_esq3.png").convert_alpha(), TAMANHO_PLAYER)
        ]

        self.sprite_atual = self.angelo_frente
        self.sprite = self.sprite_atual[0]

        self.frame = 0
        self.contador_animacao = 0
        self.indice_animacao = 0

        # Sequência da animação
        self.sequencia_normal = [0, 1, 0, 1, 0, 1, 2] # Animação de frente, esquerda e direita
        self.sequencia_costas = [0, 1] # Animação de costas

    def mover(self):
        teclas = pygame.key.get_pressed()
        movendo = False

        # Frente
        if teclas[K_w] or teclas[K_UP]:
            self.y -= self.velocidade
            self.sprite_atual = self.angelo_costas
            movendo = True

        # Trás
        if teclas[K_s] or teclas[K_DOWN]:
            self.y += self.velocidade
            self.sprite_atual = self.angelo_frente
            movendo = True

        if teclas[K_a] or teclas[K_LEFT]:
            self.x -= self.velocidade
            self.sprite_atual = self.angelo_esq
            movendo = True

        # Direita
        if teclas[K_d] or teclas[K_RIGHT]:
            self.x += self.velocidade
            self.sprite_atual = self.angelo_dir
            movendo = True

        # Esquerda
        if self.sprite_atual == self.angelo_costas:
            sequencia = self.sequencia_costas
        else:
            sequencia = self.sequencia_normal

        if movendo:
            self.contador_animacao += 1

            if self.contador_animacao >= 10:
                self.contador_animacao = 0

                self.indice_animacao += 1

                if self.indice_animacao >= len(sequencia):
                    self.indice_animacao = 0

                self.frame = sequencia[self.indice_animacao]
        else:
            self.frame = 0
            self.indice_animacao = 0
            self.contador_animacao = 0

        self.sprite = self.sprite_atual[self.frame]