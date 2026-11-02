# -*- coding: utf-8 -*-
"""
NWX-Argon — Verificação das afirmações do vídeo (Igor Mundstock, 01/11/2026)
"ESTÃO PRONTOS PARA O RALLY DE NATAL? | Estudo de sazonalidade do mercado americano"

Cada afirmação do vídeo é recalculada com dados brutos (Yahoo Finance chart API).
Saída: sandbox/runs/VIDEO_CLAIMS_VERIFICATION.json
"""
import json
import statistics
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "sandbox" / "runs"
H = {"User-Agent": "Mozilla/5.0"}
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def fetch(ticker, period1=-631152000):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}"
           f"?period1={period1}&period2=9999999999&interval=1d")
    with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30) as r:
        res = json.loads(r.read().decode())["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    return [((EPOCH + timedelta(seconds=t)).date(), c) for t, c in zip(res["timestamp"], q["close"]) if c is not None]


def cyc(y):
    return ((y - 1949) % 4) + 1


def stats(v):
    if not v:
        return None
    return {"n": len(v), "media": round(statistics.mean(v), 2), "mediana": round(statistics.median(v), 2),
            "pct_pos": round(100 * sum(x > 0 for x in v) / len(v), 1), "pior": round(min(v), 2), "melhor": round(max(v), 2)}


def month_end(rows, y, m):
    v = [c for d, c in rows if d.year == y and d.month == m]
    return v[-1] if v else None


def close_on_or_after(rows, target):
    for d, c in rows:
        if d >= target:
            return d, c
    return None, None


def midterm_election_day(y):
    # 1ª terça-feira após a 1ª segunda-feira de novembro
    d = datetime(y, 11, 2).date()
    while d.weekday() != 1:
        d += timedelta(days=1)
    return d


def main():
    spx = [r for r in fetch("^GSPC") if r[0].year >= 1949]
    last = spx[-1][0]
    years = sorted({d.year for d, _ in spx if 1950 <= d.year})

    # 1) Retorno de ano-calendário por fase do ciclo
    cal = defaultdict(list)
    for y in years:
        a, b = month_end(spx, y - 1, 12), month_end(spx, y, 12)
        if a and b and y < last.year:
            cal[cyc(y)].append(100 * (b / a - 1))

    # 2) Retorno mensal Out / Nov: midterm vs outros
    monthly = {}
    for m in (10, 11, 12):
        mid, oth = [], []
        for y in years:
            a = month_end(spx, y, m - 1)
            b = month_end(spx, y, m)
            if a and b and not (y == last.year and last.month == m):
                (mid if cyc(y) == 2 else oth).append(100 * (b / a - 1))
        monthly[m] = {"midterm": stats(mid), "outros": stats(oth)}

    # 3) 12 meses à frente em anos de midterm (3 âncoras distintas)
    fwd = {"fim_set": [], "fim_out": [], "dia_eleicao": [], "minimo_set_out": []}
    detail = []
    for y in years:
        if cyc(y) != 2 or y >= last.year:
            continue
        rec = {"ano": y}
        anchors = {
            "fim_set": (datetime(y, 9, 30).date(), month_end(spx, y, 9)),
            "fim_out": (datetime(y, 10, 31).date(), month_end(spx, y, 10)),
            "dia_eleicao": close_on_or_after(spx, midterm_election_day(y)),
        }
        win = [(d, c) for d, c in spx if d.year == y and d.month in (9, 10)]
        lo = min(win, key=lambda x: x[1])
        anchors["minimo_set_out"] = lo
        for k, (d0, c0) in anchors.items():
            d1, c1 = close_on_or_after(spx, d0.replace(year=d0.year + 1))
            if c0 and c1:
                r = 100 * (c1 / c0 - 1)
                fwd[k].append(r)
                rec[k] = round(r, 2)
        detail.append(rec)

    # 4) Nov+Dez (fim de out -> fim de dez) em midterm
    novdec_mid = [100 * (month_end(spx, y, 12) / month_end(spx, y, 10) - 1) for y in years if cyc(y) == 2 and y < last.year]

    # 5) Fatos de mercado citados no vídeo (sexta 30/10/2026)
    def day_chg(t):
        r = fetch(t, period1=int((datetime(2025, 9, 1, tzinfo=timezone.utc) - EPOCH).total_seconds()))
        d, c = r[-1]
        p = r[-2][1]
        yr = [x for x in r if x[0].year == d.year]
        lo = min(yr, key=lambda x: x[1])
        hi = max(r, key=lambda x: x[1])
        return {"data": str(d), "close": round(c, 2), "var_dia_pct": round(100 * (c / p - 1), 2),
                "minimo_do_ano": round(lo[1], 2), "data_minimo_ano": str(lo[0]),
                "dist_max_desde_set25_pct": round(100 * (c / hi[1] - 1), 2)}

    market = {}
    for t in ["^GSPC", "^IXIC", "^RUT", "RSP", "XLK", "GC=F", "SI=F", "HG=F", "BZ=F", "CL=F", "^TNX", "^TYX", "DX-Y.NYB"]:
        try:
            market[t] = day_chg(t)
        except Exception as e:
            market[t] = {"erro": str(e)}
    oct26 = None
    a, b = month_end(spx, 2026, 9), month_end(spx, 2026, 10)
    if a and b:
        oct26 = round(100 * (b / a - 1), 2)

    out = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "fonte": "Yahoo Finance chart API (^GSPC preço, sem dividendos)",
        "ultimo_pregao": str(last),
        "ano_calendario_por_ciclo": {f"ano_{k}": stats(cal[k]) for k in sorted(cal)},
        "mensal": {str(k): v for k, v in monthly.items()},
        "outubro_2026_pct": oct26,
        "nov_dez_midterm": stats(novdec_mid),
        "forward_12m_midterm": {k: stats(v) for k, v in fwd.items()},
        "forward_12m_detalhe": detail,
        "mercado_sexta_30out2026": market,
    }
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / "VIDEO_CLAIMS_VERIFICATION.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=True, indent=1))


if __name__ == "__main__":
    main()
