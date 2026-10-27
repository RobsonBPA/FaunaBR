import pygame


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


def atualizar_dialogo_pombo(missao_ativa, missao_concluida, lixo_coletado, total_lixos):
    if missao_concluida:
        return DIALOGO_POMBO_FINAL

    if missao_ativa and lixo_coletado >= total_lixos:
        return DIALOGO_POMBO_CONCLUSAO

    if missao_ativa:
        return [
            texto.format(coletado=lixo_coletado, total=total_lixos)
            for texto in DIALOGO_POMBO_ANDAMENTO
        ]

    return DIALOGO_POMBO_INICIAL


class GerenciadorDialogo:
    def __init__(self):
        self.ativo = False
        self.npc_atual = None
        self.fala_atual = 0
        self._textos_renderizados = {}

    def iniciar(self, npcs, player_rect, dialogo_pombo):
        for npc in npcs:
            if player_rect.colliderect(npc.get_rect().inflate(80, 80)):
                self.ativo = True
                self.npc_atual = npc
                self.fala_atual = 0

                if npc.nome == "Pombo Beiçudo":
                    npc.dialogos = dialogo_pombo

                break

    def avancar(self):
        self.fala_atual += 1

        if self.fala_atual < len(self.npc_atual.dialogos):
            return None

        nome_npc = self.npc_atual.nome
        self.ativo = False
        self.npc_atual = None
        self.fala_atual = 0
        return nome_npc

    def desenhar(self, tela, fonte, largura_tela, altura_tela):
        if not self.ativo or self.npc_atual is None:
            return

        caixa = pygame.Rect(80, altura_tela - 180, largura_tela - 160, 130)
        pygame.draw.rect(tela, (20, 20, 20), caixa)
        pygame.draw.rect(tela, (255, 255, 255), caixa, 4)

        nome = self._obter_texto(
            fonte, self.npc_atual.nome, (255, 255, 0)
        )
        fala = self._obter_texto(
            fonte,
            self.npc_atual.dialogos[self.fala_atual],
            (255, 255, 255)
        )
        tela.blit(nome, (caixa.x + 25, caixa.y + 20))
        tela.blit(fala, (caixa.x + 25, caixa.y + 65))

    def _obter_texto(self, fonte, texto, cor):
        chave = (texto, cor)
        if chave not in self._textos_renderizados:
            self._textos_renderizados[chave] = fonte.render(texto, True, cor)
        return self._textos_renderizados[chave]