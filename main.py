# ====================
# IMPORTAÇÕES
# ====================

import os
import sys

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


import pygame
from pygame.locals import *
from sys import exit

import pytmx
from pytmx.util_pygame import load_pygame

from src.player import Jogador
from src.camera import atualizar_camera
from src.config import *
from src.npc import NPC


pygame.init()


# ====================
# CONFIGURAÇÕES
# ====================

tela = pygame.display.set_mode((TELA_LAR, TELA_ALT))
pygame.display.set_caption("FaunaBR")

clock = pygame.time.Clock()


# ====================
# MAPA TILED
# ====================

mata_atlantica = pytmx.util_pygame.load_pygame(
    resource_path("assets/images/maps/mata_atlantica.tmx")
)

# mata_atlantica = load_pygame(
#     "assets/images/maps/mata_atlantica.tmx"
# )

mapa_lar = mata_atlantica.width * TILE_SIZE
mapa_alt = mata_atlantica.height * TILE_SIZE


tile_cache = {}


def obter_tile(gid):

    if gid not in tile_cache:

        imagem = mata_atlantica.get_tile_image_by_gid(gid)

        if imagem is None:

            tile_cache[gid] = None

        else:

            tile_cache[gid] = pygame.transform.scale(
                imagem,
                (TILE_SIZE, TILE_SIZE)
            )

    return tile_cache[gid]


# ====================
# JOGADOR
# ====================

player = Jogador()

player.x = mapa_lar // 2
player.y = mapa_alt // 2


# ====================
# NPCs
# ====================

npcs = [

    NPC(
        "Capivara",
        resource_path(
            "assets/images/personagens/capivara/capivara_frente1.png"
        ),
        450,
        3400,
        [
            "Ola! Eu sou uma capivara.",
            "Sou o maior roedor do mundo.",
            "Gosto de viver perto da agua.",
            "No Brasil, posso ser encontrada em varios biomas."
        ]
    ),

    NPC(
        "Pombo Beiçudo",
        resource_path(
            "assets/images/personagens/pombo/pombo_frente1.png"
        ),
        3000,
        3000,
        [
            "Opa... A cidade esta cheia de cacos de vidro!",
            "Voce pode me ajudar a recolher esse lixo?",
            "Procure os cacos de vidro espalhados pela cidade.",
            "Volte aqui quando terminar!"
        ]
    ),

    NPC(
        "Escorpião",
        resource_path(
            "assets/images/personagens/escorpiao/escorpiao_frente1.png"
        ),
        350,
        550,
        [
            "Fala 1",
            "Fala 2",
            "Fala 3",
            "Fala 4"
        ]
    ),

    NPC(
        "Cachorro",
        resource_path(
            "assets/images/personagens/cachorro/cachorro1.png"
        ),
        400,
        400,
        [
            "Fala 1",
            "Fala 2",
            "Fala 3",
            "Fala 4"
        ]
    ),
]


# ====================
# MISSÃO DO POMBO BEIÇUDO
# ====================

missao_pombo_ativa = False
missao_pombo_concluida = False

lixo_coletado = 0
total_lixos = 6


# ====================
# POSIÇÕES DOS LIXOS
# ====================

posicoes_lixos = [

    (2500, 2800),
    (2800, 3200),
    (3200, 2700),
    (3500, 3100),
    (3800, 3500),
    (4200, 3000),

]


# ====================
# SPRITES DOS CACOS
# ====================

lixo_sprites = [

    pygame.image.load(
        resource_path(
            "assets/images/tiles/mata_atlantica/cacos_vidro1.png"
        )
    ).convert_alpha(),

    pygame.image.load(
        resource_path(
            "assets/images/tiles/mata_atlantica/cacos_vidro2.png"
        )
    ).convert_alpha()

]


# ====================
# REDIMENSIONAMENTO DOS CACOS
# ====================

lixo_sprites = [

    pygame.transform.scale(
        sprite,
        (TILE_SIZE, TILE_SIZE)
    )

    for sprite in lixo_sprites

]


# ====================
# CRIAÇÃO DOS OBJETOS DE LIXO
# ====================

lixos = []


for i, (x, y) in enumerate(posicoes_lixos):

    lixos.append({

        "x": x,
        "y": y,

        "sprite": lixo_sprites[i % 2],

        "coletado": False

    })


# ====================
# DIÁLOGO
# ====================

fonte_dialogo = pygame.font.Font(
    None,
    36
)

dialogo_ativo = False

npc_atual = None

fala_atual = 0


# ====================
# LOOP PRINCIPAL
# ====================

while True:

    clock.tick(60)


    # ====================
    # EVENTOS
    # ====================

    for event in pygame.event.get():

        if event.type == QUIT:

            pygame.quit()
            exit()


        if event.type == KEYDOWN:

            if event.key == K_e:

                # ====================
                # AVANÇAR DIÁLOGO
                # ====================

                if dialogo_ativo:

                    fala_atual += 1


                    # ====================
                    # FINAL DO DIÁLOGO
                    # ====================

                    if fala_atual >= len(npc_atual.dialogos):


                        # ====================
                        # POMBO BEIÇUDO
                        # ====================

                        if npc_atual.nome == "Pombo Beiçudo":


                            # Inicia a missão
                            if (
                                not missao_pombo_ativa
                                and not missao_pombo_concluida
                            ):

                                missao_pombo_ativa = True


                            # Conclui a missão
                            elif (
                                missao_pombo_ativa
                                and lixo_coletado >= total_lixos
                            ):

                                missao_pombo_ativa = False
                                missao_pombo_concluida = True


                        dialogo_ativo = False

                        npc_atual = None

                        fala_atual = 0


                # ====================
                # INICIAR DIÁLOGO
                # ====================

                else:

                    player_rect = pygame.Rect(
                        player.x,
                        player.y,
                        96,
                        96
                    )


                    for npc in npcs:

                        area_interacao = npc.get_rect().inflate(
                            80,
                            80
                        )


                        if player_rect.colliderect(
                            area_interacao
                        ):

                            dialogo_ativo = True

                            npc_atual = npc

                            fala_atual = 0


                            # ====================
                            # DIÁLOGOS DO POMBO
                            # ====================

                            if npc.nome == "Pombo Beiçudo":


                                # Missão já concluída
                                if missao_pombo_concluida:

                                    npc.dialogos = [

                                        "Obrigado por limpar a cidade!",

                                        "Voce ajudou a deixar a Mata Atlantica mais segura."

                                    ]


                                # Todos os lixos foram coletados
                                elif (
                                    missao_pombo_ativa
                                    and lixo_coletado >= total_lixos
                                ):

                                    npc.dialogos = [

                                        "Voce conseguiu!",

                                        "Todos os cacos foram recolhidos!",

                                        "Muito obrigado pela ajuda!"

                                    ]


                                # Missão em andamento
                                elif missao_pombo_ativa:

                                    npc.dialogos = [

                                        "Ainda falta recolher alguns cacos.",

                                        f"Voce recolheu {lixo_coletado} de {total_lixos}."

                                    ]


                                # Missão ainda não começou
                                else:

                                    npc.dialogos = [

                                        "Opa... A cidade esta cheia de cacos de vidro!",

                                        "Voce pode me ajudar a recolher esse lixo?",

                                        "Procure os cacos de vidro espalhados pela cidade.",

                                        "Volte aqui quando terminar!"

                                    ]


                            break


    # ====================
    # MOVIMENTAÇÃO
    # ====================

    x_antigo = player.x
    y_antigo = player.y


    if not dialogo_ativo:

        player.mover()


    # ====================
    # COLETA DE LIXO
    # ====================

    if missao_pombo_ativa:

        player_rect = pygame.Rect(
            player.x,
            player.y,
            96,
            96
        )


        for lixo in lixos:

            # Ignora lixo já coletado
            if lixo["coletado"]:

                continue


            lixo_rect = pygame.Rect(
                lixo["x"],
                lixo["y"],
                TILE_SIZE,
                TILE_SIZE
            )


            # Jogador encostou no lixo
            if player_rect.colliderect(
                lixo_rect
            ):

                lixo["coletado"] = True

                lixo_coletado += 1


    # ====================
    # LIMITES DO MAPA
    # ====================

    if player.x < 0:

        player.x = 0


    if player.y < 0:

        player.y = 0


    if player.x > mapa_lar - 96:

        player.x = mapa_lar - 96


    if player.y > mapa_alt - 96:

        player.y = mapa_alt - 96


    # ====================
    # CÂMERA
    # ====================

    camera_x, camera_y = atualizar_camera(

        player.x,
        player.y,

        TELA_LAR,
        TELA_ALT,

        mapa_lar,
        mapa_alt

    )


    # ====================
    # DESENHO
    # ====================

    tela.fill(
        (0, 0, 0)
    )


    # ====================
    # MAPA
    # ====================

    coluna_inicial = camera_x // TILE_SIZE

    coluna_final = (
        camera_x + TELA_LAR
    ) // TILE_SIZE + 1


    linha_inicial = camera_y // TILE_SIZE

    linha_final = (
        camera_y + TELA_ALT
    ) // TILE_SIZE + 1


    coluna_inicial = max(
        0,
        coluna_inicial
    )

    linha_inicial = max(
        0,
        linha_inicial
    )


    coluna_final = min(
        mata_atlantica.width,
        coluna_final
    )

    linha_final = min(
        mata_atlantica.height,
        linha_final
    )


    for layer in mata_atlantica.visible_layers:

        if hasattr(layer, "data"):

            for y in range(
                linha_inicial,
                linha_final
            ):

                for x in range(
                    coluna_inicial,
                    coluna_final
                ):

                    gid = layer.data[y][x]

                    tile = obter_tile(gid)


                    if tile:

                        tela.blit(

                            tile,

                            (
                                x * TILE_SIZE - camera_x,
                                y * TILE_SIZE - camera_y
                            )

                        )


    # ====================
    # LIXOS
    # ====================

    for lixo in lixos:

        if not lixo["coletado"]:

            tela.blit(

                lixo["sprite"],

                (
                    lixo["x"] - camera_x,
                    lixo["y"] - camera_y
                )

            )

    # ====================
    # NPCs
    # ====================

    for npc in npcs:

        npc.desenhar(
            tela,
            camera_x,
            camera_y
        )


    # ====================
    # JOGADOR
    # ====================

    tela.blit(

        player.sprite,

        (
            player.x - camera_x,
            player.y - camera_y
        )

    )


    # ====================
    # CONTADOR DA MISSÃO
    # ====================

    if missao_pombo_ativa:

        texto_missao = fonte_dialogo.render(

            f"Cacos recolhidos: {lixo_coletado}/{total_lixos}",

            True,

            (255, 255, 255)

        )


        tela.blit(

            texto_missao,

            (20, 20)

        )


    # ====================
    # DIÁLOGO
    # ====================

    if (
        dialogo_ativo
        and npc_atual is not None
    ):

        caixa = pygame.Rect(

            80,
            TELA_ALT - 180,
            TELA_LAR - 160,
            130

        )


        # Fundo da caixa
        pygame.draw.rect(

            tela,

            (20, 20, 20),

            caixa

        )


        # Borda da caixa
        pygame.draw.rect(

            tela,

            (255, 255, 255),

            caixa,

            4

        )


        # Nome do NPC
        nome_texto = fonte_dialogo.render(

            npc_atual.nome,

            True,

            (255, 255, 0)

        )


        # Fala do NPC
        fala_texto = fonte_dialogo.render(

            npc_atual.dialogos[fala_atual],

            True,

            (255, 255, 255)

        )


        tela.blit(

            nome_texto,

            (
                caixa.x + 25,
                caixa.y + 20
            )

        )


        tela.blit(

            fala_texto,

            (
                caixa.x + 25,
                caixa.y + 65
            )

        )


    # ====================
    # ATUALIZA A TELA
    # ====================

    pygame.display.update()