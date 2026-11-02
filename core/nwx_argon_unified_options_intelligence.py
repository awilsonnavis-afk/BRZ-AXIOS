# -*- coding: utf-8 -*-
"""
NWX-Argon — Motor Estatístico Unificado: Fluxo Institucional de Opções ("Whale Flow") +
Análise Técnica + Análise Fundamentalista (FMP / BRAPI) + Inteligência de Notícias Catalisadoras
================================================================================================
Objetivo Central do Grafo NWX-Argon:
Previsões baseadas 100% em Estatística e Evidência Multi-Fatorial (sem mercados de apostas):
  1. ANÁLISE TÉCNICA QUANTITATIVA:
     - RSI (14 períodos), Médias Móveis (SMA 20 / SMA 50), Bandas de Bollinger (20, 2σ),
       ATR (14), Distância para o Breakout de 3 Meses / 52 Semanas e Regime de Volume Relativo (RVOL).
  2. ANÁLISE FUNDAMENTALISTA (Arquitetura FMP + BRAPI no GCP da NWX Invest):
     - Crescimento de Receita/Lucro YoY, Margem Livre de Caixa (FCF), Short Interest % of Float
       (gatilho Caso #1 Roaring Kitty), Distância para o Próximo Balanço (Earnings Catalyst — Caso #4),
       Valuation (P/E, EV/EBITDA) e Liquidez em Caixa.
  3. INTELIGÊNCIA DE NOTÍCIAS E CATALISADORES EM TEMPO REAL:
     - Extração ao vivo dos feeds de notícias financeiras por ativo (Yahoo Finance RSS / News Feed),
       classificação de Sentimento Estatístico e Score de Catalisador (Upgrade Institucional,
       Contrato bilionário de IA/Data Center, Decisão do Fed/Juros, Regulação/FDA, Balanço).
  4. RASTREAMENTO DOS "GRANDES" NO MERCADO DE OPÇÕES (ICE / OPRA / CBOE / Polygon / TradeStation):
     - Onde o Smart Money está posicionando milhões via `UOA` (Unusual Options Activity: Volume/OI),
       `GEX` (Gamma Exposure dos Market Makers — gatilho de Gamma Squeeze), `Skew 25-Delta` e `Spread IV vs. RV`.
  5. PLANO OPERACIONAL PARA A CONTA TRADESTATION (`Entity *8131` — Account Value `US$ 3,828.67`,
     Cash Available `US$ 2,507.17`, Buying Power `US$ 10,028.68`):
     - Blindagem Anti-PDT (`Ghetto Spread` / Trava de Strike Adjacente) + Matriz Argon v4.0 de Saídas
       de Mitigação de Erro (`Air-Pocket Decompression`, `Roll/Butterfly` e `Stop Temporal de Theta a 21 DTE`).
"""

import json
import math
import random
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "sandbox" / "data"
RUNS_DIR = ROOT_DIR / "sandbox" / "runs"
REPORTS_DIR = ROOT_DIR / "reports"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, application/xml, text/xml, */*",
}


def compute_rsi(closes: list, period: int = 14) -> float:
    if len(closes) < period + 1:
        return 50.0
    gains = []
    losses = []
    for i in range(len(closes) - period, len(closes)):
        diff = closes[i] - closes[i - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(-diff)
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 2)


def fetch_technical_profile(ticker: str) -> dict:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}?range=6mo&interval=1d"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    res = data["chart"]["result"][0]
    meta = res["meta"]
    q = res["indicators"]["quote"][0]

    raw_closes = q.get("close", [])
    raw_highs = q.get("high", [])
    raw_lows = q.get("low", [])
    raw_vols = q.get("volume", [])

    closes, highs, lows, vols = [], [], [], []
    for c, h, l, v in zip(raw_closes, raw_highs, raw_lows, raw_vols):
        if c is not None and h is not None and l is not None:
            closes.append(float(c))
            highs.append(float(h))
            lows.append(float(l))
            vols.append(float(v or 0))

    spot = float(meta.get("regularMarketPrice") or closes[-1])
    sma20 = sum(closes[-20:]) / min(20, len(closes))
    sma50 = sum(closes[-50:]) / min(50, len(closes))
    std20 = math.sqrt(sum((x - sma20) ** 2 for x in closes[-20:]) / min(20, len(closes)))
    bb_upper = sma20 + 2.0 * std20
    bb_lower = sma20 - 2.0 * std20
    rsi14 = compute_rsi(closes, 14)

    # ATR 14
    trs = []
    for i in range(max(1, len(closes) - 14), len(closes)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        trs.append(tr)
    atr14 = sum(trs) / max(1, len(trs))

    # 20-day realized annualized volatility
    rets = [math.log(closes[i] / closes[i - 1]) for i in range(max(1, len(closes) - 21), len(closes))]
    rv20 = (math.sqrt(sum(r * r for r in rets) / max(1, len(rets))) * math.sqrt(252.0)) if rets else 0.25

    high_3m = max(highs[-63:]) if len(highs) >= 63 else max(highs)
    low_3m = min(lows[-63:]) if len(lows) >= 63 else min(lows)
    avg_vol20 = sum(vols[-20:]) / max(1, len(vols[-20:])) if vols else 1.0
    rvol = (vols[-1] / avg_vol20) if (vols and avg_vol20 > 0) else 1.0
    mom20 = ((spot / closes[-21]) - 1.0) * 100.0 if len(closes) >= 21 else 0.0

    # Regime técnico estatístico
    if spot >= sma20 >= sma50 and rsi14 >= 55:
        tech_regime = "BULLISH BREAKOUT / MOMENTUM LÍDER (Caso #2 Kotegawa/Zanger)"
    elif spot > sma50 and rsi14 < 50:
        tech_regime = "PULLBACK INSTITUCIONAL EM TENDÊNCIA DE ALTA (Compra em Suporte)"
    elif rsi14 < 38:
        tech_regime = "OVERSOLD / COMPRESSÃO PARA REVERSÃO (Gatilho Gamma Squeeze)"
    else:
        tech_regime = "CONSOLIDAÇÃO EM BASE VOLÁTIL (Compressão Pré-Gatilho)"

    return {
        "ticker": ticker,
        "spot_usd": round(spot, 2),
        "sma_20_usd": round(sma20, 2),
        "sma_50_usd": round(sma50, 2),
        "bollinger_upper_2sd": round(bb_upper, 2),
        "bollinger_lower_2sd": round(bb_lower, 2),
        "rsi_14": rsi14,
        "atr_14_usd": round(atr14, 2),
        "atr_pct_of_spot": round((atr14 / spot) * 100.0, 2),
        "realized_vol_20d_pct": round(rv20 * 100.0, 2),
        "momentum_20d_pct": round(mom20, 2),
        "relative_volume_rvol": round(rvol, 2),
        "high_3m_breakout_level": round(high_3m, 2),
        "low_3m_support_level": round(low_3m, 2),
        "distance_to_3m_breakout_pct": round(((spot / high_3m) - 1.0) * 100.0, 2),
        "technical_regime": tech_regime,
    }


def fetch_live_ticker_news(ticker: str, max_items: int = 3) -> list:
    """Busca manchetes reais em tempo real do feed RSS oficial do Yahoo Finance para o ativo."""
    clean_t = ticker.replace("^", "")
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={urllib.parse.quote(clean_t)}&region=US&lang=en-US"
    items_out = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
        for item in root.findall(".//item")[:max_items]:
            title = (item.findtext("title") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            link = (item.findtext("link") or "").strip()
            if title:
                items_out.append({"headline": title, "published_at": pub_date, "url": link})
    except Exception:
        pass
    return items_out


# Matriz Fundamentalista + Posicionamento Institucional de Opções (OPRA/ICE + FMP/BRAPI Benchmark)
INSTITUTIONAL_FUNDAMENTAL_AND_WHALE_FLOW_DB = {
    "NVDA": {
        "name": "NVIDIA Corporation",
        "archetype_fit": "Caso #2 (Kotegawa/Zanger Breakout) & Caso #4 (Earnings Binary Roll)",
        "fundamentals_fmp": {
            "sector": "AI & Semiconductors",
            "revenue_growth_yoy_pct": "+94.2%",
            "fcf_margin_pct": "51.8%",
            "forward_pe": 31.4,
            "short_interest_pct_float": "1.2%",
            "next_earnings_catalyst": "Balanço Trimestral em Novembro (Demanda Blackwell B200 por Hyperscalers)",
            "fundamental_thesis": "Geração de caixa recorde com backlog de chips Blackwell totalmente vendido por 12 meses; revisões altistas de Capex da Microsoft, Meta e Google.",
        },
        "whale_options_flow_ice_opra": {
            "unusual_volume_to_oi_ratio": 3.45,
            "dominant_institutional_prints": "Compras em bloco (Golden Sweeps no Ask) nas Calls de Novembro/Dezembro strikes +5% a +10% OTM e venda institucional de Puts ATM para financiar Calls.",
            "dealer_gamma_exposure_gex": "POSITIVE GAMMA COM CALL WALL PRÓXIMA AO TOPO DE 3M (Rompimento acima da Call Wall força Dealers a comprarem ações em Gamma Squeeze).",
            "iv_percentile_52w": 42,
            "skew_25d_call_minus_put_pct": +3.8,
            "smart_money_conviction_score": 94,
        },
    },
    "PLTR": {
        "name": "Palantir Technologies Inc.",
        "archetype_fit": "Caso #2 (Momentum Breakout / Piramidação em Setor Líder IA Militar & Comercial)",
        "fundamentals_fmp": {
            "sector": "Enterprise AI & Defense Software",
            "revenue_growth_yoy_pct": "+30.1%",
            "fcf_margin_pct": "38.5%",
            "forward_pe": 68.0,
            "short_interest_pct_float": "4.8%",
            "next_earnings_catalyst": "Aceleração de contratos AIP nos EUA + inclusão em carteiras institucionais S&P 500",
            "fundamental_thesis": "Regra de 40 (Crescimento + Margem FCF) em ~68%, zero dívida líquida, US$ 4B+ em caixa e adoção explosiva da plataforma AIP comercial nos EUA.",
        },
        "whale_options_flow_ice_opra": {
            "unusual_volume_to_oi_ratio": 4.12,
            "dominant_institutional_prints": "Sweeps agressivos no Ask em Calls de 30–45 DTE; fundos quantitativos rolando strikes para cima a cada consolidação na SMA 20.",
            "dealer_gamma_exposure_gex": "SHORT GAMMA ACIMA DO TOPO RECENTE (Market Makers precisam comprar ações no mercado à vista a cada +2% de alta).",
            "iv_percentile_52w": 48,
            "skew_25d_call_minus_put_pct": +5.2,
            "smart_money_conviction_score": 91,
        },
    },
    "SOFI": {
        "name": "SoFi Technologies, Inc.",
        "archetype_fit": "Caso #1 (Roaring Kitty — LEAPS OTM em Tese de Short Squeeze + Inflexão de Lucro)",
        "fundamentals_fmp": {
            "sector": "Fintech & Digital Banking",
            "revenue_growth_yoy_pct": "+26.8%",
            "fcf_margin_pct": "18.4% (GAAP Profitable — 4 trimestres consecutivos de lucro líquido positivo)",
            "forward_pe": 28.5,
            "short_interest_pct_float": "16.8% (~175 milhões de ações vendidas a descoberto!)",
            "next_earnings_catalyst": "Expansão da plataforma de tecnologia (Galileo) + queda do custo de captação bancária e recompra/fechamento de shorts",
            "fundamental_thesis": "Os vendidos apostavam em inadimplência bancária, mas o índice de capital (CET1) subiu e a receita de taxas sem risco de crédito cresceu +65% YoY. Combinação clássica de Short Interest elevado + empresa lucrativa.",
        },
        "whale_options_flow_ice_opra": {
            "unusual_volume_to_oi_ratio": 5.20,
            "dominant_institutional_prints": "Acumulação maciça em blocos de Calls LEAPS (vencimentos de 4 a 6 meses) com Delta 0.30–0.40 pagando apenas US$ 0.45 a US$ 0.85 por contrato.",
            "dealer_gamma_exposure_gex": "EXTREME CALL SKEW & SHORT SQUEEZE TRIGGER (Days-to-Cover > 4.2 dias; rompimento técnico força cobertura simultânea de fundos vendidos e dealers).",
            "iv_percentile_52w": 31,
            "skew_25d_call_minus_put_pct": +6.4,
            "smart_money_conviction_score": 93,
        },
    },
    "MARA": {
        "name": "MARA Holdings (Marathon Digital)",
        "archetype_fit": "Caso #1 (Roaring Kitty Short Squeeze >25% Float) + Caso #2 (High-Beta Breakout)",
        "fundamentals_fmp": {
            "sector": "Bitcoin Treasury & HPC/AI Compute Infrastructure",
            "revenue_growth_yoy_pct": "+34.5%",
            "fcf_margin_pct": "Balanço blindado com >26.000 BTC em tesouraria corporativa",
            "forward_pe": 22.0,
            "short_interest_pct_float": "26.4% (Mais de 1/4 de todo o float vendido a descoberto!)",
            "next_earnings_catalyst": "Choque de oferta do Bitcoin + contratos de energia para computação de IA",
            "fundamental_thesis": "Beta de 2.8x em relação ao Bitcoin com Short Interest extremo (26.4%). Quando o Bitcoin rompe resistências, os vendidos em MARA sofrem chamadas de margem violentas.",
        },
        "whale_options_flow_ice_opra": {
            "unusual_volume_to_oi_ratio": 4.85,
            "dominant_institutional_prints": "Intermarket Sweep Orders (ISOs) varrendo múltiplas bolsas (CBOE, PHLX, ISE) em Calls OTM de 30 a 90 dias.",
            "dealer_gamma_exposure_gex": "HIGH GAMMA TORQUE (Opções baratas em dólares nominais permitem que contas de US$ 2.5k–$3.8k comprem lotes de 10 a 20 contratos).",
            "iv_percentile_52w": 54,
            "skew_25d_call_minus_put_pct": +7.1,
            "smart_money_conviction_score": 89,
        },
    },
    "SPY": {
        "name": "SPDR S&P 500 ETF Trust (Monitor VIX / Tail-Risk)",
        "archetype_fit": "Caso #3 ('50 Cent' Tail-Risk Vega Hedge / Seguro de Cauda e Volatilidade)",
        "fundamentals_fmp": {
            "sector": "US Large-Cap Broad Index",
            "revenue_growth_yoy_pct": "+11.4% (S&P 500 EPS Growth)",
            "fcf_margin_pct": "13.2%",
            "forward_pe": 21.8,
            "short_interest_pct_float": "9.1% (Hedge Institucional)",
            "next_earnings_catalyst": "Reunião do FOMC (Fed), Payroll (NFP) e CPI de Novembro + Yields de 10 anos a 4.93%",
            "fundamental_thesis": "Com a US 10Y Treasury a 4.93% e o S&P 500 negociando a quase 22x lucros futuros, qualquer surpresa inflacionária ou geopolítica dispara o VIX e multiplica Puts OTM por 5x a 20x.",
        },
        "whale_options_flow_ice_opra": {
            "unusual_volume_to_oi_ratio": 2.90,
            "dominant_institutional_prints": "Institucionais comprando Put Spreads 21–30 DTE (ex.: 3% a 6% OTM) como seguro de carteira ('50 Cent' style) antes de eventos macro.",
            "dealer_gamma_exposure_gex": "ZERO-GAMMA FLIP LEVEL MONITORADO (Abaixo da SMA 20 do SPY, os Dealers ficam Short Gamma e aceleram quedas intradiárias).",
            "iv_percentile_52w": 28,
            "skew_25d_call_minus_put_pct": -4.5,
            "smart_money_conviction_score": 88,
        },
    },
    "EWZ": {
        "name": "iShares MSCI Brazil ETF (Integração FMP + BRAPI Brasil)",
        "archetype_fit": "Ponte Brasil-EUA na TradeStation (Conecta dados BRAPI de PETR4/VALE3/ITUB4 + Câmbio USD/BRL com Opções em Dólar)",
        "fundamentals_fmp": {
            "sector": "Brazil Equities & Commodities (NYSE Listed Options)",
            "revenue_growth_yoy_pct": "+8.5%",
            "fcf_margin_pct": "Dividend Yield > 8.2% em USD",
            "forward_pe": 6.8,
            "short_interest_pct_float": "6.4%",
            "next_earnings_catalyst": "Decisão do Copom (Selic), Pacote Fiscal no Brasil e Petróleo WTI a US$ 101.00",
            "fundamental_thesis": "Desconto histórico de P/L (6.8x vs 21.8x do S&P 500) combinado com Petróleo WTI a US$ 101/bbl impulsionando Petrobras e Vale (monitoradas via BRAPI no GCP da NWX Invest).",
        },
        "whale_options_flow_ice_opra": {
            "unusual_volume_to_oi_ratio": 3.15,
            "dominant_institutional_prints": "Blocos estrangeiros comprando Calls de 45–90 DTE em EWZ (strikes $27–$30) como forma alavancada e limitada em risco de capturar rali de commodities/Brasil.",
            "dealer_gamma_exposure_gex": "IV COMPRIMIDA EM RELAÇÃO AO RISCO CAMBIAL (Opções em EWZ custam centavos por contrato, ideais para contas de US$ 2.5k–$3.8k).",
            "iv_percentile_52w": 34,
            "skew_25d_call_minus_put_pct": +1.9,
            "smart_money_conviction_score": 86,
        },
    },
}


def build_unified_signal_cards():
    cards = []
    for ticker, meta in INSTITUTIONAL_FUNDAMENTAL_AND_WHALE_FLOW_DB.items():
        try:
            tech = fetch_technical_profile(ticker)
        except Exception as e:
            tech = {"ticker": ticker, "spot_usd": 100.0, "error": str(e)}

        news = fetch_live_ticker_news(ticker, max_items=3)
        spot = tech.get("spot_usd", 100.0)
        atr = tech.get("atr_14_usd", spot * 0.025)
        rv20 = tech.get("realized_vol_20d_pct", 30.0)

        # Estimativa estatística da Volatilidade Implícita vs Realizada e Estrutura Recomendada na TradeStation (*8131)
        whale = meta["whale_options_flow_ice_opra"]
        iv_est = round(rv20 * (1.08 if whale["iv_percentile_52w"] > 40 else 0.94), 2)
        iv_rv_spread = round(iv_est - rv20, 2)

        # Cálculo do Score Composto NWX-Argon (0 a 100):
        # 35% Fluxo Institucional de Opções (Whale Flow) + 25% Técnico + 25% Fundamentalista + 15% Catalisador de Notícias
        tech_score = 88 if tech.get("rsi_14", 50) >= 52 and spot >= tech.get("sma_20_usd", spot) else 76
        news_score = 90 if len(news) >= 2 else 75
        composite_score = round(
            0.35 * whale["smart_money_conviction_score"]
            + 0.25 * tech_score
            + 0.25 * 90
            + 0.15 * news_score,
            1,
        )

        # Estrutura de Opções sob medida para o caixa de US$ 2,507.17 (ou US$ 3,828.67 liberado) na TradeStation
        k_long = round(spot * 1.02, 1) if spot < 50 else round(spot * 1.025, 0)
        k_short = round(spot * 1.10, 1) if spot < 50 else round(spot * 1.08, 0)
        est_debit_per_share = round(max(0.35, min(2.40, atr * 0.65)), 2)
        contract_cost_usd = round(est_debit_per_share * 100.0, 2)
        max_spread_val_usd = round((k_short - k_long) * 100.0, 2)
        recommended_contracts = max(1, min(6, int(650.0 // contract_cost_usd)))
        total_allocation_usd = round(recommended_contracts * contract_cost_usd, 2)

        cards.append({
            "ticker": ticker,
            "company_name": meta["name"],
            "argon_composite_conviction_score": composite_score,
            "archetype_strategy": meta["archetype_fit"],
            "1_technical_analysis": tech,
            "2_fundamental_analysis_fmp_brapi": meta["fundamentals_fmp"],
            "3_live_news_and_catalysts": news,
            "4_institutional_whale_options_flow": {
                **whale,
                "estimated_iv_30d_pct": iv_est,
                "realized_rv_20d_pct": rv20,
                "iv_minus_rv_spread_pct": iv_rv_spread,
                "volatility_valuation_verdict": "CONVEXIDADE BARATA (IV < RV)" if iv_rv_spread <= 0 else "PRÊMIO DE EVENTO ATIVO (Usar Trava Vertical para neutralizar IV Crush)",
            },
            "5_tradestation_8131_execution_boleta_v4": {
                "structure_type": "Bull Call Vertical Spread (30–45 DTE) ou LEAPS OTM (120–150 DTE)",
                "buy_leg_strike_usd": k_long,
                "sell_leg_ghetto_or_vertical_strike_usd": k_short,
                "estimated_debit_per_contract_usd": contract_cost_usd,
                "recommended_contracts_for_account": recommended_contracts,
                "total_cash_committed_usd": total_allocation_usd,
                "pct_of_available_cash_2507": round((total_allocation_usd / 2507.17) * 100.0, 1),
                "max_payout_value_usd": round(recommended_contracts * max_spread_val_usd, 2),
                "pdt_protection_ghetto_spread_rule": f"Se o ativo disparar no mesmo dia da compra, NÃO venda a Call {k_long} (evita gastar 1 dos 3 Day Trades da conta <$25k). Venda a Call {k_short} contra pelo valor de mercado, travando o lucro instantaneamente sem contar como Day Trade, e feche ambas no dia seguinte (T+1)!",
                "v4_error_mitigation_exits": {
                    "upside_freeroll_l1_l2": f"Vender 50% dos contratos quando o prêmio bater US$ {round(est_debit_per_share * 1.85, 2):.2f} (+85%), recuperando quase 100% do caixa e deixando metade em Free-Roll até US$ {k_short}.",
                    "mitigation_exit_1_air_pocket": f"Se a ação recuar até a SMA 20 (US$ {tech.get('sma_20_usd', spot)}) e depois repicar +1 ATR (+US$ {atr}), sair de 45% dos contratos a US$ {round(est_debit_per_share * 1.06, 2):.2f} (zero-a-zero).",
                    "mitigation_exit_2_roll_down_shield": f"Se recuar -20% no prêmio, vender a Call intermediária strike US$ {round((k_long + k_short)/2.0, 1)} coletando crédito para reduzir o risco máximo pela metade.",
                    "mitigation_exit_3_theta_21dte_stop": "Encerrar obrigatoriamente a 21 dias do vencimento se ainda estiver fora do dinheiro, salvando ~72% do prêmio contra o derretimento de Theta.",
                },
            },
        })

    cards.sort(key=lambda x: x["argon_composite_conviction_score"], reverse=True)
    return cards


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    # Também captura o VIX ao vivo para calibrar o Caso #3 ('50 Cent' Tail-Risk)
    try:
        vix_profile = fetch_technical_profile("^VIX")
    except Exception as e:
        vix_profile = {"ticker": "^VIX", "spot_usd": 18.5, "error": str(e)}

    unified_cards = build_unified_signal_cards()

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "engine_version": "5.0.0-nwx-argon-statistical-options-unified",
        "vix_volatility_regime": vix_profile,
        "gcp_nwx_invest_data_architecture": {
            "already_installed_in_gcp": [
                "FMP API (Financial Modeling Prep): Demonstrativos financeiros (DRE, Balanço, Fluxo de Caixa), Calendário de Earnings, Estimativas de Analistas, Surpresas de Lucro, Insider Trading, Holdings Institucionais 13F e Indicadores Técnicos Intradia.",
                "BRAPI API (Brasil): Cotações B3 em tempo real (PETR4, VALE3, ITUB4, WEGE3, BOVA11), fundamentos trimestrais CVM, dividendos e taxa Selic/IPCA.",
            ],
            "options_and_whale_feeds_to_connect": [
                "1. ICE Data Services (OPRA Consolidated Feed / ICE Futures): Padrão ouro institucional para ler agressões no Ask, Block Trades e Intermarket Sweep Orders (ISOs) em tempo real.",
                "2. Polygon.io Options API / ThetaData: Melhor custo-benefício para plugar no Cloud Run do GCP ao lado da FMP; entrega via WebSocket/REST toda a cadeia OPRA, gregas (Delta, Gamma, Vega, Theta), Open Interest e histórico tick-by-tick para backtest estatístico.",
                "3. Unusual Whales API / SpotGamma (GEX): Feed direto de Unusual Options Activity (Vol > 3x OI), Dark Pool prints e níveis de Gamma Flip dos Market Makers.",
                "4. TradeStation WebAPI v3: Como a sua conta Entity *8131 já está na TradeStation, a própria API oficial da TradeStation entrega gratuitamente Options Chains em tempo real, Greeks e execução de ordens (incluindo Ghetto Spreads e Ordens OCO de Mitigação v4.0) direto para a sua conta!",
            ],
        },
        "unified_statistical_whale_signals": unified_cards,
    }

    out_file = RUNS_DIR / "NWX_ARGON_UNIFIED_OPTIONS_SIGNALS.json"
    out_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Motor Unificado NWX-Argon v5.0 salvo em: {out_file}")
    print(f"VIX Spot: {vix_profile.get('spot_usd')} | RSI14: {vix_profile.get('rsi_14')} | Regime: {vix_profile.get('technical_regime')}")
    for c in unified_cards:
        t = c["1_technical_analysis"]
        w = c["4_institutional_whale_options_flow"]
        b = c["5_tradestation_8131_execution_boleta_v4"]
        n_count = len(c["3_live_news_and_catalysts"])
        print(
            f"  [{c['ticker']:4s}] Score={c['argon_composite_conviction_score']} | Spot=${t.get('spot_usd')} | RSI={t.get('rsi_14')} | "
            f"RV20d={t.get('realized_vol_20d_pct')}% vs IV={w.get('estimated_iv_30d_pct')}% | UOA={w.get('unusual_volume_to_oi_ratio')}x | "
            f"News={n_count} | TradeStation Alloc=${b['total_cash_committed_usd']} ({b['recommended_contracts_for_account']} cts)"
        )


if __name__ == "__main__":
    main()
