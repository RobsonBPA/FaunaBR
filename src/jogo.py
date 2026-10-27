import pygame
from pygame.locals import K_e, KEYDOWN, QUIT

from src.camera import atualizar_camera
from src.config import (
    FPS,
    PLAYER_TAMANHO,
    TELA_ALT,
    TELA_LAR,
    TILE_SIZE,
    VOLUME_TRILHA,
)
from src.dialogo import GerenciadorDialogo
from src.mapa import Mapa
from src.missao import MissaoPombo
from src.personagens import criar_npcs
from src.player import Jogador
from src.recursos import resource_path


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.tela = pygame.display.set_mode((TELA_LAR, TELA_ALT))
        pygame.display.set_caption("FaunaBR")
        self.clock = pygame.time.Clock()
        self.executando = True

        pygame.mixer.music.load(
            resource_path("assets", "sounds", "ambiente", "trilha_sonora.mp3")
        )
        pygame.mixer.music.set_volume(VOLUME_TRILHA)
        pygame.mixer.music.play(-1)

        self.mapa = Mapa("assets/images/maps/mata_atlantica.tmx", TILE_SIZE)
        self.jogador = Jogador()
        self.jogador.x = self.mapa.largura // 2
        self.jogador.y = self.mapa.altura // 2
        self.jogador.sincronizar_rect()
        self.npcs = criar_npcs()
        self.missao = MissaoPombo(TILE_SIZE)
        self.dialogo = GerenciadorDialogo()
        self.fonte = pygame.font.Font(None, 36)

    def _limitar_jogador(self):
        self.jogador.x = max(
            0,
            min(self.jogador.x, self.mapa.largura - PLAYER_TAMANHO)
        )
        self.jogador.y = max(
            0,
            min(self.jogador.y, self.mapa.altura - PLAYER_TAMANHO)
        )

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == QUIT:
                self.executando = False
            elif evento.type == KEYDOWN and evento.key == K_e:
                self._interagir()

    def _interagir(self):
        if self.dialogo.ativo:
            npc_finalizado = self.dialogo.avancar()
            if npc_finalizado == "Pombo Beiçudo":
                self.missao.finalizar_dialogo()
            return

        self.dialogo.iniciar(
            self.npcs,
            self.jogador.rect,
            self.missao.dialogos()
        )

    def _atualizar(self, dt):
        if self.dialogo.ativo:
            self.jogador.parar_passos()
        else:
            self.jogador.mover(dt)

        self.jogador.sincronizar_rect()
        if self.missao.ativa:
            self.missao.coletar(self.jogador.rect)

        self._limitar_jogador()
        self.jogador.sincronizar_rect()

    def _desenhar(self):
        camera_x, camera_y = atualizar_camera(
            self.jogador.x,
            self.jogador.y,
            TELA_LAR,
            TELA_ALT,
            self.mapa.largura,
            self.mapa.altura
        )

        self.tela.fill((0, 0, 0))
        self.mapa.desenhar(
            self.tela, camera_x, camera_y, TELA_LAR, TELA_ALT
        )
        self.missao.desenhar_lixos(self.tela, camera_x, camera_y)

        for npc in self.npcs:
            npc.desenhar(self.tela, camera_x, camera_y)

        self.tela.blit(
            self.jogador.sprite,
            (self.jogador.x - camera_x, self.jogador.y - camera_y)
        )
        self.missao.desenhar_contador(self.tela, self.fonte)
        self.dialogo.desenhar(self.tela, self.fonte, TELA_LAR, TELA_ALT)
        pygame.display.flip()

    def executar(self):
        try:
            while self.executando:
                elapsed = self.clock.tick(FPS) / 1000
                dt = min(elapsed, 0.05)
                self._processar_eventos()
                if not self.executando:
                    break
                self._atualizar(dt)
                self._desenhar()
        finally:
            self.jogador.parar_passos()
            pygame.quit()


def main():
    Jogo().executar()