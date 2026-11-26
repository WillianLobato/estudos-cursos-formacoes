"""
calculos.py - Funções financeiras do "Painel & Calculadoras Financeiras".

Somente biblioteca padrão. Todas as taxas de entrada são em PERCENTUAL
(ex.: 1.0 significa 1%) e todas as funções retornam dicionários simples,
prontos para serem convertidos em JSON.
"""

import math


# ---------------------------------------------------------------------------
# Utilitários de taxa
# ---------------------------------------------------------------------------
def anual_para_mensal(taxa_anual_pct: float) -> float:
    """Converte taxa anual (%) em taxa mensal equivalente (%).

    Usa juros compostos: (1 + ia)^(1/12) - 1.
    """
    return ((1 + taxa_anual_pct / 100) ** (1 / 12) - 1) * 100


def mensal_para_anual(taxa_mensal_pct: float) -> float:
    """Converte taxa mensal (%) em taxa anual equivalente (%)."""
    return ((1 + taxa_mensal_pct / 100) ** 12 - 1) * 100


def _validar(**campos):
    """Valida entradas numéricas finitas e não negativas."""
    for nome, valor in campos.items():
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"'{nome}' deve ser um número não negativo.")
        if not math.isfinite(valor) or valor < 0:
            raise ValueError(f"'{nome}' deve ser um número não negativo.")


def _validar_meses(valor) -> int:
    """Converte um prazo inteiro positivo sem truncar meses fracionários."""
    if isinstance(valor, bool):
        raise ValueError("'meses' deve ser um número inteiro maior que zero.")
    try:
        prazo = float(valor)
    except (TypeError, ValueError):
        raise ValueError("'meses' deve ser um número inteiro maior que zero.")
    if not math.isfinite(prazo) or prazo <= 0 or not prazo.is_integer():
        raise ValueError("'meses' deve ser um número inteiro maior que zero.")
    return int(prazo)


def _arred(x: float) -> float:
    return round(x, 2)


# ---------------------------------------------------------------------------
# 1) Juros compostos
# ---------------------------------------------------------------------------
def juros_compostos(valor_inicial, aporte_mensal, taxa, meses, tipo_taxa="mensal"):
    """Simula o acúmulo de capital com aportes mensais.

    Parâmetros:
        valor_inicial : capital inicial (R$)
        aporte_mensal : valor depositado ao FINAL de cada mês (R$)
        taxa          : taxa em %, mensal ou anual conforme `tipo_taxa`
        meses         : número de meses (inteiro > 0)
        tipo_taxa     : "mensal" ou "anual"

    Em cada mês: saldo = saldo * (1 + i) + aporte.

    Retorna: montante final, total investido, total de juros e a evolução
    mês a mês (útil para gráficos/tabelas).
    """
    _validar(valor_inicial=valor_inicial, aporte_mensal=aporte_mensal, taxa=taxa)
    meses = _validar_meses(meses)
    if tipo_taxa not in ("mensal", "anual"):
        raise ValueError("'tipo_taxa' deve ser 'mensal' ou 'anual'.")

    i_mensal = anual_para_mensal(taxa) if tipo_taxa == "anual" else taxa
    i = i_mensal / 100

    saldo = valor_inicial
    evolucao = []
    for mes in range(1, meses + 1):
        saldo = saldo * (1 + i) + aporte_mensal
        investido = valor_inicial + aporte_mensal * mes
        evolucao.append({"mes": mes, "investido": _arred(investido), "saldo": _arred(saldo)})

    total_investido = valor_inicial + aporte_mensal * meses
    return {
        "montante_final": _arred(saldo),
        "total_investido": _arred(total_investido),
        "total_juros": _arred(saldo - total_investido),
        "taxa_mensal_usada": round(i_mensal, 4),
        "taxa_anual_equivalente": round(mensal_para_anual(i_mensal), 4),
        "evolucao": evolucao,
    }


# ---------------------------------------------------------------------------
# 2) Comparador de investimentos
# ---------------------------------------------------------------------------
def aliquota_ir_renda_fixa(meses: int) -> float:
    """Alíquota regressiva de IR da renda fixa (CDB, prefixados etc.).

    Até 180 dias: 22,5% | 181-360: 20% | 361-720: 17,5% | acima: 15%.
    """
    dias = meses * 30
    if dias <= 180:
        return 22.5
    if dias <= 360:
        return 20.0
    if dias <= 720:
        return 17.5
    return 15.0


def taxa_poupanca_anual(selic_anual: float) -> float:
    """Rendimento anual aproximado da poupança (regra vigente).

    Selic > 8,5% a.a.  -> 0,5% a.m. + TR (TR considerada ~0 aqui).
    Selic <= 8,5% a.a. -> 70% da Selic + TR.
    """
    if selic_anual > 8.5:
        return mensal_para_anual(0.5)
    return selic_anual * 0.70


def comparador_investimentos(valor_inicial, aporte_mensal, meses, selic_anual,
                             pct_cdi=100.0, taxa_prefixada_anual=None):
    """Compara CDB/CDI, prefixado e poupança com os mesmos aportes.

    Premissas (simplificações didáticas):
      * CDI ≈ Selic - 0,10 ponto percentual.
      * O IR regressivo é aplicado sobre o lucro total pela idade média do
        prazo total (aproximação; na prática cada aporte tem sua própria idade).
      * Poupança é isenta de IR; CDB e prefixado sofrem IR.

    Retorna as opções ordenadas pelo valor LÍQUIDO (maior primeiro).
    """
    _validar(valor_inicial=valor_inicial, aporte_mensal=aporte_mensal,
             selic_anual=selic_anual, pct_cdi=pct_cdi)
    meses = _validar_meses(meses)

    cdi_anual = max(selic_anual - 0.10, 0)
    if taxa_prefixada_anual is None:
        taxa_prefixada_anual = cdi_anual  # referência neutra se não informado
    _validar(taxa_prefixada_anual=taxa_prefixada_anual)

    opcoes = [
        (f"{pct_cdi:g}% do CDI", cdi_anual * pct_cdi / 100, True),
        ("Prefixado", taxa_prefixada_anual, True),
        ("Poupança (referência)", taxa_poupanca_anual(selic_anual), False),
    ]

    resultado = []
    for nome, taxa_anual, paga_ir in opcoes:
        sim = juros_compostos(valor_inicial, aporte_mensal, taxa_anual, meses, "anual")
        lucro_bruto = sim["total_juros"]
        aliquota = aliquota_ir_renda_fixa(meses) if paga_ir else 0.0
        ir = lucro_bruto * aliquota / 100
        resultado.append({
            "nome": nome,
            "taxa_anual": round(taxa_anual, 2),
            "total_investido": sim["total_investido"],
            "montante_bruto": sim["montante_final"],
            "lucro_bruto": lucro_bruto,
            "aliquota_ir": aliquota,
            "ir": _arred(ir),
            "montante_liquido": _arred(sim["montante_final"] - ir),
            "lucro_liquido": _arred(lucro_bruto - ir),
        })

    resultado.sort(key=lambda o: o["montante_liquido"], reverse=True)
    melhor, pior = resultado[0], resultado[-1]
    return {
        "cdi_anual": round(cdi_anual, 2),
        "opcoes": resultado,
        "melhor": melhor["nome"],
        "vantagem_sobre_pior": _arred(melhor["montante_liquido"] - pior["montante_liquido"]),
    }


# ---------------------------------------------------------------------------
# 3) Financiamentos: SAC e Price
# ---------------------------------------------------------------------------
def financiamento_price(valor, taxa_mensal, prazo):
    """Tabela Price: parcelas FIXAS.

    PMT = PV * i / (1 - (1 + i)^-n)   (se i = 0, PMT = PV / n)
    """
    _validar(valor=valor, taxa_mensal=taxa_mensal)
    prazo = _validar_meses(prazo)
    if valor <= 0:
        raise ValueError("'valor' deve ser maior que zero.")

    i = taxa_mensal / 100
    pmt = valor / prazo if i == 0 else valor * i / (1 - (1 + i) ** -prazo)

    saldo, parcelas = valor, []
    for _ in range(prazo):
        juros = saldo * i
        amort = pmt - juros
        saldo -= amort
        parcelas.append(pmt)
    return _resumo(parcelas, valor)


def financiamento_sac(valor, taxa_mensal, prazo):
    """Tabela SAC: amortização CONSTANTE, parcelas decrescentes.

    amortização = PV / n ; parcela_k = amortização + saldo_devedor * i
    """
    _validar(valor=valor, taxa_mensal=taxa_mensal)
    prazo = _validar_meses(prazo)
    if valor <= 0:
        raise ValueError("'valor' deve ser maior que zero.")

    i = taxa_mensal / 100
    amort = valor / prazo

    saldo, parcelas = valor, []
    for _ in range(prazo):
        parcelas.append(amort + saldo * i)
        saldo -= amort
    return _resumo(parcelas, valor)


def _resumo(parcelas, valor):
    """Resume uma lista de parcelas em indicadores."""
    total = sum(parcelas)
    return {
        "parcela_inicial": _arred(parcelas[0]),
        "parcela_final": _arred(parcelas[-1]),
        "parcela_media": _arred(total / len(parcelas)),
        "total_pago": _arred(total),
        "total_juros": _arred(total - valor),
        "parcelas": [_arred(p) for p in parcelas],
    }


def comparar_financiamentos(valor, taxa_mensal, prazo):
    """Calcula SAC e Price lado a lado e indica qual custa menos."""
    _validar(valor=valor, taxa_mensal=taxa_mensal)
    prazo = _validar_meses(prazo)
    if valor <= 0:
        raise ValueError("Valor financiado deve ser maior que zero.")

    sac = financiamento_sac(valor, taxa_mensal, prazo)
    price = financiamento_price(valor, taxa_mensal, prazo)
    return {
        "sac": sac,
        "price": price,
        "menor_custo": "SAC" if sac["total_pago"] <= price["total_pago"] else "Price",
        "economia_total": _arred(abs(price["total_pago"] - sac["total_pago"])),
        "taxa_anual_equivalente": round(mensal_para_anual(taxa_mensal), 2),
    }


if __name__ == "__main__":  # teste rápido pelo terminal
    r = juros_compostos(1000, 200, 1, 12)
    print(r["montante_final"], r["total_investido"], r["total_juros"])
    f = comparar_financiamentos(200000, 0.9, 240)
    print(f["sac"]["parcela_inicial"], f["price"]["parcela_inicial"], f["menor_custo"])
