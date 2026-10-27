import sys
from pathlib import Path

import pygame


def resource_path(*relative_path):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent
    return str(base_path.joinpath(*(str(part) for part in relative_path)))


def carregar_sprite(caminho, tamanho=None):
    partes_caminho = (caminho,) if isinstance(caminho, (str, Path)) else caminho
    sprite = pygame.image.load(resource_path(*partes_caminho)).convert_alpha()
    if tamanho:
        sprite = pygame.transform.scale(sprite, tamanho)
    return sprite