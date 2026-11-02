# -*- coding: utf-8 -*-
"""
NWX-Argon — Estudo de Sazonalidade x Ciclo Eleitoral (S&P 500)
==============================================================
Reproduz com DADOS REAIS (Yahoo Finance ^GSPC, diário desde 1950) o tipo de estudo
apresentado no vídeo "ESTÃO PRONTOS PARA O RALLY DE NATAL? | Estudo de sazonalidade
do mercado americano" (Igor Mundstock, 01/11/2026):

  1. Santa Claus Rally (definição Stock Trader's Almanac: últimos 5 pregões de dezembro
     + 2 primeiros pregões de janeiro).
  2. Retorno de Novembro, Dezembro e Nov+Dez (bimestre pós-eleição).
  3. Segmentação pelo Ciclo Presidencial dos EUA:
       - Ano 1 = pós-eleição presidencial (ex.: 2025)
       - Ano 2 = ano de MIDTERM (ex.: 2026)  <-- ano corrente
       - Ano 3 = pré-eleitoral (ex.: 2027)
       - Ano 4 = ano de eleição presidencial (ex.: 2024)

Fonte única: https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC
Nenhum número é inventado: tudo sai do histórico baixado. Saída em sandbox/runs/.
"""

import json
import statistics
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "sandbox" / "runs"
DATA = ROOT / "sandbox" / "data"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def cycle_year(y: int) -> int:
    # 1952, 1956 ... 2024 = ano 4 (eleição presidencial)
    return ((y - 1949) % 4) + 1


CYCLE_LABEL = {1: "Ano 1 (pós-eleição)", 2: "Ano 2 (MIDTERM)", 3: "Ano 3 (pré-eleitoral)", 4: "Ano 4 (eleição presidencial)"}


def fetch_spx():
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC"
           "?period1=-631152000&period2=9999999999&interval=1d")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode("utf-8"))
    res = d["chart"]["result"][0]
    ts = res["timestamp"]
    cl = res["indicators"]["quote"][0]["close"]
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    from datetime import timedelta
    rows = [((epoch + timedelta(seconds=t)).date(), c) for t, c in zip(ts, cl) if c is not None]
    return [r for r in rows if r[0].year >= 1950]


def summarize(vals):
    if not vals:
        return {}
    return {
        "n": len(vals),
        "media_pct": round(statistics.mean(vals), 2),
        "mediana_pct": round(statistics.median(vals), 2),
        "pct_positivo": round(100 * sum(v > 0 for v in vals) / len(vals), 1),
        "pior_pct": round(min(vals), 2),
        "melhor_pct": round(max(vals), 2),
    }


def main():
    rows = fetch_spx()
    DATA.mkdir(parents=True, exist_ok=True)
    by_year = defaultdict(list)
    for dt, c in rows:
        by_year[dt.year].append((dt, c))

    last_year = rows[-1][0].year
    santa, nov, dec, novdec, q4 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    detail = []

    for y in sorted(by_year):
        if y + 1 not in by_year and y != last_year:
            continue
        yr = by_year[y]
        cy = cycle_year(y)

        def close_before(month):
            prev = [c for d, c in yr if d.month < month]
            return prev[-1] if prev else None

        def close_end(month):
            m = [c for d, c in yr if d.month == month]
            return m[-1] if m else None

        oct_end, nov_end, dec_end, sep_end = close_before(11), close_end(11), close_end(12), close_before(10)
        rec = {"ano": y, "ciclo": cy}
        if oct_end and nov_end:
            v = 100 * (nov_end / oct_end - 1); nov[cy].append(v); rec["nov_pct"] = round(v, 2)
        if nov_end and dec_end:
            v = 100 * (dec_end / nov_end - 1); dec[cy].append(v); rec["dez_pct"] = round(v, 2)
        if oct_end and dec_end:
            v = 100 * (dec_end / oct_end - 1); novdec[cy].append(v); rec["nov_dez_pct"] = round(v, 2)
        if sep_end and dec_end:
            v = 100 * (dec_end / sep_end - 1); q4[cy].append(v); rec["q4_pct"] = round(v, 2)
        # Santa Rally: close antes dos últimos 5 pregões de dez -> close do 2º pregão de jan
        decs = [c for d, c in yr if d.month == 12]
        jans = [c for d, c in by_year.get(y + 1, []) if d.month == 1]
        prior = [c for d, c in yr if d.month < 12 or True]
        if len(decs) >= 6 and len(jans) >= 2:
            idx_dec = [i for i, (d, c) in enumerate(yr) if d.month == 12]
            start = yr[idx_dec[-5] - 1][1]
            v = 100 * (jans[1] / start - 1); santa[cy].append(v); rec["santa_rally_pct"] = round(v, 2)
        detail.append(rec)

    def pack(store):
        out = {CYCLE_LABEL[k]: summarize(store[k]) for k in sorted(store)}
        out["TODOS"] = summarize([v for k in store for v in store[k]])
        return out

    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "fonte": "Yahoo Finance ^GSPC diário (sem dividendos), 1950–hoje",
        "ultimo_pregao": str(rows[-1][0]),
        "ultimo_close": round(rows[-1][1], 2),
        "ano_corrente_ciclo": CYCLE_LABEL[cycle_year(last_year)],
        "santa_claus_rally": pack(santa),
        "novembro": pack(nov),
        "dezembro": pack(dec),
        "nov_dez": pack(novdec),
        "q4_set_a_dez": pack(q4),
        "midterm_years_detail": [r for r in detail if r["ciclo"] == 2],
    }
    RUNS.mkdir(parents=True, exist_ok=True)
    out = RUNS / "SEASONALITY_ELECTION_CYCLE_SPX.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("ultimo_pregao", "ano_corrente_ciclo", "santa_claus_rally", "nov_dez", "q4_set_a_dez")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
