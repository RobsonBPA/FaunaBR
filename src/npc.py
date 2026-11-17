import pygame

from src.config import PLAYER_TAMANHO
from src.recursos import carregar_sprite


class NPC:
    def __init__(self, nome, imagem, x, y, dialogos):
        self.nome = nome
        self.imagem = carregar_sprite(imagem, (PLAYER_TAMANHO, PLAYER_TAMANHO)) if imagem else None
        self.visivel = True

        self.x = x
        self.y = y
        self.dialogos = dialogos
        self.rect = pygame.Rect(x, y, PLAYER_TAMANHO, PLAYER_TAMANHO)
    
    def desenhar(self, tela, camera_x, camera_y):
        if not self.visivel:
            return
        pos = (self.x - camera_x, self.y - camera_y)
        if self.imagem:
            tela.blit(self.imagem, pos)
        else:
            pygame.draw.circle(tela, (93, 151, 94), (pos[0] + 48, pos[1] + 48), 36)
            pygame.draw.circle(tela, (255, 255, 255), (pos[0] + 48, pos[1] + 48), 36, 3)
    
    def get_rect(self):
        return self.rect
