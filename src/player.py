import pygame
from pygame.locals import K_a, K_d, K_s, K_w, K_DOWN, K_LEFT, K_RIGHT, K_UP

from src.config import PLAYER_TAMANHO, VELOCIDADE_JOGADOR
from src.recursos import carregar_sprite, resource_path


class Jogador:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velocidade = VELOCIDADE_JOGADOR
        self.rect = pygame.Rect(0, 0, PLAYER_TAMANHO, PLAYER_TAMANHO)
        self._resto_x = 0.0
        self._resto_y = 0.0
        self.som_passos = pygame.mixer.Sound(
            resource_path("assets/sounds/personagem/passos.mp3")
        )
        self.canal_passos = None
        self.intervalo_passos = 350
        self.ultimo_passo = 0

        TAMANHO_PLAYER = (PLAYER_TAMANHO, PLAYER_TAMANHO)

        # Sprites - Frente
        self.angelo_frente = [
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_frente1.png",
                TAMANHO_PLAYER
            ),
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_frente2.png",
                TAMANHO_PLAYER
            ),
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_frente3.png",
                TAMANHO_PLAYER
            ),
        ]

        # Sprites - Costas
        self.angelo_costas = [
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_costas1.png",
                TAMANHO_PLAYER
            ),
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_costas2.png",
                TAMANHO_PLAYER
            )
        ]

        # Sprites - Direita
        self.angelo_dir = [
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_dir1.png",
                TAMANHO_PLAYER
            ),
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_dir2.png",
                TAMANHO_PLAYER
            ),
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_dir3.png",
                TAMANHO_PLAYER
            )
        ]

        # Sprites - Esquerda
        self.angelo_esq = [
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_esq1.png",
                TAMANHO_PLAYER
            ),
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_esq2.png",
                TAMANHO_PLAYER
            ),
            carregar_sprite(
                "assets/images/personagens/angelo/angelo_esq3.png",
                TAMANHO_PLAYER
            )
        ]

        # Sprites parados
        self.angelo_parado = {
            "frente": carregar_sprite(
                "assets/images/personagens/angelo/angelo_parado_frente.png",
                TAMANHO_PLAYER
            ),

            "costas": carregar_sprite(
                "assets/images/personagens/angelo/angelo_parado_costas.png",
                TAMANHO_PLAYER
            ),

            "direita": carregar_sprite(
                "assets/images/personagens/angelo/angelo_parado_dir.png",
                TAMANHO_PLAYER
            ),

            "esquerda": carregar_sprite(
                "assets/images/personagens/angelo/angelo_parado_esq.png",
                TAMANHO_PLAYER
            )
        }

        self.sprite_atual = self.angelo_frente
        self.direcao_atual = "frente"
        self.sprite = self.angelo_parado[self.direcao_atual]

        self.frame = 0
        self.contador_animacao = 0
        self.indice_animacao = 0

        # Sequência da animação
        self.sequencia_normal = [0, 1, 0, 1, 0, 1, 2]
        self.sequencia_costas = [0, 1]

    def mover(self, dt=1 / 60):
        teclas = pygame.key.get_pressed()
        movendo = False
        deslocamento = self.velocidade * dt
        deslocamento_x = 0.0
        deslocamento_y = 0.0

        # Frente
        if teclas[K_w] or teclas[K_UP]:
            deslocamento_y -= deslocamento
            self.sprite_atual = self.angelo_costas
            self.direcao_atual = "costas"
            movendo = True

        # Trás
        if teclas[K_s] or teclas[K_DOWN]:
            deslocamento_y += deslocamento
            self.sprite_atual = self.angelo_frente
            self.direcao_atual = "frente"
            movendo = True

        # Esquerda
        if teclas[K_a] or teclas[K_LEFT]:
            deslocamento_x -= deslocamento
            self.sprite_atual = self.angelo_esq
            self.direcao_atual = "esquerda"
            movendo = True

        # Direita
        if teclas[K_d] or teclas[K_RIGHT]:
            deslocamento_x += deslocamento
            self.sprite_atual = self.angelo_dir
            self.direcao_atual = "direita"
            movendo = True

        self._mover_eixo("x", deslocamento_x)
        self._mover_eixo("y", deslocamento_y)

        if self.sprite_atual == self.angelo_costas:
            sequencia = self.sequencia_costas
        else:
            sequencia = self.sequencia_normal

        if self.frame >= len(self.sprite_atual):
            self.frame = 0
            self.indice_animacao = 0

        if movendo:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_passo >= self.intervalo_passos:
                if self.canal_passos is None or not self.canal_passos.get_busy():
                    self.canal_passos = self.som_passos.play()
                self.ultimo_passo = agora

            self.contador_animacao += dt

            if self.contador_animacao >= 1 / 6:
                self.contador_animacao -= 1 / 6

                self.indice_animacao += 1

                if self.indice_animacao >= len(sequencia):
                    self.indice_animacao = 0

                self.frame = sequencia[self.indice_animacao]

        else:
            self.parar_passos()
            self.frame = 0
            self.indice_animacao = 0
            self.contador_animacao = 0
            self.sprite = self.angelo_parado[self.direcao_atual]
            return

        self.sprite = self.sprite_atual[self.frame]

    def _mover_eixo(self, eixo, deslocamento):
        nome_resto = f"_resto_{eixo}"
        resto = getattr(self, nome_resto) + deslocamento
        pixels = int(resto)
        setattr(self, nome_resto, resto - pixels)
        setattr(self, eixo, getattr(self, eixo) + pixels)

    def sincronizar_rect(self):
        self.rect.update(self.x, self.y, PLAYER_TAMANHO, PLAYER_TAMANHO)

    def parar_passos(self):
        if self.canal_passos is not None:
            self.canal_passos.stop()
            self.canal_passos = None
        self.ultimo_passo = 0