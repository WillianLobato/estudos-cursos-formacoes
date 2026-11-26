"""Testes das simulações financeiras usando somente a biblioteca padrão."""

import unittest

import calculos


class JurosCompostosTests(unittest.TestCase):
    def test_inclui_aportes_ao_final_de_cada_mes(self):
        resultado = calculos.juros_compostos(1000, 100, 1, 2)

        self.assertEqual(resultado["montante_final"], 1221.1)
        self.assertEqual(resultado["total_investido"], 1200)
        self.assertEqual(resultado["total_juros"], 21.1)

    def test_rejeita_prazo_fracionario_e_tipo_de_taxa_desconhecido(self):
        with self.assertRaises(ValueError):
            calculos.juros_compostos(1000, 0, 1, 2.5)
        with self.assertRaises(ValueError):
            calculos.juros_compostos(1000, 0, 1, 12, "diária")

    def test_converte_taxa_anual_em_equivalente_mensal(self):
        anual = calculos.juros_compostos(1000, 0, 12, 12, "anual")
        taxa_mensal = calculos.anual_para_mensal(12)
        mensal = calculos.juros_compostos(1000, 0, taxa_mensal, 12)

        self.assertAlmostEqual(anual["montante_final"], mensal["montante_final"], places=2)


class InvestimentosTests(unittest.TestCase):
    def test_ordena_opcoes_pelo_montante_liquido(self):
        resultado = calculos.comparador_investimentos(
            1000, 0, 24, selic_anual=10, taxa_prefixada_anual=20
        )

        self.assertEqual(resultado["melhor"], "Prefixado")
        valores = [opcao["montante_liquido"] for opcao in resultado["opcoes"]]
        self.assertEqual(valores, sorted(valores, reverse=True))


class FinanciamentosTests(unittest.TestCase):
    def test_sac_custa_menos_que_price_com_taxa_positiva(self):
        resultado = calculos.comparar_financiamentos(100000, 1, 12)

        self.assertLess(resultado["sac"]["total_pago"], resultado["price"]["total_pago"])
        self.assertGreater(resultado["sac"]["parcela_inicial"], resultado["sac"]["parcela_final"])
        self.assertEqual(resultado["price"]["parcela_inicial"], resultado["price"]["parcela_final"])

    def test_rejeita_prazo_invalido_tambem_nas_funcoes_individuais(self):
        for funcao in (calculos.financiamento_sac, calculos.financiamento_price):
            with self.subTest(funcao=funcao.__name__):
                with self.assertRaises(ValueError):
                    funcao(1000, 1, 0)
                with self.assertRaises(ValueError):
                    funcao(1000, 1, 1.5)

    def test_taxa_zero_tem_parcelas_iguais_nos_dois_sistemas(self):
        resultado = calculos.comparar_financiamentos(1200, 0, 12)

        self.assertEqual(resultado["sac"]["total_pago"], 1200)
        self.assertEqual(resultado["price"]["parcela_media"], 100)


if __name__ == "__main__":
    unittest.main()
