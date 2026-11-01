# -*- coding: utf-8 -*-
"""
Argon Brazil Prediction Markets Scanner (Polymarket + Kalshi)
=============================================================
Agente Responsavel: Gabriel Torres (05_gabriel_torres_investigador_fontes)
Apoio Analitico: Clara Mendonca (02_clara_mendonca_analista_dados)
Orquestrador: Axio Vance (00_axio_orquestrador)

Objetivo:
Validar e executar a busca automatizada de operacoes/mercados que envolvem o BRASIL
nas duas maiores bolsas/mercados de predicao do mundo:
1. Polymarket (Gamma API: `https://gamma-api.polymarket.com`)
2. Kalshi (Trade API v2: `https://api.elections.kalshi.com/trade-api/v2`)
"""

import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "sandbox" / "data"

BRAZIL_KEYWORDS = [
    r"\bbrazil\b",
    r"\bbrasil\b",
    r"\bbrazilian\b",
    r"\blula\b",
    r"\bbolsonaro\b",
    r"\btarcisio\b",
    r"\btarcísio\b",
    r"\bhaddad\b",
    r"\bmoraes\b",
    r"\bpablo marcal\b",
    r"\bselic\b",
    r"\bibovespa\b",
    r"\bbovespa\b",
    r"\bbrl\b",
    r"\bpetrobras\b",
    r"\bsao paulo\b",
    r"\bsão paulo\b",
    r"\brio de janeiro\b",
    r"\bcopa do brasil\b",
    r"\bbrasileirao\b",
    r"\bbrasileirão\b",
    r"\bflamengo\b",
    r"\bpalmeiras\b",
    r"\bcorinthians\b",
    r"\bbotafogo\b",
    r"\bneymar\b",
    r"\bvinicius jr\b",
    r"\bvini jr\b",
    r"\banderson silva\b",
    r"\balex pereira\b",
    r"\bpankration\b",
    r"\bcharles oliveira\b",
]

BRAZIL_REGEX = re.compile("|".join(BRAZIL_KEYWORDS), re.IGNORECASE)


def fetch_json(url: str, timeout: int = 20):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ArgonQuantEngine/2.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def matches_brazil(text: str) -> bool:
    if not text:
        return False
    return bool(BRAZIL_REGEX.search(text))


def scan_polymarket_brazil():
    """
    Valida multiplas rotas da Gamma API da Polymarket para capturar 100% dos mercados ativos sobre o Brasil:
    1. Rota de eventos paginada (`/events?active=true&closed=false&limit=100&offset=...`)
    2. Rota de busca textual (`/public-search?q=Brazil`, `q=Brasil`, `q=Lula`, `q=Bolsonaro`) se disponivel
    """
    events_by_id = {}
    diagnostics = {"endpoints_tested": [], "total_events_scanned": 0}

    # 1. Testar public-search / events com queries especificas e varredura paginada de eventos ativos
    search_queries = ["Brazil", "Brasil", "Lula", "Bolsonaro", "BRL"]
    for q in search_queries:
        url = f"https://gamma-api.polymarket.com/public-search?q={urllib.parse.quote(q)}"
        try:
            data = fetch_json(url, timeout=15)
            evs = data.get("events", []) if isinstance(data, dict) else []
            diagnostics["endpoints_tested"].append({"url": url, "status": "OK", "events_found": len(evs)})
            for ev in evs:
                if isinstance(ev, dict) and ev.get("id"):
                    # Verifica se esta aberto/ativo
                    if not ev.get("closed", False) and ev.get("active", True):
                        events_by_id[str(ev["id"])] = ev
        except Exception as e:
            diagnostics["endpoints_tested"].append({"url": url, "status": f"ERR: {e}"})

    # 2. Varredura paginada de eventos ativos por volume na Polymarket (`/events?active=true&closed=false`)
    for offset in range(0, 1000, 100):
        url = f"https://gamma-api.polymarket.com/events?active=true&closed=false&limit=100&offset={offset}&order=volume&ascending=false"
        try:
            batch = fetch_json(url, timeout=15)
            if not isinstance(batch, list) or not batch:
                break
            diagnostics["total_events_scanned"] += len(batch)
            for ev in batch:
                blob = " ".join([
                    str(ev.get("title", "")),
                    str(ev.get("slug", "")),
                    str(ev.get("description", "")),
                    " ".join(str(m.get("question", "")) for m in (ev.get("markets") or [])),
                ])
                if matches_brazil(blob):
                    events_by_id[str(ev["id"])] = ev
        except Exception as e:
            diagnostics["endpoints_tested"].append({"url": url, "status": f"ERR: {e}"})
            break

    # 3. Filtrar estritamente eventos cujo titulo, slug, descricao ou pergunta contenha referencia ao Brasil
    parsed_events = []
    for eid, ev in events_by_id.items():
        blob = " ".join([
            str(ev.get("title", "")),
            str(ev.get("slug", "")),
            str(ev.get("description", "")),
            " ".join(str(m.get("question", "")) for m in (ev.get("markets") or [])),
        ])
        if not matches_brazil(blob):
            continue

        markets_summary = []
        for m in (ev.get("markets") or []):
            if m.get("closed", False) or not m.get("active", True):
                continue
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

            markets_summary.append({
                "market_id": m.get("id"),
                "question": m.get("question") or m.get("groupItemTitle") or ev.get("title"),
                "group_item_title": m.get("groupItemTitle", ""),
                "condition_id": m.get("conditionId", ""),
                "slug": m.get("slug", ""),
                "outcomes": outcomes,
                "outcome_prices": outcome_prices,
                "best_bid": m.get("bestBid"),
                "best_ask": m.get("bestAsk"),
                "last_trade_price": m.get("lastTradePrice"),
                "volume_usd": float(m.get("volumeNum") or m.get("volume") or 0.0),
                "liquidity_usd": float(m.get("liquidityNum") or m.get("liquidity") or 0.0),
                "end_date": m.get("endDate", ""),
            })

        if not markets_summary:
            continue

        parsed_events.append({
            "event_id": eid,
            "title": ev.get("title", ""),
            "slug": ev.get("slug", ""),
            "url": f"https://polymarket.com/event/{ev.get('slug', '')}",
            "volume_usd": float(ev.get("volume") or 0.0),
            "liquidity_usd": float(ev.get("liquidity") or 0.0),
            "start_date": ev.get("startDate", ""),
            "end_date": ev.get("endDate", ""),
            "markets_count": len(markets_summary),
            "markets": sorted(markets_summary, key=lambda x: x["volume_usd"], reverse=True)[:15],
        })

    parsed_events.sort(key=lambda x: x["volume_usd"], reverse=True)
    return {"diagnostics": diagnostics, "events_count": len(parsed_events), "events": parsed_events}


def scan_kalshi_brazil():
    """
    Valida multiplas rotas da Kalshi Trade API v2 (`https://api.elections.kalshi.com/trade-api/v2`):
    1. Varredura de Series (`/series`) procurando Brazil, Brasil, Lula, Bolsonaro, BRL, Copa, etc.
    2. Varredura de Eventos Abertos (`/events?status=open&with_nested_markets=true&limit=200`) paginada por cursor.
    """
    diagnostics = {"series_matched": [], "total_series_scanned": 0, "total_open_events_scanned": 0}
    matched_events = {}

    # 1. Buscar todas as series da Kalshi para encontrar series especificas do Brasil
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
                    "frequency": s.get("frequency"),
                })
    except Exception as e:
        diagnostics["series_error"] = str(e)

    # 2. Para cada serie do Brasil encontrada, buscar eventos (open e recentes)
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

    # 3. Varredura paginada de eventos abertos gerais (`/events?status=open&with_nested_markets=true&limit=200`)
    cursor = None
    for _ in range(8):
        url = "https://api.elections.kalshi.com/trade-api/v2/events?status=open&with_nested_markets=true&limit=200"
        if cursor:
            url += f"&cursor={urllib.parse.quote(cursor)}"
        try:
            resp = fetch_json(url, timeout=20)
            evs = resp.get("events") or []
            diagnostics["total_open_events_scanned"] += len(evs)
            for ev in evs:
                blob = " ".join([
                    str(ev.get("event_ticker", "")),
                    str(ev.get("title", "")),
                    str(ev.get("sub_title", "")),
                    str(ev.get("category", "")),
                    " ".join(str(m.get("title", "")) + " " + str(m.get("subtitle", "")) + " " + str(m.get("yes_sub_title", "")) for m in (ev.get("markets") or [])),
                ])
                if matches_brazil(blob):
                    matched_events[ev.get("event_ticker")] = ev
            cursor = resp.get("cursor")
            if not cursor or not evs:
                break
        except Exception as e:
            diagnostics["events_scan_error"] = str(e)
            break

    parsed_events = []
    for eticker, ev in matched_events.items():
        markets_out = []
        for m in (ev.get("markets") or []):
            markets_out.append({
                "ticker": m.get("ticker"),
                "title": m.get("title") or m.get("yes_sub_title") or m.get("subtitle", ""),
                "yes_sub_title": m.get("yes_sub_title", ""),
                "status": m.get("status", ""),
                "yes_bid_dollars": m.get("yes_bid_dollars"),
                "yes_ask_dollars": m.get("yes_ask_dollars"),
                "no_bid_dollars": m.get("no_bid_dollars"),
                "no_ask_dollars": m.get("no_ask_dollars"),
                "last_price_dollars": m.get("last_price_dollars"),
                "volume_fp": m.get("volume_fp"),
                "open_interest_fp": m.get("open_interest_fp"),
                "close_time": m.get("close_time") or m.get("expiration_time"),
            })
        parsed_events.append({
            "event_ticker": eticker,
            "series_ticker": ev.get("series_ticker", ""),
            "title": ev.get("title", ""),
            "sub_title": ev.get("sub_title", ""),
            "category": ev.get("category", ""),
            "markets_count": len(markets_out),
            "markets": markets_out[:15],
        })

    return {"diagnostics": diagnostics, "events_count": len(parsed_events), "events": parsed_events}


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("[1/2] Consultando Polymarket (Gamma API) para operacoes envolvendo Brazil/Brasil...")
    poly_res = scan_polymarket_brazil()
    print(f"      -> Eventos Polymarket encontrados: {poly_res['events_count']}")

    print("[2/2] Consultando Kalshi (Trade API v2) para series e eventos envolvendo Brazil/Brasil...")
    kalshi_res = scan_kalshi_brazil()
    print(f"      -> Series Kalshi encontradas: {len(kalshi_res['diagnostics'].get('series_matched', []))}")
    print(f"      -> Eventos Kalshi encontrados: {kalshi_res['events_count']}")

    output = {
        "scanned_at": datetime.now().isoformat(),
        "polymarket_brazil": poly_res,
        "kalshi_brazil": kalshi_res,
    }
    out_path = DATA_DIR / "brazil_markets_polymarket_kalshi.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Resultado salvo em: {out_path}")


if __name__ == "__main__":
    main()
