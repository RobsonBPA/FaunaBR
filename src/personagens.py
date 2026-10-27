from src.npc import NPC
from src.dialogo import DIALOGO_POMBO_INICIAL
from src.recursos import resource_path


def criar_npcs():
    return [
        NPC(
            "Capivara",
            resource_path("assets/images/personagens/capivara/capivara_frente1.png"),
            450, 3400,
            [
                "Olá! Eu sou uma capivara.",
                "Sou o maior roedor do mundo.",
                "Gosto de viver perto da agua.",
                "No Brasil, posso ser encontrada em varios biomas."
            ]
        ),
        NPC(
            "Pombo Beiçudo",
            resource_path("assets/images/personagens/pombo/pombo_frente1.png"),
            3000, 3000,
            DIALOGO_POMBO_INICIAL.copy()
        ),
        NPC(
            "Escorpião",
            resource_path("assets/images/personagens/escorpiao/escorpiao_frente1.png"),
            350, 550,
            ["Fala 1", "Fala 2", "Fala 3", "Fala 4"]
        ),
        NPC(
            "Cachorro",
            resource_path("assets/images/personagens/cachorro/cachorro1.png"),
            400, 400,
            ["Fala 1", "Fala 2", "Fala 3", "Fala 4"]
        ),
    ]