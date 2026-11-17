"""Missões exploratórias da jornada de Ângelo."""
from __future__ import annotations

import pygame

# Coordenadas em pixels do mapa atual (50 x 50 tiles de 96 px).
# Como o TMX não nomeia as regiões, os limites são mantidos aqui para ajuste simples.
REGIOES = {
    # O lixão ocupa a área superior esquerda antes marcada como praça.
    "lixao": pygame.Rect(384, 576, 1152, 768),
    # Praça central junto à estátua (GID 2684354584), à esquerda do campo.
    "praca": pygame.Rect(900, 1500, 775, 900),
    "campo": pygame.Rect(2784, 1440, 1920, 960),
    "mata": pygame.Rect(1728, 0, 3072, 576),
    "lagoa": pygame.Rect(3744, 336, 240, 192),
}

MISSOES = [
    {
        "id": "cidade",
        "npc": "Iggy (Cachorro)",
        "titulo": "Conhecendo a região",
        "objetivos": [
            ("lixao", "Lixão"),
            ("praca", "Praça"),
            ("campo", "Campo de futebol"),
        ],
        "inicio": [
            "Oi, Angelo! Vamos conhecer melhor os lugares da cidade.",
            "Visite o lixão, a praça e o campo de futebol. Cada visita conta como um objetivo.",
            "Minha espécie é bastante popular e presente na vida dos brasileiros!",
        ],
    },
    {
        "id": "aguas",
        "npc": "Rocky (Capivara)",
        "titulo": "De volta à água",
        "seguir": "lagoa",
        "inicio": [
            "Estou longe do ambiente de que preciso. Você pode me acompanhar até a lagoa na mata?",
            "Use E para iniciar e caminhe até a lagoa marcada. Eu vou acompanhar você.",
            "Não me leve ao mar: capivaras vivem associadas à água doce.",
        ],
        "dica": "Capivaras são herbívoras e vivem perto da água, que usam para se abrigar e se deslocar.",
    },
    {
        "id": "pombo",
        "npc": "Pombo Beiçudo",
        "titulo": "Praça mais limpa",
        "inicio": [
            "A praça está cheia de resíduos. Você pode ajudar a recolher o lixo?",
            "Procure garrafas, papéis e latinhas pela praça. Encoste em cada objeto para recolhê-lo.",
        ],
        "dica": "Recolher resíduos ajuda a manter o ambiente urbano mais seguro para pessoas e animais.",
    },
    {
        "id": "escondidos",
        "npc": "Scorpion (Escorpião-Amarelo)",
        "titulo": "Encontre o escorpião",
        "inicio": [
            "Você me encontrou! Escorpiões podem se abrigar em locais escuros e protegidos.",
            "Observe de longe. Não toque nem tente capturar; cuidado com entulhos, calçados e frestas.",
            "Se houver picada, lave com água e sabão e procure atendimento médico sem demora.",
        ],
        "dica": "O escorpião-amarelo costuma ter atividade noturna. A observação deve ser feita à distância e com segurança.",
    },
    {
        "id": "arara_retorno",
        "npc": "Blue (Arara-Azul)",
        "titulo": "De volta à floresta",
        "seguir": "mata",
        "inicio": [
            "Estou na cidade e preciso voltar a um ambiente natural. Você pode me acompanhar até a floresta?",
            "Sou visitante de outro bioma, não sou típica da Mata Atlântica.",
            "Acompanhe-me até o ponto seguro na floresta ao norte; uma equipe me levará ao ambiente adequado.",
            "Use E para começar e siga o marcador verde.",
        ],
        "dica": "A arara-azul ocorre em outros biomas brasileiros, como Pantanal, Cerrado e Amazônia. Cada espécie depende de ambientes adequados.",
    },
]

MISSOES_PRINCIPAIS = tuple(missao["id"] for missao in MISSOES)
QUANTIDADE_RESIDUOS = 6


def _novo_estado():
    return {
        missao["id"]: {
            "iniciada": False,
            "concluida": False,
            "vistos": [],
            "coletados": [],
            "seguindo": False,
            "encontrado": False,
            "chegou": False,
        }
        for missao in MISSOES
    }


class GerenciadorMissoes:
    """Controla objetivos, seguidores e recompensas durante a sessão."""

    def __init__(self, tamanho_tile):
        self.tamanho_tile = tamanho_tile
        self.estado = _novo_estado()
        self.missao_atual = None
        self.dialogo_extra = []
        self._textos_alvos = {}
        self._cache_hud = None
        self._superficie_hud = None
        self._conclusoes_pendentes = []
        self._descoberta_pendente = False
        self._npc_por_nome = {}
        self._ponto_lagoa = REGIOES["lagoa"].copy()
        self._retangulo_mata = REGIOES["mata"].copy()
        self.residuos = [
            {"x": x, "y": y, "tipo": tipo, "rect": pygame.Rect(x, y, 34, 34), "coletado": False}
            for x, y, tipo in (
                (1584, 1104, "garrafa"), (1824, 1900, "papel"),
                (2160, 1200, "lata"), (2484, 1840, "garrafa"),
                (1680, 1940, "lata"), (2352, 1450, "papel"),
            )
        ]
        self._posicoes_originais = {
            "Rocky (Capivara)": (720, 360),
            "Pombo Beiçudo": (2016, 1536),
            "Scorpion (Escorpião-Amarelo)": (900, 900),
            "Blue (Arara-Azul)": (3000, 2700),
        }

    @property
    def ativas(self):
        return [
            missao for missao in MISSOES
            if self.estado[missao["id"]]["iniciada"]
            and not self.estado[missao["id"]]["concluida"]
            and self.disponivel(missao)
        ]

    def chave_angelo(self):
        return sum(bool(self.estado[identificador]["concluida"]) for identificador in MISSOES_PRINCIPAIS)

    def disponivel(self, missao):
        indice = MISSOES_PRINCIPAIS.index(missao["id"])
        return all(self.estado[anterior]["concluida"] for anterior in MISSOES_PRINCIPAIS[:indice])

    def por_npc(self, nome):
        return next(
            (
                missao for missao in MISSOES
                if missao["npc"] == nome
                and not self.estado[missao["id"]]["concluida"]
                and self.disponivel(missao)
            ),
            None,
        )

    def definir_npcs(self, npcs):
        self._npc_por_nome = {npc.nome: npc for npc in npcs}
        # Coloca os animais nos ambientes previstos pela campanha.
        for nome, posicao in self._posicoes_originais.items():
            npc = self._npc_por_nome.get(nome)
            if npc:
                npc.x, npc.y = posicao
                npc.rect.topleft = posicao
        escorpiao = self._npc_por_nome.get("Scorpion (Escorpião-Amarelo)")
        if escorpiao:
            escorpiao.visivel = False
        self._sincronizar_seguidores()

    def dialogos_npc(self, nome):
        missao = self.por_npc(nome)
        if missao is None:
            return ["Ainda não é hora desta missão!"]

        self.missao_atual = missao["id"]
        estado = self.estado[missao["id"]]
        if not estado["iniciada"]:
            self.dialogo_extra = []
            return missao["inicio"]

        if missao.get("seguir") and estado["seguindo"]:
            nome_destino = "lagoa" if missao["id"] == "aguas" else "floresta"
            return [f"Estou seguindo você. Continue até o marcador da {nome_destino}."]
        if missao.get("seguir") and not estado.get("chegou", False):
            return missao["inicio"]

        if missao["id"] == "cidade":
            return [self._resumo_visitas()]
        if missao["id"] == "pombo":
            coletados = len(estado["coletados"])
            return [f"Você recolheu {coletados}/{QUANTIDADE_RESIDUOS} resíduos. Continue procurando pela praça."]
        if missao["id"] == "escondidos" and estado["encontrado"]:
            return ["Você me encontrou. Observe à distância; não toque nem tente capturar.", missao["dica"]]
        return [missao.get("dica", "Continue explorando para cumprir o objetivo da missão.")]

    def fim_dialogo(self, nome):
        missao = next((item for item in MISSOES if item["id"] == self.missao_atual), None)
        if missao is None or missao["npc"] != nome:
            return

        estado = self.estado[missao["id"]]
        if not estado["iniciada"]:
            estado["iniciada"] = True
            if missao["id"] == "escondidos":
                estado["encontrado"] = True
        if missao.get("seguir") and not estado.get("chegou", False):
            estado["seguindo"] = True
        self._sincronizar_seguidores()
        if self._objetivos_ok(missao):
            self._concluir(missao)

    def _resumo_visitas(self):
        vistos = set(self.estado["cidade"]["vistos"])
        nomes = [nome for indice, (_chave, nome) in enumerate(MISSOES[0]["objetivos"])
                 if indice in vistos]
        faltam = [nome for indice, (_chave, nome) in enumerate(MISSOES[0]["objetivos"])
                  if indice not in vistos]
        if faltam:
            return f"Locais visitados: {', '.join(nomes) or 'nenhum'}. Faltam: {', '.join(faltam)}."
        return "Você visitou os três locais! A missão foi concluída."

    def _objetivos_ok(self, missao):
        estado = self.estado[missao["id"]]
        if missao["id"] == "cidade":
            return len(estado["vistos"]) >= len(missao["objetivos"])
        if missao["id"] == "pombo":
            return len(estado["coletados"]) >= QUANTIDADE_RESIDUOS
        if missao["id"] == "escondidos":
            return estado["encontrado"]
        if missao.get("seguir"):
            return estado["iniciada"] and estado["seguindo"] is False and estado.get("chegou", False)
        return False

    def _concluir(self, missao):
        estado = self.estado[missao["id"]]
        if estado["concluida"] or not self._objetivos_ok(missao):
            return
        estado["concluida"] = True
        estado["seguindo"] = False
        self._conclusoes_pendentes.append(missao["titulo"])
        self._sincronizar_seguidores()

    def consumir_conclusoes(self):
        conclusoes = self._conclusoes_pendentes[:]
        self._conclusoes_pendentes.clear()
        return conclusoes

    def consumir_descoberta(self):
        descoberta = self._descoberta_pendente
        self._descoberta_pendente = False
        return descoberta

    def atualizar(self, player_rect):
        missao_atual = next(iter(self.ativas), None)
        if missao_atual is None:
            self._atualizar_visibilidade_escorpiao(player_rect)
            self._sincronizar_seguidores(player_rect)
            return
        identificador = missao_atual["id"]
        estado = self.estado[identificador]

        if identificador == "cidade":
            for indice, (chave, _nome) in enumerate(missao_atual["objetivos"]):
                if indice not in estado["vistos"] and player_rect.colliderect(REGIOES[chave]):
                    estado["vistos"].append(indice)
                    if len(estado["vistos"]) == len(missao_atual["objetivos"]):
                        self._concluir(missao_atual)

        elif identificador == "pombo":
            for indice, residuo in enumerate(self.residuos):
                if indice not in estado["coletados"] and player_rect.colliderect(residuo["rect"].inflate(20, 20)):
                    estado["coletados"].append(indice)
                    residuo["coletado"] = True
            if self._objetivos_ok(missao_atual):
                self._concluir(missao_atual)

        elif identificador == "escondidos":
            self._atualizar_visibilidade_escorpiao(player_rect)

        elif identificador in ("aguas", "arara_retorno") and estado["seguindo"]:
            destino = self._ponto_lagoa if identificador == "aguas" else self._retangulo_mata
            if player_rect.colliderect(destino):
                estado["seguindo"] = False
                estado["chegou"] = True
                self._concluir(missao_atual)
            self._sincronizar_seguidores(player_rect)

    def _atualizar_visibilidade_escorpiao(self, player_rect):
        npc = self._npc_por_nome.get("Scorpion (Escorpião-Amarelo)")
        missao = next(item for item in MISSOES if item["id"] == "escondidos")
        estado = self.estado["escondidos"]
        if npc is None:
            return
        if not self.disponivel(missao) or estado["concluida"]:
            npc.visivel = estado["concluida"]
            return
        encontrado_agora = player_rect.colliderect(npc.rect.inflate(300, 300))
        if encontrado_agora and not estado["encontrado"]:
            estado["encontrado"] = True
            self._descoberta_pendente = True
        npc.visivel = encontrado_agora or estado["encontrado"]

    def interagir_alvo(self, player_rect):
        """Coleta resíduos por proximidade; pontos de visita são registrados ao andar."""
        estado = self.estado["pombo"]
        if not estado["iniciada"] or estado["concluida"]:
            return False
        for indice, residuo in enumerate(self.residuos):
            if indice in estado["coletados"]:
                continue
            if player_rect.colliderect(residuo["rect"].inflate(48, 48)):
                estado["coletados"].append(indice)
                residuo["coletado"] = True
                self.dialogo_extra = ["Resíduo recolhido! "
                                      f"{len(estado['coletados'])}/{QUANTIDADE_RESIDUOS}."]
                missao = next(item for item in MISSOES if item["id"] == "pombo")
                if self._objetivos_ok(missao):
                    self._concluir(missao)
                return True
        return False

    def _sincronizar_seguidores(self, player_rect=None):
        for identificador, nome in (
            ("aguas", "Rocky (Capivara)"),
            ("arara_retorno", "Blue (Arara-Azul)"),
        ):
            estado = self.estado[identificador]
            npc = self._npc_por_nome.get(nome)
            if npc is None:
                continue
            npc.visivel = True
            if estado["seguindo"] and player_rect is not None:
                posicao = (player_rect.x, player_rect.y - self.tamanho_tile)
                npc.x, npc.y = posicao
                npc.rect.topleft = posicao

    def desenhar(self, tela, camera_x, camera_y, fonte):
        # Lagoa provisória de água doce na área verde, desenhada sobre o mapa existente.
        centro = self._ponto_lagoa.centerx - camera_x, self._ponto_lagoa.centery - camera_y
        pygame.draw.ellipse(tela, (85, 139, 103), (centro[0] - 58, centro[1] - 36, 116, 72))
        pygame.draw.ellipse(tela, (53, 157, 202), (centro[0] - 50, centro[1] - 28, 100, 56))
        pygame.draw.ellipse(tela, (184, 220, 173), (centro[0] - 50, centro[1] - 28, 100, 56), 3)

        for missao in self.ativas:
            identificador = missao["id"]
            estado = self.estado[identificador]
            if identificador == "cidade":
                for indice, (chave, nome) in enumerate(missao["objetivos"]):
                    regiao = REGIOES[chave].move(-camera_x, -camera_y)
                    pygame.draw.rect(tela, (235, 210, 85), regiao, 3, border_radius=8)
                    self._desenhar_rotulo(tela, fonte, nome, regiao.x + 4, regiao.y + 4,
                                          (indice in estado["vistos"]))
            elif identificador == "aguas":
                alvo = self._ponto_lagoa.move(-camera_x, -camera_y)
                pygame.draw.rect(tela, (240, 230, 120), alvo.inflate(24, 24), 3, border_radius=10)
            elif identificador == "pombo":
                for indice, residuo in enumerate(self.residuos):
                    if indice not in estado["coletados"]:
                        self._desenhar_residuo(tela, residuo["x"] - camera_x,
                                               residuo["y"] - camera_y, residuo["tipo"])
            elif identificador == "escondidos":
                area = REGIOES["lixao"].move(-camera_x, -camera_y)
                pygame.draw.rect(tela, (218, 174, 90), area, 3, border_radius=8)
                self._desenhar_rotulo(tela, fonte, "Procure por aqui", area.x + 4, area.y + 4, False)
            elif identificador == "arara_retorno" and estado["seguindo"]:
                alvo = self._retangulo_mata.move(-camera_x, -camera_y)
                pygame.draw.rect(tela, (104, 201, 114), alvo, 3)
                self._desenhar_rotulo(tela, fonte, "Floresta", alvo.x + 8, alvo.y + 8, False)

    @staticmethod
    def _desenhar_residuo(tela, x, y, tipo):
        if tipo == "garrafa":
            pygame.draw.rect(tela, (60, 183, 145), (x + 10, y + 6, 14, 28), border_radius=4)
            pygame.draw.rect(tela, (220, 240, 220), (x + 14, y + 2, 6, 7))
        elif tipo == "lata":
            pygame.draw.rect(tela, (173, 177, 180), (x + 5, y + 8, 26, 24), border_radius=4)
            pygame.draw.line(tela, (235, 235, 235), (x + 8, y + 12), (x + 28, y + 12), 2)
        else:
            pygame.draw.polygon(tela, (245, 238, 209),
                                ((x + 5, y + 8), (x + 25, y + 4), (x + 31, y + 27), (x + 10, y + 31)))
            pygame.draw.line(tela, (147, 128, 91), (x + 10, y + 15), (x + 25, y + 12), 2)

    @staticmethod
    def _desenhar_rotulo(tela, fonte, texto, x, y, concluido):
        prefixo = "✓ " if concluido else "○ "
        superficie = fonte.render(prefixo + texto, True, (240, 255, 225))
        fundo = pygame.Surface((superficie.get_width() + 12, superficie.get_height() + 6), pygame.SRCALPHA)
        fundo.fill((16, 28, 20, 190))
        tela.blit(fundo, (x, y))
        tela.blit(superficie, (x + 6, y + 3))

    def desenhar_hud(self, tela, fonte):
        missao = next(iter(self.ativas), None)
        if missao is None:
            if self.chave_angelo() == len(MISSOES_PRINCIPAIS):
                mensagem = "Todas as missões de Ângelo foram concluídas!"
                superficie = fonte.render(mensagem, True, (255, 255, 225))
                tela.blit(superficie, (20, 20))
            return

        identificador = missao["id"]
        estado = self.estado[identificador]
        linhas = [f"{missao['titulo']}  |  Peças da Chave: {self.chave_angelo()}/5"]
        if identificador == "cidade":
            for indice, (_chave, nome) in enumerate(missao["objetivos"]):
                linhas.append(("✓ " if indice in estado["vistos"] else "□ ") + nome)
        elif identificador == "pombo":
            linhas.append(f"Resíduos recolhidos: {len(estado['coletados'])}/{QUANTIDADE_RESIDUOS}")
        elif identificador == "aguas":
            linhas.append("Leve a capivara até a lagoa na mata. Use E para conversar.")
        elif identificador == "escondidos":
            linhas.append("Explore o lixão e aproxime-se com cuidado para encontrá-lo.")
        elif identificador == "arara_retorno":
            linhas.append("Acompanhe a arara até a área verde ao norte.")

        chave = tuple(linhas)
        if chave != self._cache_hud:
            largura_max = min(tela.get_width() - 80, 620)
            renderizados = []
            for linha in linhas:
                atual = ""
                for palavra in linha.split():
                    tentativa = f"{atual} {palavra}".strip()
                    if atual and fonte.size(tentativa)[0] > largura_max - 24:
                        renderizados.append(fonte.render(atual, True, (255, 255, 230)))
                        atual = palavra
                    else:
                        atual = tentativa
                if atual:
                    renderizados.append(fonte.render(atual, True, (255, 255, 230)))
            altura = len(renderizados) * fonte.get_linesize() + 18
            painel = pygame.Surface((largura_max, altura), pygame.SRCALPHA)
            pygame.draw.rect(painel, (14, 25, 22, 210), painel.get_rect(), border_radius=8)
            y = 9
            for superficie in renderizados:
                painel.blit(superficie, (12, y))
                y += fonte.get_linesize()
            self._superficie_hud = painel
            self._cache_hud = chave
        # Uma margem maior mantém o painel legível mesmo em janelas escaladas/capturadas.
        tela.blit(self._superficie_hud, (40, 40))


# Compatibilidade com imports de versões anteriores do jogo.
MissaoPombo = GerenciadorMissoes
