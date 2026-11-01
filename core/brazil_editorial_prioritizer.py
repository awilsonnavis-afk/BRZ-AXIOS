# -*- coding: utf-8 -*-
"""
Argon BRZ News — Algoritmo de Priorizacao Editorial por Volume & Gerador de Pautas
===================================================================================
Orquestrador: Axio Vance (agents/00_axio_orquestrador)
Investigador de Fontes: Gabriel Torres (agents/05_gabriel_torres_investigador_fontes)
Analista de Dados & Editorial: Clara Mendonca (agents/02_clara_mendonca_analista_dados)

Regra de Ouro Editorial (BRZ News):
- Priorizar estritamente o que tem MAIS VOLUME FINANCEIRO, LIQUIDEZ ATIVA e GIRO DE 24H.
- Filtrar mercados ja encerrados/decididos em campo (ex: preco >= 99.5c ou <= 0.5c em jogo unico)
  para que a redacao foque apenas em eventos VIVOS com dinheiro real em disputa.
"""

import json
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "sandbox" / "data"
RUNS_DIR = ROOT_DIR / "sandbox" / "runs"
REPORTS_DIR = ROOT_DIR / "reports"


def clean_text(s):
    if not s:
        return ""
    return str(s).replace("\u200b", "").strip()


def is_effectively_settled(markets):
    """Retorna True se todos os sub-mercados principais ja estao em 99.9% / 0.1% (liquidacao iminente)."""
    if not markets:
        return True
    for m in markets:
        p = m.get("yes_price_usd", 0.5)
        if 0.005 < p < 0.995:
            return False
    return True


def build_unified_volume_ranking():
    raw_path = DATA_DIR / "brazil_markets_high_volume_priority.json"
    data = json.loads(raw_path.read_text(encoding="utf-8"))

    poly_events = data["polymarket_high_volume"]["events"]
    kalshi_active = data["kalshi_high_volume"]["active_events"]
    kalshi_hist_mega = data["kalshi_high_volume"]["historical_mega_volume_events"]

    unified_live = []
    settled_today_reference = []

    # 1. Processar Polymarket
    for ev in poly_events:
        br_mkts = ev.get("brazil_markets") or ev.get("top_all_markets") or []
        settled_flag = is_effectively_settled(br_mkts)

        vol_br = float(ev.get("brazil_attributable_volume_usd", 0.0))
        vol_tot = float(ev.get("event_total_volume_usd", 0.0))
        vol_24h = float(ev.get("event_volume_24h_usd", 0.0))
        liq_br = float(ev.get("brazil_attributable_liquidity_usd", 0.0))

        # Score Editorial Priorizado por Volume:
        # Prioriza Volume Direto Brasil + 1.5x Liquidez + 3.0x Volume 24h + 0.15x Volume Global do Evento
        editorial_score = round(vol_br + 1.5 * liq_br + 3.0 * vol_24h + 0.15 * (vol_tot - vol_br), 2)

        item = {
            "exchange": "Polymarket",
            "id_or_ticker": ev.get("event_id"),
            "title": clean_text(ev.get("title")),
            "slug": ev.get("slug"),
            "url": ev.get("url"),
            "scope": ev.get("scope"),
            "brazil_volume_usd": round(vol_br, 2),
            "event_total_volume_usd": round(vol_tot, 2),
            "volume_24h_usd": round(vol_24h, 2),
            "liquidity_or_oi_usd": round(liq_br, 2),
            "editorial_priority_score": editorial_score,
            "is_settled_in_play": settled_flag,
            "top_brazil_contracts": br_mkts[:5],
        }

        if settled_flag:
            settled_today_reference.append(item)
        else:
            unified_live.append(item)

    # 2. Processar Kalshi (Contratos Ativos — 1 contrato = US$ 1.00 de valor nocional de liquidacao)
    for ev in kalshi_active:
        mkts = ev.get("markets") or []
        vol_contracts = float(ev.get("total_volume_contracts", 0.0))
        oi_contracts = float(ev.get("total_open_interest_contracts", 0.0))

        # Para eventos globais (ex: Copa 2030), usar volume do contrato do Brasil
        if ev.get("scope") != "100% Brasil":
            br_only = [m for m in mkts if ("brazil" in (m.get("title", "") + m.get("yes_sub_title", "")).lower())]
            if br_only:
                vol_br = sum(float(m.get("volume_contracts", 0.0)) for m in br_only)
                oi_br = sum(float(m.get("open_interest_contracts", 0.0)) for m in br_only)
            else:
                vol_br = vol_contracts
                oi_br = oi_contracts
        else:
            vol_br = vol_contracts
            oi_br = oi_contracts

        editorial_score = round(vol_br + 1.5 * oi_br + 0.10 * (vol_contracts - vol_br), 2)

        unified_live.append({
            "exchange": "Kalshi",
            "id_or_ticker": ev.get("event_ticker"),
            "title": f"{clean_text(ev.get('title'))} ({clean_text(ev.get('sub_title'))})",
            "slug": ev.get("series_ticker"),
            "url": f"https://kalshi.com/markets/{str(ev.get('series_ticker', '')).lower()}",
            "scope": ev.get("scope"),
            "brazil_volume_usd": round(vol_br, 2),
            "event_total_volume_usd": round(vol_contracts, 2),
            "volume_24h_usd": 0.0,
            "liquidity_or_oi_usd": round(oi_br, 2),
            "editorial_priority_score": editorial_score,
            "is_settled_in_play": False,
            "top_brazil_contracts": mkts[:5],
        })

    # Ordenar estritamente pelo Volume Direto no Brasil e Score Editorial
    unified_live.sort(key=lambda x: x["editorial_priority_score"], reverse=True)

    # Classificar em Tiers de Volume
    tier1 = [x for x in unified_live if (x["brazil_volume_usd"] >= 90000 or x["event_total_volume_usd"] >= 200000)]
    tier2 = [x for x in unified_live if x not in tier1 and (x["brazil_volume_usd"] >= 15000 or x["liquidity_or_oi_usd"] >= 15000)]
    tier3 = [x for x in unified_live if x not in tier1 and x not in tier2]

    return {
        "generated_at": datetime.now().isoformat(),
        "total_live_brazil_operations": len(unified_live),
        "tier_1_headline_high_volume_count": len(tier1),
        "tier_2_sectoral_medium_volume_count": len(tier2),
        "tier_3_low_volume_radar_count": len(tier3),
        "tier_1_headline_markets": tier1,
        "tier_2_sectoral_markets": tier2,
        "tier_3_radar_markets": tier3[:15],
        "settled_today_high_volume": settled_today_reference,
        "kalshi_historical_mega_benchmarks": kalshi_hist_mega,
    }


def main():
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    ranking = build_unified_volume_ranking()
    out_path = RUNS_DIR / "BRAZIL_EDITORIAL_VOLUME_RANKING.json"
    out_path.write_text(json.dumps(ranking, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== TOP 15 OPERACOES VIVAS DO BRASIL POR VOLUME & PRIORIDADE EDITORIAL ===")
    for i, m in enumerate((ranking["tier_1_headline_markets"] + ranking["tier_2_sectoral_markets"])[:15], 1):
        print(
            f"{i:02d}. [{m['exchange']}] {m['title']} | "
            f"Vol_BR=${m['brazil_volume_usd']:,.0f} | Vol_Global=${m['event_total_volume_usd']:,.0f} | "
            f"Liq/OI=${m['liquidity_or_oi_usd']:,.0f} | Score={m['editorial_priority_score']:,.0f}"
        )

    print("\n=== BENCHMARKS HISTORICOS DE MEGA-VOLUME BRASIL NA KALSHI (>50k contratos) ===")
    for i, h in enumerate(ranking["kalshi_historical_mega_benchmarks"][:10], 1):
        print(f"{i:02d}. [{h['event_ticker']}] {h['title']} ({h['sub_title']}) | Vol={h['total_volume_contracts']:,.0f} contratos")


if __name__ == "__main__":
    main()
