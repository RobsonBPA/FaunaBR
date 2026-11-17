"""NPCs da jornada de Ângelo no mapa da Mata Atlântica."""
from src.npc import NPC
from src.recursos import resource_path


def criar_npcs():
    elenco = (
        ("Iggy (Cachorro)", "cachorro/cachorro1.png", 400, 400),
        ("Rocky (Capivara)", "capivara/capivara_frente1.png", 720, 360),
        ("Pombo Beiçudo", "pombo/pombo_frente1.png", 2016, 1536),
        ("Scorpion (Escorpião-Amarelo)", "escorpiao/escorpiao_frente1.png", 900, 900),
        ("Blue (Arara-Azul)", "arara_azul/arara_azul_frente1.png", 3000, 2700),
    )
    return [
        NPC(
            nome,
            resource_path("assets", "images", "personagens", sprite),
            x,
            y,
            [],
        )
        for nome, sprite, x, y in elenco
    ]
