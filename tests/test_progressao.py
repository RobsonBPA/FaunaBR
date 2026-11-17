import unittest
from types import SimpleNamespace

import pygame

from src.missao import (
    MISSOES,
    MISSOES_PRINCIPAIS,
    QUANTIDADE_RESIDUOS,
    REGIOES,
    GerenciadorMissoes,
)
from src.personagens import criar_npcs


class TestProgressaoMissoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.missoes = GerenciadorMissoes(96)
        self.missoes.estado = {
            missao["id"]: {
                "iniciada": False, "concluida": False, "vistos": [],
                "coletados": [], "seguindo": False, "encontrado": False,
            }
            for missao in MISSOES
        }

    @staticmethod
    def _npc(nome, x=0, y=0):
        return SimpleNamespace(
            nome=nome, x=x, y=y, rect=pygame.Rect(x, y, 96, 96), visivel=True,
        )

    def _aceitar(self, identificador):
        missao = next(item for item in MISSOES if item["id"] == identificador)
        self.assertTrue(self.missoes.disponivel(missao))
        self.missoes.missao_atual = identificador
        self.missoes.fim_dialogo(missao["npc"])

    def _concluir_cachorro(self):
        self._aceitar("cidade")
        for chave, _nome in MISSOES[0]["objetivos"]:
            centro_x, centro_y = REGIOES[chave].center
            self.missoes.atualizar(pygame.Rect(centro_x, centro_y, 1, 1))
        self.assertTrue(self.missoes.estado["cidade"]["concluida"])

    def _concluir_capivara(self):
        self._aceitar("aguas")
        destino = self.missoes._ponto_lagoa
        self.missoes.atualizar(pygame.Rect(destino.centerx, destino.centery, 1, 1))
        self.assertTrue(self.missoes.estado["aguas"]["concluida"])

    def _concluir_pombo(self):
        self._aceitar("pombo")
        for residuo in self.missoes.residuos:
            self.missoes.atualizar(pygame.Rect(residuo["x"], residuo["y"], 1, 1))
        self.assertEqual(len(self.missoes.estado["pombo"]["coletados"]), QUANTIDADE_RESIDUOS)
        self.assertTrue(self.missoes.estado["pombo"]["concluida"])

    def test_elenco_e_missoes_nao_contem_a_prova_antiga(self):
        nomes = [npc.nome for npc in criar_npcs()]
        self.assertEqual(nomes, [
            "Iggy (Cachorro)", "Rocky (Capivara)", "Pombo Beiçudo",
            "Scorpion (Escorpião-Amarelo)", "Blue (Arara-Azul)",
        ])
        ids = {missao["id"] for missao in MISSOES}
        self.assertNotIn("prova_angelo", ids)
        self.assertNotIn("arara_biomas", ids)
        self.assertEqual(len(MISSOES_PRINCIPAIS), 5)

    def test_praca_central_lixao_superior_esquerdo_e_escorpiao_no_lixao(self):
        self.assertTrue(REGIOES["praca"].collidepoint(2496, 1344))
        self.assertLessEqual(REGIOES["praca"].right, REGIOES["campo"].left)
        self.assertLess(REGIOES["lixao"].y, REGIOES["praca"].y)
        scorpiao = self._npc("Scorpion (Escorpião-Amarelo)")
        self.missoes.definir_npcs([scorpiao])
        self.assertTrue(REGIOES["lixao"].contains(scorpiao.rect))

    def test_cachorro_requer_visitar_os_tres_locais_e_recompensa_uma_vez(self):
        self._aceitar("cidade")
        lixao, praca, campo = (chave for chave, _nome in MISSOES[0]["objetivos"])
        for chave in (lixao, praca):
            regiao = REGIOES[chave]
            self.missoes.atualizar(pygame.Rect(regiao.centerx, regiao.centery, 1, 1))
        self.assertFalse(self.missoes.estado["cidade"]["concluida"])
        self.assertEqual(len(self.missoes.estado["cidade"]["vistos"]), 2)
        regiao = REGIOES[campo]
        self.missoes.atualizar(pygame.Rect(regiao.centerx, regiao.centery, 1, 1))
        self.assertTrue(self.missoes.estado["cidade"]["concluida"])
        self.assertEqual(self.missoes.chave_angelo(), 1)
        self.missoes.fim_dialogo("Iggy (Cachorro)")
        self.assertEqual(self.missoes.chave_angelo(), 1)

    def test_capivara_so_conclui_quando_chega_a_lagoa_de_agua_doce(self):
        npcs = [self._npc("Rocky (Capivara)", 720, 360)]
        self.missoes.definir_npcs(npcs)
        self._concluir_cachorro()
        self._aceitar("aguas")
        estado = self.missoes.estado["aguas"]
        self.assertTrue(estado["seguindo"])
        self.missoes.atualizar(pygame.Rect(2200, 3300, 96, 96))  # faixa de praia, fora da lagoa
        self.assertFalse(estado["concluida"])
        alvo = self.missoes._ponto_lagoa
        self.missoes.atualizar(pygame.Rect(alvo.centerx, alvo.centery, 1, 1))
        self.assertTrue(estado["concluida"])

    def test_pombo_recolhe_seis_residuos_e_nao_duplica_coletas(self):
        self._concluir_cachorro()
        self._concluir_capivara()
        self._aceitar("pombo")
        primeiro = self.missoes.residuos[0]
        posicao = pygame.Rect(primeiro["x"], primeiro["y"], 1, 1)
        self.missoes.atualizar(posicao)
        self.missoes.atualizar(posicao)
        self.assertEqual(len(self.missoes.estado["pombo"]["coletados"]), 1)
        for residuo in self.missoes.residuos[1:]:
            self.missoes.atualizar(pygame.Rect(residuo["x"], residuo["y"], 1, 1))
        self.assertTrue(self.missoes.estado["pombo"]["concluida"])
        self.assertEqual(self.missoes.chave_angelo(), 3)

    def test_escorpiao_fica_oculto_ate_jogador_se_aproximar_e_interagir(self):
        self._concluir_cachorro()
        self._concluir_capivara()
        self._concluir_pombo()
        scorpiao = self._npc("Scorpion (Escorpião-Amarelo)", 900, 900)
        self.missoes.definir_npcs([scorpiao])
        self.assertFalse(scorpiao.visivel)
        self.missoes.atualizar(scorpiao.rect.copy())
        self.assertTrue(scorpiao.visivel)
        self.assertTrue(self.missoes.consumir_descoberta())
        self.missoes.dialogos_npc("Scorpion (Escorpião-Amarelo)")
        self.missoes.fim_dialogo("Scorpion (Escorpião-Amarelo)")
        self.assertTrue(self.missoes.estado["escondidos"]["concluida"])
        self.assertIn("atendimento médico", " ".join(MISSOES[3]["inicio"]))

    def test_arara_e_conduzida_da_cidade_ate_a_mata(self):
        arara = self._npc("Blue (Arara-Azul)", 3000, 2700)
        self.missoes.definir_npcs([arara])
        self._concluir_cachorro()
        self._concluir_capivara()
        self._concluir_pombo()
        scorpiao = self._npc("Scorpion (Escorpião-Amarelo)", 900, 900)
        self.missoes.definir_npcs([arara, scorpiao])
        self.missoes.atualizar(scorpiao.rect.copy())
        self.missoes.dialogos_npc("Scorpion (Escorpião-Amarelo)")
        self.missoes.fim_dialogo("Scorpion (Escorpião-Amarelo)")
        self.missoes.dialogos_npc("Blue (Arara-Azul)")
        self.missoes.fim_dialogo("Blue (Arara-Azul)")
        self.assertTrue(self.missoes.estado["arara_retorno"]["seguindo"])
        self.missoes.atualizar(pygame.Rect(2000, 2000, 96, 96))
        self.assertFalse(self.missoes.estado["arara_retorno"]["concluida"])
        floresta = REGIOES["mata"]
        self.missoes.atualizar(pygame.Rect(floresta.centerx, floresta.centery, 1, 1))
        self.assertTrue(self.missoes.estado["arara_retorno"]["concluida"])
        self.assertEqual(self.missoes.chave_angelo(), 5)

    def test_missao_futura_nao_avanca_antes_de_desbloquear(self):
        self.missoes.estado["pombo"]["iniciada"] = True
        for residuo in self.missoes.residuos:
            self.missoes.atualizar(pygame.Rect(residuo["x"], residuo["y"], 96, 96))
        self.assertFalse(self.missoes.estado["pombo"]["concluida"])
        self.assertEqual(self.missoes.estado["pombo"]["coletados"], [])

    def test_progresso_nao_e_persistido_entre_instancias(self):
        self._aceitar("cidade")
        self.assertTrue(self.missoes.estado["cidade"]["iniciada"])
        outra_sessao = GerenciadorMissoes(96)
        self.assertFalse(outra_sessao.estado["cidade"]["iniciada"])
        self.assertFalse(outra_sessao.estado["cidade"]["concluida"])


if __name__ == "__main__":
    unittest.main()
