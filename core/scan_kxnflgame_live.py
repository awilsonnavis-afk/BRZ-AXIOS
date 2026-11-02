# -*- coding: utf-8 -*-
"""
Kalshi KXNFLGAME Live Scanner & Post-Mortem Evaluator
=====================================================
Consulta a API oficial da Kalshi (series_ticker=KXNFLGAME) para:
1. Verificar o fechamento/status de KC Chiefs vs DEN Broncos (KXNFLGAME-26NOV01KCDEN)
2. Listar todos os jogos ativos/abertos de KXNFLGAME com maior volume neste momento (20:42 ET - Sunday Night Football / Semana 9-10)
"""
import json
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "sandbox" / "data"


def fetch_json(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ArgonKalshiNFLScanner/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def main():
    # 1. Fetch events in series KXNFLGAME (both open and settled/closed recently)
    events_open = fetch_json("https://api.elections.kalshi.com/trade-api/v2/events?series_ticker=KXNFLGAME&status=open&with_nested_markets=true&limit=100")
    events_settled = fetch_json("https://api.elections.kalshi.com/trade-api/v2/events?series_ticker=KXNFLGAME&status=settled&with_nested_markets=true&limit=50")
    events_closed = fetch_json("https://api.elections.kalshi.com/trade-api/v2/events?series_ticker=KXNFLGAME&status=closed&with_nested_markets=true&limit=50")
    
    # Also fetch directly KXNFLGAME-26NOV01KCDEN
    kcden_event = None
    try:
        kcden_event = fetch_json("https://api.elections.kalshi.com/trade-api/v2/events/KXNFLGAME-26NOV01KCDEN?with_nested_markets=true")
    except Exception as e:
        kcden_event = {"error": str(e)}

    out = {
        "kcden_event": kcden_event,
        "open_events_count": len(events_open.get("events", [])),
        "open_events": events_open.get("events", []),
        "closed_events": events_closed.get("events", [])[:15],
        "settled_events": events_settled.get("events", [])[:15],
    }

    out_path = DATA_DIR / "kalshi_kxnflgame_live_scan.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== KCDEN STATUS ===")
    if kcden_event and "event" in kcden_event:
        ev = kcden_event["event"]
        print(f"Event: {ev.get('event_ticker')} | Title: {ev.get('title')}")
        for m in ev.get("markets", []):
            print(
                f"  Market: {m.get('ticker')} | Status: {m.get('status')} | Result: {m.get('result')} | "
                f"Last: {m.get('last_price_dollars')} | YesBid: {m.get('yes_bid_dollars')} | YesAsk: {m.get('yes_ask_dollars')} | "
                f"Vol: {m.get('volume_fp')}"
            )
    else:
        print(kcden_event)

    print("\n=== OPEN KXNFLGAME EVENTS (SORTED BY TOTAL VOLUME) ===")
    open_list = []
    for ev in events_open.get("events", []):
        mkts = ev.get("markets", [])
        tot_vol = sum(float(m.get("volume_fp") or m.get("volume") or 0) for m in mkts)
        tot_liq = sum(float(m.get("liquidity_dollars") or 0) for m in mkts)
        open_list.append((tot_vol, tot_liq, ev))

    open_list.sort(key=lambda x: x[0], reverse=True)
    for vol, liq, ev in open_list[:15]:
        print(f"\nEvent: {ev.get('event_ticker')} | {ev.get('title')} | Total Vol: ${vol:,.2f} | Liq: ${liq:,.2f}")
        for m in ev.get("markets", []):
            print(
                f"  -> {m.get('ticker')} ({m.get('yes_sub_title') or m.get('subtitle')}): "
                f"Status={m.get('status')} | Last={m.get('last_price_dollars')} | "
                f"Bid={m.get('yes_bid_dollars')} / Ask={m.get('yes_ask_dollars')} | Vol={m.get('volume_fp')}"
            )


if __name__ == "__main__":
    main()
