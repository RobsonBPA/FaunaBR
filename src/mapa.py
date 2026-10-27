from collections import OrderedDict

import pygame
import pytmx

from src.recursos import resource_path


class Mapa:
    TAMANHO_BLOCO_TILES = 8
    MAX_BLOCOS_CACHE = 12

    def __init__(self, caminho, tamanho_tile):
        self.tmx = pytmx.util_pygame.load_pygame(resource_path(caminho))
        self.tamanho_tile = tamanho_tile
        self.largura = self.tmx.width * tamanho_tile
        self.altura = self.tmx.height * tamanho_tile
        self._tiles = {}
        self._blocos = OrderedDict()
        self._camadas_visiveis = tuple(
            layer for layer in self.tmx.visible_layers if hasattr(layer, "data")
        )
        self._tamanho_bloco = self.TAMANHO_BLOCO_TILES * tamanho_tile

    def _obter_tile(self, gid):
        if gid not in self._tiles:
            imagem = self.tmx.get_tile_image_by_gid(gid)
            self._tiles[gid] = (
                pygame.transform.scale(
                    imagem,
                    (self.tamanho_tile, self.tamanho_tile)
                )
                if imagem else None
            )
        return self._tiles[gid]

    def _construir_bloco(self, bloco_x, bloco_y):
        inicio_x = bloco_x * self.TAMANHO_BLOCO_TILES
        inicio_y = bloco_y * self.TAMANHO_BLOCO_TILES
        fim_x = min(inicio_x + self.TAMANHO_BLOCO_TILES, self.tmx.width)
        fim_y = min(inicio_y + self.TAMANHO_BLOCO_TILES, self.tmx.height)
        largura = (fim_x - inicio_x) * self.tamanho_tile
        altura = (fim_y - inicio_y) * self.tamanho_tile
        bloco = pygame.Surface((largura, altura), pygame.SRCALPHA).convert_alpha()

        for layer in self._camadas_visiveis:
            for y in range(inicio_y, fim_y):
                for x in range(inicio_x, fim_x):
                    gid = layer.data[y][x]
                    if not gid:
                        continue

                    tile = self._obter_tile(gid)
                    if tile:
                        bloco.blit(
                            tile,
                            (
                                (x - inicio_x) * self.tamanho_tile,
                                (y - inicio_y) * self.tamanho_tile
                            )
                        )
        return bloco

    def _obter_bloco(self, bloco_x, bloco_y):
        chave = (bloco_x, bloco_y)
        bloco = self._blocos.get(chave)
        if bloco is None:
            bloco = self._construir_bloco(bloco_x, bloco_y)
            self._blocos[chave] = bloco
            if len(self._blocos) > self.MAX_BLOCOS_CACHE:
                self._blocos.popitem(last=False)
        else:
            self._blocos.move_to_end(chave)
        return bloco

    def desenhar(self, tela, camera_x, camera_y, largura_tela, altura_tela):
        primeiro_x = max(0, camera_x // self._tamanho_bloco)
        primeiro_y = max(0, camera_y // self._tamanho_bloco)
        ultimo_x = min(
            (self.tmx.width - 1) // self.TAMANHO_BLOCO_TILES,
            (camera_x + largura_tela - 1) // self._tamanho_bloco
        )
        ultimo_y = min(
            (self.tmx.height - 1) // self.TAMANHO_BLOCO_TILES,
            (camera_y + altura_tela - 1) // self._tamanho_bloco
        )

        for bloco_y in range(primeiro_y, ultimo_y + 1):
            for bloco_x in range(primeiro_x, ultimo_x + 1):
                bloco = self._obter_bloco(bloco_x, bloco_y)
                tela.blit(
                    bloco,
                    (
                        bloco_x * self._tamanho_bloco - camera_x,
                        bloco_y * self._tamanho_bloco - camera_y
                    )
                )