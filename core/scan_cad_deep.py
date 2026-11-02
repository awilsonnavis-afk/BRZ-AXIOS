# -*- coding: utf-8 -*-
"""
Deep Scanner para Opcoes Tradicionais (FXC / 6C=F / USDCAD) e Opcoes Binarias (Kalshi / Polymarket) do Dolar Canadense
"""

import json
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "sandbox" / "data"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def fetch_json(url: str, timeout: int = 12):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def main():
    kalshi_series_targets = [
        "KXUSDCADW", "KXUSDCADAD", "KXUSDCADAW", "KXUSDCADAH", "KXUSDCAD15M",
        "KXCACPIYOY", "KXCANOREOY", "KXCANCUTS", "KXCBDECISIONCANADA",
        "KXCANRECESSION", "KXCANUSRAISE", "KX232ALUMCA", "KXCANEVTRTARIFF"
    ]
    kalshi_events = []
    for st in kalshi_series_targets:
        try:
            data = fetch_json(f"https://api.elections.kalshi.com/trade-api/v2/events?series_ticker={st}&with_nested_markets=true")
            for ev in data.get("events", []):
                kalshi_events.append(ev)
        except Exception as e:
            print(f"Error {st}: {e}")

    poly_ids = ["200525", "991303", "872544", "1280517"]
    poly_events = []
    for pid in poly_ids:
        try:
            ev = fetch_json(f"https://gamma-api.polymarket.com/events/{pid}")
            poly_events.append(ev)
        except Exception as e:
            print(f"Poly err {pid}: {e}")

    out = {
        "kalshi_targeted_events": kalshi_events,
        "polymarket_targeted_events": poly_events,
    }
    p = DATA_DIR / "cad_deep_markets.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(kalshi_events)} Kalshi events and {len(poly_events)} Polymarket events to {p}")
    for ev in kalshi_events:
        mkts = ev.get("markets", [])
        active_mkts = [m for m in mkts if m.get("status") == "active"]
        vol = sum(float(m.get("volume_fp") or m.get("volume") or 0) for m in mkts)
        if mkts:
            print(f"KALSHI: {ev['event_ticker']} | {ev['title']} | total_mkts={len(mkts)} active={len(active_mkts)} | vol=${vol:,.2f}")
    for ev in poly_events:
        print(f"POLY: {ev.get('id')} | {ev.get('title')} | vol=${float(ev.get('volume') or 0):,.2f} | mkts={len(ev.get('markets', []))}")
        for m in ev.get("markets", []):
            print(f"   -> {m.get('question')} | bid={m.get('bestBid')} ask={m.get('bestAsk')} last={m.get('lastTradePrice')} vol=${float(m.get('volume') or 0):,.2f}")


if __name__ == "__main__":
    main()
