import pygame

class NPC:
    def __init__(self, imagem, x, y):
        self.imagem = pygame.transform.scale(pygame.image.load(imagem).convert_alpha(), (96, 96))
        
        self.x = x
        self.y = y
    
    def desenhar(self, tela, camera_x, camera_y):
        tela.blit(
            self.imagem,
            (self.x - camera_x, self.y - camera_y)
        )
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 96, 96)