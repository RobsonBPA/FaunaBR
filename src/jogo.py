from pathlib import Path
import os
import shutil
import tempfile
import webbrowser

import pygame
from pygame.locals import K_e, KEYDOWN, QUIT

from src.camera import atualizar_camera
from src.config import FPS, PLAYER_TAMANHO, TELA_ALT, TELA_LAR, TILE_SIZE, VOLUME_TRILHA
from src.dialogo import GerenciadorDialogo
from src.mapa import Mapa
from src.missao import GerenciadorMissoes
from src.personagens import criar_npcs
from src.player import Jogador
from src.recursos import resource_path


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((TELA_LAR, TELA_ALT))
        pygame.display.set_caption("Guardiões da Fauna Brasileira — A Última Prova")
        self.clock = pygame.time.Clock()
        self.executando = True
        pygame.mixer.music.load(resource_path("assets", "sounds", "ambiente", "trilha_sonora.mp3"))
        pygame.mixer.music.set_volume(VOLUME_TRILHA)
        pygame.mixer.music.play(-1)
        self.mapa = Mapa("assets/images/maps/mata_atlantica.tmx", TILE_SIZE)
        self.jogador = Jogador()
        self.jogador.x = self.mapa.largura // 2
        self.jogador.y = self.mapa.altura // 2
        self.jogador.sincronizar_rect()
        self.npcs = criar_npcs()
        self.missoes = GerenciadorMissoes(TILE_SIZE)
        self.missoes.definir_npcs(self.npcs)
        self.dialogo = GerenciadorDialogo()
        self.fonte = pygame.font.Font(None, 30)
        self._aviso = "WASD/setas: mover; E: conversar; caminhe até os resíduos para recolhê-los"
        self._aviso_ate = pygame.time.get_ticks() + 7000
        self._aviso_renderizado = None
        self._superficie_aviso = None
        self._tamanho_aviso = (0, 0)
        self._creditos_iniciados = False

    def _limitar_jogador(self):
        self.jogador.x = max(0, min(self.jogador.x, self.mapa.largura - PLAYER_TAMANHO))
        self.jogador.y = max(0, min(self.jogador.y, self.mapa.altura - PLAYER_TAMANHO))

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == QUIT:
                self.executando = False
            elif evento.type == KEYDOWN:
                if evento.key == K_e:
                    self._interagir()

    def _interagir(self):
        if self.dialogo.ativo:
            nome = self.dialogo.avancar()
            if nome:
                self.missoes.fim_dialogo(nome)
                self._notificar_conclusoes()
            return
        if self.dialogo.iniciar(self.npcs, self.jogador.rect, self.missoes.dialogos_npc):
            return
        if self.missoes.interagir_alvo(self.jogador.rect):
            if self.missoes.dialogo_extra:
                self._aviso = self.missoes.dialogo_extra[0]
                self._aviso_ate = pygame.time.get_ticks() + 4500
            return
        self._aviso = "Aproxime-se de um personagem ou marcador para interagir."
        self._aviso_ate = pygame.time.get_ticks() + 2500

    def _atualizar(self, dt):
        if self.dialogo.ativo:
            self.jogador.parar_passos()
        else:
            self.jogador.mover(dt)
        self.jogador.sincronizar_rect()
        self.missoes.atualizar(self.jogador.rect)
        if self.missoes.consumir_descoberta():
            self._aviso = "Você encontrou o escorpião-amarelo! Aproxime-se e pressione E para conversar, sem tocar nele."
            self._aviso_ate = pygame.time.get_ticks() + 5500
        self._notificar_conclusoes()
        self._limitar_jogador()
        self.jogador.sincronizar_rect()

    def _notificar_conclusoes(self):
        conclusoes = self.missoes.consumir_conclusoes()
        if not conclusoes:
            return
        titulo = conclusoes[-1]
        quantidade = self.missoes.chave_angelo()
        self._aviso = f"Missão concluída: {titulo}. Peça da Chave do Conhecimento {quantidade}/5."
        self._aviso_ate = pygame.time.get_ticks() + 5500
        if quantidade == 5:
            self._iniciar_creditos_finais()

    def _iniciar_creditos_finais(self):
        """Abre os créditos uma única vez no reprodutor padrão do sistema."""
        if self._creditos_iniciados:
            return
        self._creditos_iniciados = True
        caminho_video = Path(resource_path("assets", "sounds", "CreditosFinais.mp4"))
        if not caminho_video.is_file():
            self._aviso = "Missões concluídas, mas CreditosFinais.mp4 não foi encontrado."
            self._aviso_ate = pygame.time.get_ticks() + 7000
            return

        try:
            # O caminho temporário também funciona com o executável --onefile.
            video_estavel = Path(tempfile.gettempdir()) / "FaunaBR_CreditosFinais.mp4"
            shutil.copyfile(caminho_video, video_estavel)
            if hasattr(os, "startfile"):
                os.startfile(str(video_estavel))
            else:
                webbrowser.open(video_estavel.as_uri())
        except OSError:
            self._aviso = "Missões concluídas, mas não foi possível abrir o vídeo de créditos."
            self._aviso_ate = pygame.time.get_ticks() + 7000
            return

        pygame.mixer.music.stop()
        self.executando = False

    def _desenhar_aviso(self):
        if self._aviso_renderizado != self._aviso:
            largura_texto = min(TELA_LAR - 72, 720)
            linhas = []
            linha_atual = ""
            for palavra in self._aviso.split():
                tentativa = f"{linha_atual} {palavra}".strip()
                if linha_atual and self.fonte.size(tentativa)[0] > largura_texto:
                    linhas.append(linha_atual)
                    linha_atual = palavra
                else:
                    linha_atual = tentativa
            if linha_atual:
                linhas.append(linha_atual)

            textos = [self.fonte.render(linha, True, (255, 255, 180)) for linha in linhas]
            largura = max((texto.get_width() for texto in textos), default=0) + 32
            altura = len(textos) * self.fonte.get_linesize() + 20
            painel = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(painel, (18, 24, 28, 225), painel.get_rect(), border_radius=8)
            pygame.draw.rect(painel, (235, 220, 150, 230), painel.get_rect(), 2, border_radius=8)
            for indice, texto in enumerate(textos):
                painel.blit(texto, (16, 10 + indice * self.fonte.get_linesize()))

            self._superficie_aviso = painel
            self._tamanho_aviso = (largura, altura)
            self._aviso_renderizado = self._aviso

        largura, altura = self._tamanho_aviso
        x = 20
        if self.dialogo.ativo:
            y = TELA_ALT - 180 - altura - 12
        else:
            y = TELA_ALT - altura - 20
        y = max(12, y)
        x = min(x, TELA_LAR - largura - 12)
        self.tela.blit(self._superficie_aviso, (x, y))

    def _desenhar(self):
        camera_x, camera_y = atualizar_camera(self.jogador.x, self.jogador.y, TELA_LAR, TELA_ALT, self.mapa.largura, self.mapa.altura)
        self.tela.fill((0, 0, 0))
        self.mapa.desenhar(self.tela, camera_x, camera_y, TELA_LAR, TELA_ALT)
        self.missoes.desenhar(self.tela, camera_x, camera_y, self.fonte)
        for npc in self.npcs:
            npc.desenhar(self.tela, camera_x, camera_y)
        self.tela.blit(self.jogador.sprite, (self.jogador.x-camera_x, self.jogador.y-camera_y))
        self.missoes.desenhar_hud(self.tela, self.fonte)
        if pygame.time.get_ticks() < self._aviso_ate:
            self._desenhar_aviso()
        self.dialogo.desenhar(self.tela, self.fonte, TELA_LAR, TELA_ALT)
        pygame.display.flip()

    def executar(self):
        try:
            while self.executando:
                dt = min(self.clock.tick(FPS) / 1000, 0.05)
                self._processar_eventos()
                if not self.executando: break
                self._atualizar(dt)
                if not self.executando: break
                self._desenhar()
        finally:
            self.jogador.parar_passos()
            pygame.quit()


def main():
    Jogo().executar()
