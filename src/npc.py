import pygame

from src.config import PLAYER_TAMANHO
from src.recursos import carregar_sprite


class NPC:
    def __init__(self, nome, imagem, x, y, dialogos):
        self.nome = nome
        self.imagem = carregar_sprite(imagem, (PLAYER_TAMANHO, PLAYER_TAMANHO))

        self.x = x
        self.y = y
        self.dialogos = dialogos
        self.rect = pygame.Rect(x, y, PLAYER_TAMANHO, PLAYER_TAMANHO)
    
    def desenhar(self, tela, camera_x, camera_y):
        tela.blit(
            self.imagem,
            (self.x - camera_x, self.y - camera_y)
        )
    
    def get_rect(self):
        return self.rect