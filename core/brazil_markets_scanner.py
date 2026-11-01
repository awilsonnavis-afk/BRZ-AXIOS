# -*- coding: utf-8 -*-
"""
Argon Brazil Prediction Markets High-Volume Scanner & Editorial Prioritizer (Polymarket + Kalshi)
=================================================================================================
Agente Responsavel: Gabriel Torres (05_gabriel_torres_investigador_fontes)
Analista de Dados & Editorial: Clara Mendonca (02_clara_mendonca_analista_dados)
Orquestrador: Axio Vance (00_axio_orquestrador) — Projeto GCP `brz-news-prod` (BRZ News)

Objetivo:
1. Buscar de forma exaustiva todas as operacoes que envolvem o BRASIL na Polymarket e na Kalshi,
   expandindo `limit_per_type=50` na Gamma API e varrendo todas as 97 series da Kalshi.
2. Priorizar estritamente por VOLUME FINANCEIRO (US$), LIQUIDEZ DE LIVRO (US$) e OPEN INTEREST,
   separando:
   - Tier 1 (Mega-Volume / Pauta Principal BRZ News): Acima de US$ 100.000 de volume/liquidez.
   - Tier 2 (Médio Volume / Pauta Setorial): Entre US$ 10.000 e US$ 100.000.
   - Tier 3 (Baixo Volume / Monitoramento Secundário): Abaixo de US$ 10.000 (descartado da capa editorial).
"""

import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "sandbox" / "data"

# Regex rigorosa para mercados DIRETAMENTE ligados ao Brasil
CORE_BRAZIL_KEYWORDS = [
    r"\bbrazil\b",
    r"\bbrasil\b",
    r"\bbrazilian\b",
    r"\blula\b",
    r"\bbolsonaro\b",
    r"\btarcisio\b",
    r"\btarcísio\b",
    r"\bhaddad\b",
    r"\bmoraes\b",
    r"\bmarcal\b",
    r"\bmarçal\b",
    r"\bcaiado\b",
    r"\bzema\b",
    r"\bratinho\b",
    r"\bselic\b",
    r"\bcopom\b",
    r"\bibovespa\b",
    r"\bbovespa\b",
    r"\busd/brl\b",
    r"\busdbrl\b",
    r"\bpetrobras\b",
    r"\bsao paulo\b",
    r"\bsão paulo\b",
    r"\brio de janeiro\b",
    r"\bcopa do brasil\b",
    r"\bbrasileirao\b",
    r"\bbrasileirão\b",
    r"\blibertadores\b",
    r"\bflamengo\b",
    r"\bpalmeiras\b",
    r"\bcorinthians\b",
    r"\bbotafogo\b",
    r"\bgremio\b",
    r"\bgrêmio\b",
    r"\batletico mineiro\b",
    r"\batlético mineiro\b",
    r"\bvasco da gama\b",
    r"\bfluminense\b",
    r"\bcruzeiro\b",
    r"\bbahia\b",
    r"\bfortaleza\b",
    r"\bneymar\b",
    r"\bvinicius jr\b",
    r"\bvini jr\b",
    r"\balex pereira\b",
    r"\bcharles oliveira\b",
]

BRAZIL_REGEX = re.compile("|".join(CORE_BRAZIL_KEYWORDS), re.IGNORECASE)


def fetch_json(url: str, timeout: int = 20):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ArgonBRZNewsScanner/3.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def safe_float(val, default=0.0):
    try:
        if val is None or val == "":
            return default
        return float(val)
    except Exception:
        return default


def matches_brazil(text: str) -> bool:
    if not text:
        return False
    return bool(BRAZIL_REGEX.search(text))


def scan_polymarket_high_volume():
    """
    Busca todos os eventos na Polymarket usando `limit_per_type=50` em `/public-search`
    para 18 termos-chave do Brasil + varredura dos maiores eventos por volume.
    Calcula o Volume Relevante Brasil (para eventos globais, soma apenas o volume do sub-contrato do Brasil;
    para eventos 100% Brasil, usa o volume total do evento).
    """
    events_by_id = {}
    diagnostics = {"queries_tested": [], "total_unique_events_inspected": 0}

    queries = [
        "Brazil", "Brasil", "Lula", "Bolsonaro", "Moraes", "Tarcisio",
        "Bank of Brazil", "Selic", "Petrobras", "Libertadores",
        "Brasileirao", "Copa do Brasil", "Flamengo", "Palmeiras",
        "Corinthians", "Botafogo", "Sao Paulo", "Alex Pereira",
    ]

    for q in queries:
        for param_style in [
            f"https://gamma-api.polymarket.com/public-search?q={urllib.parse.quote(q)}&limit_per_type=50",
            f"https://gamma-api.polymarket.com/events?slug_contains={urllib.parse.quote(q.lower().replace(' ', '-'))}&closed=false&limit=50",
        ]:
            try:
                data = fetch_json(param_style, timeout=15)
                evs = data.get("events", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
                count_added = 0
                for ev in evs:
                    if isinstance(ev, dict) and ev.get("id"):
                        if not ev.get("closed", False) and ev.get("active", True):
                            events_by_id[str(ev["id"])] = ev
                            count_added += 1
                diagnostics["queries_tested"].append({"url": param_style, "active_found": count_added})
            except Exception as e:
                diagnostics["queries_tested"].append({"url": param_style, "error": str(e)})

    # Varredura adicional dos top 1000 eventos abertos da Polymarket
    for offset in range(0, 1000, 100):
        url = f"https://gamma-api.polymarket.com/events?active=true&closed=false&limit=100&offset={offset}"
        try:
            batch = fetch_json(url, timeout=15)
            if not isinstance(batch, list) or not batch:
                break
            for ev in batch:
                if isinstance(ev, dict) and ev.get("id"):
                    blob = " ".join([
                        str(ev.get("title", "")),
                        str(ev.get("slug", "")),
                        " ".join(str(m.get("question", "")) + " " + str(m.get("groupItemTitle", "")) for m in (ev.get("markets") or [])),
                    ])
                    if matches_brazil(blob):
                        events_by_id[str(ev["id"])] = ev
        except Exception:
            break

    diagnostics["total_unique_events_inspected"] = len(events_by_id)

    parsed_events = []
    for eid, ev in events_by_id.items():
        title = str(ev.get("title", "")).strip()
        slug = str(ev.get("slug", "")).strip()
        title_is_brazil = matches_brazil(title + " " + slug)

        all_open_markets = []
        brazil_specific_markets = []

        for m in (ev.get("markets") or []):
            if m.get("closed", False) or not m.get("active", True):
                continue
            q = str(m.get("question") or m.get("groupItemTitle") or title).strip()
            g = str(m.get("groupItemTitle") or "").strip()

            outcomes = m.get("outcomes", "[]")
            outcome_prices = m.get("outcomePrices", "[]")
            try:
                if isinstance(outcomes, str):
                    outcomes = json.loads(outcomes)
            except Exception:
                pass
            try:
                if isinstance(outcome_prices, str):
                    outcome_prices = json.loads(outcome_prices)
            except Exception:
                pass

            yes_p = safe_float(outcome_prices[0]) if isinstance(outcome_prices, list) and len(outcome_prices) > 0 else safe_float(m.get("lastTradePrice"))
            no_p = safe_float(outcome_prices[1], round(1.0 - yes_p, 4)) if isinstance(outcome_prices, list) and len(outcome_prices) > 1 else round(1.0 - yes_p, 4)
            vol = safe_float(m.get("volumeNum") or m.get("volume"))
            liq = safe_float(m.get("liquidityNum") or m.get("liquidity"))

            m_obj = {
                "market_id": str(m.get("id", "")),
                "question": q,
                "group_item_title": g,
                "slug": str(m.get("slug", "")),
                "yes_price_usd": round(yes_p, 4),
                "no_price_usd": round(no_p, 4),
                "best_bid_usd": safe_float(m.get("bestBid"), round(max(0.0, yes_p - 0.01), 4)),
                "best_ask_usd": safe_float(m.get("bestAsk"), round(min(1.0, yes_p + 0.01), 4)),
                "volume_usd": round(vol, 2),
                "liquidity_usd": round(liq, 2),
                "end_date": str(m.get("endDate", "")),
                "is_brazil_leg": bool(title_is_brazil or matches_brazil(q + " " + g)),
            }
            all_open_markets.append(m_obj)
            if m_obj["is_brazil_leg"]:
                brazil_specific_markets.append(m_obj)

        # Se nem o titulo do evento nem nenhum sub-mercado ativo bate com o Brasil, descartar falso positivo!
        if not title_is_brazil and not brazil_specific_markets:
            continue

        total_event_vol = round(safe_float(ev.get("volume")), 2)
        total_event_liq = round(safe_float(ev.get("liquidity")), 2)
        vol_24h = round(safe_float(ev.get("volume24hr")), 2)

        # Volume atribuivel diretamente ao Brasil:
        # Se o evento inteiro e sobre o Brasil, usa total_event_vol; se for um evento global (ex: "Next leader out of power"),
        # calcula tanto o volume do evento global quanto o volume especifico do sub-contrato do Brasil (ex: Lula)!
        brazil_leg_vol = total_event_vol if title_is_brazil else round(sum(m["volume_usd"] for m in brazil_specific_markets), 2)
        brazil_leg_liq = total_event_liq if title_is_brazil else round(sum(m["liquidity_usd"] for m in brazil_specific_markets), 2)

        parsed_events.append({
            "exchange": "Polymarket",
            "event_id": eid,
            "title": title,
            "slug": slug,
            "url": f"https://polymarket.com/event/{slug}",
            "scope": "100% Brasil" if title_is_brazil else "Global com Sub-Contrato Brasil",
            "event_total_volume_usd": total_event_vol,
            "event_volume_24h_usd": vol_24h,
            "event_liquidity_usd": total_event_liq,
            "brazil_attributable_volume_usd": brazil_leg_vol,
            "brazil_attributable_liquidity_usd": brazil_leg_liq,
            "markets_count": len(all_open_markets),
            "brazil_markets_count": len(brazil_specific_markets),
            "brazil_markets": sorted(brazil_specific_markets, key=lambda x: x["volume_usd"], reverse=True)[:10],
            "top_all_markets": sorted(all_open_markets, key=lambda x: x["volume_usd"], reverse=True)[:8],
        })

    # Ordenar estritamente pelo Volume Atribuivel ao Brasil (decrescente)
    parsed_events.sort(key=lambda x: (x["brazil_attributable_volume_usd"], x["event_total_volume_usd"]), reverse=True)
    return {"diagnostics": diagnostics, "events_count": len(parsed_events), "events": parsed_events}


def scan_kalshi_high_volume():
    """
    Varre todas as series do Brasil na Kalshi + eventos abertos e classifica por Volume de Contratos
    e Open Interest, destacando tanto as series ativas quanto o historico recente de mega-volume
    (como o 1o e 2o turno presidencial do Brasil na Kalshi) para inteligencia editorial.
    """
    diagnostics = {"series_matched": [], "total_series_scanned": 0}
    matched_events = {}

    try:
        series_data = fetch_json("https://api.elections.kalshi.com/trade-api/v2/series", timeout=25)
        series_list = series_data.get("series", []) if isinstance(series_data, dict) else []
        diagnostics["total_series_scanned"] = len(series_list)
        for s in series_list:
            s_blob = " ".join([
                str(s.get("ticker", "")),
                str(s.get("title", "")),
                str(s.get("category", "")),
                " ".join(str(t) for t in (s.get("tags") or [])),
            ])
            if matches_brazil(s_blob):
                diagnostics["series_matched"].append({
                    "ticker": s.get("ticker"),
                    "title": s.get("title"),
                    "category": s.get("category"),
                })
    except Exception as e:
        diagnostics["series_error"] = str(e)

    for s in diagnostics["series_matched"]:
        st = s.get("ticker")
        if not st:
            continue
        try:
            ev_url = f"https://api.elections.kalshi.com/trade-api/v2/events?series_ticker={urllib.parse.quote(st)}&with_nested_markets=true&limit=50"
            ev_resp = fetch_json(ev_url, timeout=15)
            for ev in (ev_resp.get("events") or []):
                matched_events[ev.get("event_ticker")] = ev
        except Exception:
            pass

    # Tambem varrer eventos gerais abertos
    cursor = None
    for _ in range(8):
        url = "https://api.elections.kalshi.com/trade-api/v2/events?status=open&with_nested_markets=true&limit=200"
        if cursor:
            url += f"&cursor={urllib.parse.quote(cursor)}"
        try:
            resp = fetch_json(url, timeout=20)
            evs = resp.get("events") or []
            for ev in evs:
                blob = " ".join([
                    str(ev.get("event_ticker", "")),
                    str(ev.get("title", "")),
                    str(ev.get("sub_title", "")),
                    " ".join(str(m.get("title", "")) + " " + str(m.get("yes_sub_title", "")) for m in (ev.get("markets") or [])),
                ])
                if matches_brazil(blob):
                    matched_events[ev.get("event_ticker")] = ev
            cursor = resp.get("cursor")
            if not cursor or not evs:
                break
        except Exception:
            break

    active_events = []
    settled_mega_events = []

    for eticker, ev in matched_events.items():
        title = str(ev.get("title", "")).strip()
        sub_title = str(ev.get("sub_title", "")).strip()
        title_is_brazil = matches_brazil(title + " " + sub_title + " " + eticker)

        active_mkts = []
        all_mkts = []
        for m in (ev.get("markets") or []):
            m_title = str(m.get("title") or m.get("yes_sub_title") or m.get("subtitle", "")).strip()
            m_sub = str(m.get("yes_sub_title", "")).strip()
            is_br_mkt = title_is_brazil or matches_brazil(m_title + " " + m_sub + " " + str(m.get("ticker", "")))
            if not is_br_mkt:
                continue

            vol = safe_float(m.get("volume_fp"))
            oi = safe_float(m.get("open_interest_fp"))
            bid = safe_float(m.get("yes_bid_dollars"))
            ask = safe_float(m.get("yes_ask_dollars"))
            last = safe_float(m.get("last_price_dollars"))

            m_obj = {
                "ticker": m.get("ticker"),
                "title": m_title,
                "yes_sub_title": m_sub,
                "status": m.get("status", ""),
                "yes_bid_usd": bid,
                "yes_ask_usd": ask,
                "no_bid_usd": safe_float(m.get("no_bid_dollars")),
                "no_ask_usd": safe_float(m.get("no_ask_dollars")),
                "last_price_usd": last,
                "volume_contracts": round(vol, 2),
                "open_interest_contracts": round(oi, 2),
                "close_time": m.get("close_time") or m.get("expiration_time"),
            }
            all_mkts.append(m_obj)
            if m.get("status") in ("active", "open"):
                active_mkts.append(m_obj)

        if active_mkts:
            tot_vol = round(sum(x["volume_contracts"] for x in active_mkts), 2)
            tot_oi = round(sum(x["open_interest_contracts"] for x in active_mkts), 2)
            active_events.append({
                "exchange": "Kalshi",
                "event_ticker": eticker,
                "series_ticker": ev.get("series_ticker", ""),
                "title": title,
                "sub_title": sub_title,
                "category": ev.get("category", ""),
                "scope": "100% Brasil" if title_is_brazil else "Global com Sub-Contrato Brasil",
                "total_volume_contracts": tot_vol,
                "total_open_interest_contracts": tot_oi,
                "active_markets_count": len(active_mkts),
                "markets": sorted(active_mkts, key=lambda x: x["volume_contracts"], reverse=True)[:10],
            })
        elif all_mkts:
            tot_vol = round(sum(x["volume_contracts"] for x in all_mkts), 2)
            if tot_vol >= 50000:
                settled_mega_events.append({
                    "event_ticker": eticker,
                    "series_ticker": ev.get("series_ticker", ""),
                    "title": title,
                    "sub_title": sub_title,
                    "category": ev.get("category", ""),
                    "total_volume_contracts": tot_vol,
                    "top_markets": sorted(all_mkts, key=lambda x: x["volume_contracts"], reverse=True)[:5],
                })

    active_events.sort(key=lambda x: x["total_volume_contracts"], reverse=True)
    settled_mega_events.sort(key=lambda x: x["total_volume_contracts"], reverse=True)

    return {
        "diagnostics": diagnostics,
        "active_events_count": len(active_events),
        "active_events": active_events,
        "historical_mega_volume_events": settled_mega_events[:15],
    }


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("[1/2] Executando varredura profunda por VOLUME na Polymarket (limit_per_type=50)...")
    poly = scan_polymarket_high_volume()
    print(f"      -> Eventos Polymarket com exposicao real ao Brasil: {poly['events_count']}")

    print("[2/2] Executando varredura por VOLUME na Kalshi (97 series Brasil)...")
    kalshi = scan_kalshi_high_volume()
    print(f"      -> Eventos Kalshi ATIVOS ordenados por volume: {kalshi['active_events_count']}")
    print(f"      -> Mega-eventos Brasil recem-liquidados na Kalshi (>50k contratos): {len(kalshi['historical_mega_volume_events'])}")

    out = {
        "scanned_at": datetime.now().isoformat(),
        "polymarket_high_volume": poly,
        "kalshi_high_volume": kalshi,
    }
    path = DATA_DIR / "brazil_markets_high_volume_priority.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Salvo em: {path}")


if __name__ == "__main__":
    main()
