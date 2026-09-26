# ====================
# IMPORTAÇÕES
# ====================

import os
import sys
import pygame
import pytmx

from pygame.locals import QUIT, KEYDOWN, K_e
from src.player import Jogador
from src.camera import atualizar_camera
from src.npc import NPC


# ====================
# FUNÇÕES AUXILIARES
# ====================

def resource_path(*relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_path)


def carregar_sprite(caminho, tamanho=None):
    sprite = pygame.image.load(resource_path(*caminho)).convert_alpha()

    if tamanho:
        sprite = pygame.transform.scale(sprite, tamanho)

    return sprite


def criar_rect_player():
    return pygame.Rect(
        player.x,
        player.y,
        PLAYER_TAMANHO,
        PLAYER_TAMANHO
    )


def limitar_player():
    player.x = max(0, min(player.x, mapa_lar - PLAYER_TAMANHO))
    player.y = max(0, min(player.y, mapa_alt - PLAYER_TAMANHO))


def obter_tile(gid):
    if gid not in tile_cache:
        imagem = mata_atlantica.get_tile_image_by_gid(gid)

        tile_cache[gid] = (
            pygame.transform.scale(
                imagem,
                (TILE_SIZE, TILE_SIZE)
            )
            if imagem
            else None
        )

    return tile_cache[gid]


# ====================
# CONFIGURAÇÕES
# ====================

pygame.init()
pygame.mixer.init()

import pygame

TELA_LAR = 1366
TELA_ALT = 768
TILE_SIZE = 96

tela = pygame.display.set_mode((TELA_LAR, TELA_ALT))
pygame.display.set_caption("FaunaBR")

clock = pygame.time.Clock()

PLAYER_TAMANHO = 96


# ====================
# SOM
# ====================

pygame.mixer.music.load(
    resource_path(
        "assets/sounds/ambiente/trilha_sonora.mp3"
    )
)

pygame.mixer.music.play(-1)


# ====================
# MAPA
# ====================

mata_atlantica = pytmx.util_pygame.load_pygame(
    resource_path(
        "assets/images/maps/mata_atlantica.tmx"
    )
)

mapa_lar = mata_atlantica.width * TILE_SIZE
mapa_alt = mata_atlantica.height * TILE_SIZE

tile_cache = {}


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
            "Olá! Eu sou uma capivara.",
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
# MISSÃO DO POMBO
# ====================

missao_pombo_ativa = False
missao_pombo_concluida = False

lixo_coletado = 0
total_lixos = 6

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
    carregar_sprite(
        ("assets", "images", "tiles", "mata_atlantica", "cacos_vidro1.png"),
        (TILE_SIZE, TILE_SIZE)
    ),
    carregar_sprite(
        ("assets", "images", "tiles", "mata_atlantica", "cacos_vidro2.png"),
        (TILE_SIZE, TILE_SIZE)
    )
]


# ====================
# OBJETOS DE LIXO
# ====================

lixos = [
    {
        "x": x,
        "y": y,
        "sprite": lixo_sprites[i % len(lixo_sprites)],
        "coletado": False
    }
    for i, (x, y) in enumerate(posicoes_lixos)
]


# ====================
# DIÁLOGO
# ====================

fonte_dialogo = pygame.font.Font(None, 36)

dialogo_ativo = False
npc_atual = None
fala_atual = 0


# ====================
# DIÁLOGOS DO POMBO
# ====================

DIALOGO_POMBO_INICIAL = [
    "Opa... A cidade esta cheia de cacos de vidro!",
    "Voce pode me ajudar a recolher esse lixo?",
    "Procure os cacos de vidro espalhados pela cidade.",
    "Volte aqui quando terminar!"
]

DIALOGO_POMBO_ANDAMENTO = [
    "Ainda falta recolher alguns cacos.",
    "Voce recolheu {coletado} de {total}."
]

DIALOGO_POMBO_CONCLUSAO = [
    "Voce conseguiu!",
    "Todos os cacos foram recolhidos!",
    "Muito obrigado pela ajuda!"
]

DIALOGO_POMBO_FINAL = [
    "Obrigado por limpar a cidade!",
    "Voce ajudou a deixar a Mata Atlântica mais segura."
]


def atualizar_dialogo_pombo():
    if missao_pombo_concluida:
        return DIALOGO_POMBO_FINAL

    if missao_pombo_ativa and lixo_coletado >= total_lixos:
        return DIALOGO_POMBO_CONCLUSAO

    if missao_pombo_ativa:
        return [
            texto.format(
                coletado=lixo_coletado,
                total=total_lixos
            )
            for texto in DIALOGO_POMBO_ANDAMENTO
        ]

    return DIALOGO_POMBO_INICIAL


def interagir_com_npcs():
    global dialogo_ativo
    global npc_atual
    global fala_atual

    player_rect = criar_rect_player()

    for npc in npcs:
        area_interacao = npc.get_rect().inflate(80, 80)

        if player_rect.colliderect(area_interacao):
            dialogo_ativo = True
            npc_atual = npc
            fala_atual = 0

            if npc.nome == "Pombo Beiçudo":
                npc.dialogos = atualizar_dialogo_pombo()

            break


def avancar_dialogo():
    global dialogo_ativo
    global npc_atual
    global fala_atual
    global missao_pombo_ativa
    global missao_pombo_concluida

    fala_atual += 1

    if fala_atual < len(npc_atual.dialogos):
        return

    if npc_atual.nome == "Pombo Beiçudo":

        if not missao_pombo_ativa and not missao_pombo_concluida:
            missao_pombo_ativa = True

        elif missao_pombo_ativa and lixo_coletado >= total_lixos:
            missao_pombo_ativa = False
            missao_pombo_concluida = True

    dialogo_ativo = False
    npc_atual = None
    fala_atual = 0


# ====================
# COLETA DE LIXO
# ====================

def coletar_lixos():
    global lixo_coletado

    player_rect = criar_rect_player()

    for lixo in lixos:

        if lixo["coletado"]:
            continue

        lixo_rect = pygame.Rect(
            lixo["x"],
            lixo["y"],
            TILE_SIZE,
            TILE_SIZE
        )

        if player_rect.colliderect(lixo_rect):
            lixo["coletado"] = True
            lixo_coletado += 1


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
            sys.exit()

        if event.type == KEYDOWN and event.key == K_e:

            if dialogo_ativo:
                avancar_dialogo()
            else:
                interagir_com_npcs()


    # ====================
    # MOVIMENTAÇÃO
    # ====================

    if not dialogo_ativo:
        player.mover()


    # ====================
    # COLETA
    # ====================

    if missao_pombo_ativa:
        coletar_lixos()


    # ====================
    # LIMITES DO MAPA
    # ====================

    limitar_player()


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

    tela.fill((0, 0, 0))


    # ====================
    # MAPA
    # ====================

    coluna_inicial = max(
        0,
        camera_x // TILE_SIZE
    )

    coluna_final = min(
        mata_atlantica.width,
        (camera_x + TELA_LAR) // TILE_SIZE + 1
    )

    linha_inicial = max(
        0,
        camera_y // TILE_SIZE
    )

    linha_final = min(
        mata_atlantica.height,
        (camera_y + TELA_ALT) // TILE_SIZE + 1
    )

    for layer in mata_atlantica.visible_layers:

        if not hasattr(layer, "data"):
            continue

        for y in range(linha_inicial, linha_final):

            for x in range(coluna_inicial, coluna_final):

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

    if dialogo_ativo and npc_atual is not None:

        caixa = pygame.Rect(
            80,
            TELA_ALT - 180,
            TELA_LAR - 160,
            130
        )

        pygame.draw.rect(
            tela,
            (20, 20, 20),
            caixa
        )

        pygame.draw.rect(
            tela,
            (255, 255, 255),
            caixa,
            4
        )

        nome_texto = fonte_dialogo.render(
            npc_atual.nome,
            True,
            (255, 255, 0)
        )

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
    # ATUALIZA TELA
    # ====================

    pygame.display.update()