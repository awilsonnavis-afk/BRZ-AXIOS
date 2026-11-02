# -*- coding: utf-8 -*-
"""
Scanner de Opcoes de Dolar Canadense (CAD/USD, USD/CAD, FX Options 6C=F / CADUSD=X & Kalshi/Polymarket CAD)
===========================================================================================================
Busca dados reais de:
1. Yahoo Finance (Options Chain de FXC - Invesco CurrencyShares Canadian Dollar Trust, ou futuros/spot USDCAD=X / CADUSD=X)
2. Kalshi Trade API v2 (mercados de USD/CAD, Bank of Canada, CanadaFX)
3. Polymarket Gamma API (mercados de Canada / CAD / Bank of Canada)
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
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


def scan_spot_and_macro_yahoo():
    results = {}
    tickers = ["CAD=X", "CADUSD=X", "FXC", "CL=F", "^TNX"]
    for t in tickers:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=3mo&interval=1d"
            data = fetch_json(url)
            res = data["chart"]["result"][0]
            meta = res["meta"]
            closes = [c for c in res["indicators"]["quote"][0].get("close", []) if c is not None]
            highs = [h for h in res["indicators"]["quote"][0].get("high", []) if h is not None]
            lows = [l for l in res["indicators"]["quote"][0].get("low", []) if l is not None]
            results[t] = {
                "symbol": t,
                "regularMarketPrice": meta.get("regularMarketPrice"),
                "previousClose": meta.get("chartPreviousClose") or meta.get("previousClose"),
                "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh"),
                "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow"),
                "closes_3mo_count": len(closes),
                "closes_last_10": [round(x, 5) for x in closes[-10:]],
                "high_3mo": round(max(highs), 5) if highs else None,
                "low_3mo": round(min(lows), 5) if lows else None,
            }
        except Exception as e:
            results[t] = {"error": str(e)}
    return results


def scan_kalshi_cad():
    found_series = []
    found_events = []
    try:
        series_data = fetch_json("https://api.elections.kalshi.com/trade-api/v2/series")
        for s in series_data.get("series", []):
            txt = f"{s.get('ticker','')} {s.get('title','')} {s.get('category','')}".lower()
            if any(k in txt for k in ["cad", "canada", "canadian", "usdcad", "boc", "bank of canada", "forex", "fx"]):
                found_series.append({
                    "ticker": s.get("ticker"),
                    "title": s.get("title"),
                    "category": s.get("category"),
                })
        for s in found_series[:25]:
            st = s["ticker"]
            try:
                ev_data = fetch_json(f"https://api.elections.kalshi.com/trade-api/v2/events?series_ticker={st}&with_nested_markets=true")
                for ev in ev_data.get("events", []):
                    found_events.append(ev)
            except Exception:
                pass
    except Exception as e:
        return {"error": str(e)}
    return {"series_count": len(found_series), "series": found_series, "events_count": len(found_events), "events": found_events}


def scan_polymarket_cad():
    events = []
    for q in ["Canada", "Canadian Dollar", "Bank of Canada", "CAD"]:
        try:
            url = f"https://gamma-api.polymarket.com/public-search?q={urllib.parse.quote(q)}"
            data = fetch_json(url)
            for ev in data.get("events", []):
                if ev.get("active") and not ev.get("closed"):
                    events.append({
                        "id": ev.get("id"),
                        "title": ev.get("title"),
                        "slug": ev.get("slug"),
                        "volume": ev.get("volume"),
                        "markets": [
                            {
                                "question": m.get("question"),
                                "outcomePrices": m.get("outcomePrices"),
                                "volume": m.get("volume"),
                                "bestBid": m.get("bestBid"),
                                "bestAsk": m.get("bestAsk"),
                            }
                            for m in ev.get("markets", [])[:6]
                        ],
                    })
        except Exception:
            pass
    # deduplicate
    seen = set()
    dedup = []
    for e in events:
        if e["id"] not in seen:
            seen.add(e["id"])
            dedup.append(e)
    return dedup


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    spot = scan_spot_and_macro_yahoo()
    kalshi = scan_kalshi_cad()
    poly = scan_polymarket_cad()
    out = {
        "scanned_at_utc": datetime.now(timezone.utc).isoformat(),
        "yahoo_spot_and_fxc": spot,
        "kalshi_cad_markets": kalshi,
        "polymarket_cad_markets": poly,
    }
    out_path = DATA_DIR / "cad_options_live_scan.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved scan to {out_path}")
    print("Spot summary:", json.dumps(spot, indent=2))
    print(f"Kalshi CAD series={kalshi.get('series_count')}, events={kalshi.get('events_count')}")
    print(f"Polymarket CAD active events={len(poly)}")


if __name__ == "__main__":
    main()
