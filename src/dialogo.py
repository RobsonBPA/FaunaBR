import pygame


class GerenciadorDialogo:
    def __init__(self):
        self.ativo = False
        self.npc_atual = None
        self.fala_atual = 0
        self._textos_renderizados = {}

    def iniciar(self, npcs, player_rect, dialogo_por_npc):
        for npc in npcs:
            if npc.visivel and player_rect.colliderect(npc.get_rect().inflate(80, 80)):
                self.ativo = True
                self.npc_atual = npc
                self.fala_atual = 0

                npc.dialogos = dialogo_por_npc(npc.nome)

                return True
        return False

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
        tela.blit(nome, (caixa.x + 25, caixa.y + 20))
        texto = self.npc_atual.dialogos[self.fala_atual]
        linhas = []
        atual = ""
        for palavra in texto.split():
            tentativa = f"{atual} {palavra}".strip()
            if fonte.size(tentativa)[0] > caixa.width - 50 and atual:
                linhas.append(atual)
                atual = palavra
            else:
                atual = tentativa
        if atual:
            linhas.append(atual)
        for indice, linha in enumerate(linhas[:2]):
            fala = self._obter_texto(fonte, linha, (255, 255, 255))
            tela.blit(fala, (caixa.x + 25, caixa.y + 62 + indice * 30))

    def _obter_texto(self, fonte, texto, cor):
        chave = (texto, cor)
        if chave not in self._textos_renderizados:
            self._textos_renderizados[chave] = fonte.render(texto, True, cor)
        return self._textos_renderizados[chave]
