import pygame

from src.dialogo import atualizar_dialogo_pombo
from src.recursos import carregar_sprite


class MissaoPombo:
    POSICOES_LIXOS = [
        (2500, 2800),
        (2800, 3200),
        (3200, 2700),
        (3500, 3100),
        (3800, 3500),
        (4200, 3000),
    ]

    def __init__(self, tamanho_tile):
        self.ativa = False
        self.concluida = False
        self.total_lixos = len(self.POSICOES_LIXOS)
        self.lixo_coletado = 0
        self._contador_exibido = None
        self._texto_contador = None
        sprites = [
            carregar_sprite(
                ("assets", "images", "tiles", "mata_atlantica", nome),
                (tamanho_tile, tamanho_tile)
            )
            for nome in ("cacos_vidro1.png", "cacos_vidro2.png")
        ]
        self.lixos = [
            {
                "x": x,
                "y": y,
                "sprite": sprites[indice % len(sprites)],
                "rect": pygame.Rect(x, y, tamanho_tile, tamanho_tile),
                "coletado": False,
            }
            for indice, (x, y) in enumerate(self.POSICOES_LIXOS)
        ]

    def dialogos(self):
        return atualizar_dialogo_pombo(
            self.ativa,
            self.concluida,
            self.lixo_coletado,
            self.total_lixos
        )

    def finalizar_dialogo(self):
        if not self.ativa and not self.concluida:
            self.ativa = True
        elif self.ativa and self.lixo_coletado >= self.total_lixos:
            self.ativa = False
            self.concluida = True

    def coletar(self, player_rect):
        for lixo in self.lixos:
            if lixo["coletado"]:
                continue

            if player_rect.colliderect(lixo["rect"]):
                lixo["coletado"] = True
                self.lixo_coletado += 1

    def desenhar_lixos(self, tela, camera_x, camera_y):
        for lixo in self.lixos:
            if not lixo["coletado"]:
                tela.blit(
                    lixo["sprite"],
                    (lixo["x"] - camera_x, lixo["y"] - camera_y)
                )

    def desenhar_contador(self, tela, fonte):
        if not self.ativa:
            return

        if self._texto_contador is None or self._contador_exibido != self.lixo_coletado:
            self._texto_contador = fonte.render(
                f"Cacos recolhidos: {self.lixo_coletado}/{self.total_lixos}",
                True,
                (255, 255, 255)
            )
            self._contador_exibido = self.lixo_coletado
        tela.blit(self._texto_contador, (20, 20))