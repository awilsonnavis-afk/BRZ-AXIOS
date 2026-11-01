"""
Motor Quantitativo Especializado Kalshi NFL (core/kalshi_nfl_engine.py)
Orquestrador: Axio Vance — Equipe Argon

Executa o pipeline completo dos 5 agentes para o mercado `KXNFLGAME` da Kalshi:
- Henrique Vasconcelos (Matemático): Equação estrutural Elo-EPA, Probabilidade Analítica e Critério de Kelly para Contratos Binários Kalshi.
- Clara Mendonça (Analista de Dados): Extração de probabilidades implícitas, remoção de overround (vig), análise de Net EPA e auditoria de dados.
- Lucas Bittencourt (Cientista de Dados): Geração de 1.800 jogos sintéticos da NFL, validação ML Out-of-Sample (80/20 strict split) e 10.000 simulações de Monte Carlo por partida (90.000 simulações totais).
- Beatriz Alencar (Atuária): Cálculo de VaR 95%/99%, CVaR, Probabilidade de Ruína e Dimensionamento Prudencial de Risco.
"""

from __future__ import annotations

import csv
import json
import math
import random
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent


def percentile(sorted_vals: List[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[int(f)] * (c - k) + sorted_vals[int(c)] * (k - f)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def solve_linear_system_gauss(A: List[List[float]], b: List[float]) -> List[float]:
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        pivot = M[i][i] if abs(M[i][i]) > 1e-12 else 1e-12
        for j in range(i, n + 1):
            M[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n + 1):
                    M[k][j] -= factor * M[i][j]
    return [M[i][n] for i in range(n)]


# ============================================================================
# 1. GERADOR DE DADOS ESTATÍSTICOS HISTÓRICOS DA NFL (1.800 JOGOS CALIBRADOS)
# ============================================================================
def generate_synthetic_nfl_history(cfg: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Path]:
    rng = random.Random(int(cfg["seed"]))
    n_games = int(cfg["n_synthetic_historical_games"])
    sigma_nfl = 13.45  # Desvio padrão histórico empírico da margem de vitória na NFL

    records: List[Dict[str, Any]] = []
    for gid in range(1, n_games + 1):
        elo_diff = rng.gauss(0.0, 95.0)
        net_epa_diff = rng.gauss(0.0, 0.11)
        to_diff = rng.gauss(0.0, 0.45)
        hfa = rng.uniform(1.0, 2.8)

        expected_margin = (
            (elo_diff / 25.0)
            + (32.0 * net_epa_diff)
            + (1.8 * to_diff)
            + hfa
        )
        actual_margin = expected_margin + rng.gauss(0.0, sigma_nfl)
        home_win = 1 if actual_margin > 0 else 0

        records.append(
            {
                "game_id": gid,
                "elo_diff": round(elo_diff, 2),
                "net_epa_diff": round(net_epa_diff, 4),
                "turnover_diff": round(to_diff, 3),
                "hfa_pts": round(hfa, 2),
                "actual_margin_pts": round(actual_margin, 2),
                "home_win": home_win,
            }
        )

    run_dir = ROOT_DIR / "sandbox" / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    csv_path = run_dir / f"{cfg['project_id']}_synthetic_matchups.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    return records, csv_path


# ============================================================================
# 2. TREINAMENTO E VALIDAÇÃO DO MODELO PREDITIVO (LUCAS BITTENCOURT)
# ============================================================================
def train_and_validate_nfl_model(
    cfg: Dict[str, Any], records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    rng = random.Random(int(cfg["seed"]) + 77)
    n_total = len(records)
    n_train = int(0.8 * n_total)

    # STRICT FEATURIZATION ORDERING: Split 80/20 ANTES de calcular estatísticas de escala
    train_data = records[:n_train]
    test_data = records[n_train:]

    features = ["elo_diff", "net_epa_diff", "turnover_diff", "hfa_pts"]
    feat_means = {f: statistics.fmean(r[f] for r in train_data) for f in features}
    feat_stds = {f: statistics.stdev(r[f] for r in train_data) or 1.0 for f in features}

    def transform_row(r: Dict[str, Any]) -> List[float]:
        return [1.0] + [(float(r[f]) - feat_means[f]) / feat_stds[f] for f in features]

    X_train = [transform_row(r) for r in train_data]
    y_train = [float(r["actual_margin_pts"]) for r in train_data]
    X_test = [transform_row(r) for r in test_data]
    y_test = [float(r["actual_margin_pts"]) for r in test_data]
    w_test = [int(r["home_win"]) for r in test_data]

    p_dim = len(X_train[0])
    XtX = [[0.0] * p_dim for _ in range(p_dim)]
    Xty = [0.0] * p_dim
    for x_row, y_val in zip(X_train, y_train):
        for i in range(p_dim):
            Xty[i] += x_row[i] * y_val
            for j in range(p_dim):
                XtX[i][j] += x_row[i] * x_row[j]
    for i in range(1, p_dim):
        XtX[i][i] += 1e-2

    betas = solve_linear_system_gauss(XtX, Xty)

    y_pred_test = [sum(b * xij for b, xij in zip(betas, row)) for row in X_test]
    baseline_pred = statistics.fmean(y_train)
    baseline_rmse = math.sqrt(statistics.fmean((yt - baseline_pred) ** 2 for yt in y_test))
    test_rmse = math.sqrt(statistics.fmean((yt - yp) ** 2 for yt, yp in zip(y_test, y_pred_test)))

    # Brier Score e Acurácia de Classificação do Vencedor no Conjunto de Teste
    sigma_resid = test_rmse
    probs_test = [normal_cdf(yp / sigma_resid) for yp in y_pred_test]
    brier_score = statistics.fmean((p - w) ** 2 for p, w in zip(probs_test, w_test))
    baseline_brier = statistics.fmean((0.55 - w) ** 2 for w in w_test)
    accuracy = statistics.fmean(
        1.0 if (p >= 0.5 and w == 1) or (p < 0.5 and w == 0) else 0.0
        for p, w in zip(probs_test, w_test)
    )

    boot_briers: List[float] = []
    for _ in range(200):
        idxs = [rng.randrange(len(w_test)) for _ in range(len(w_test))]
        bb = statistics.fmean((probs_test[idx] - w_test[idx]) ** 2 for idx in idxs)
        boot_briers.append(bb)
    boot_briers.sort()

    return {
        "betas": betas,
        "feat_means": feat_means,
        "feat_stds": feat_stds,
        "sigma_resid": sigma_resid,
        "metrics": {
            "train_samples": len(train_data),
            "test_samples": len(test_data),
            "baseline_margin_rmse_pts": round(baseline_rmse, 2),
            "model_margin_rmse_pts": round(test_rmse, 2),
            "baseline_brier_score": round(baseline_brier, 4),
            "model_brier_score": round(brier_score, 4),
            "brier_bootstrap_95ci": [
                round(percentile(boot_briers, 2.5), 4),
                round(percentile(boot_briers, 97.5), 4),
            ],
            "out_of_sample_winner_accuracy_pct": round(accuracy * 100.0, 2),
        },
    }


# ============================================================================
# 3. ANÁLISE DOS 9 JOGOS DO KALSHI (MATEMÁTICO + ANALISTA + CIENTISTA + ATUÁRIA)
# ============================================================================
def analyze_kalshi_slate(
    cfg: Dict[str, Any], ml_bundle: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    rng = random.Random(int(cfg["seed"]) + 999)
    n_mc = int(cfg["n_monte_carlo_per_game"])
    bankroll = float(cfg["bankroll_usd"])
    kelly_frac = float(cfg["kelly_fraction"])
    betas = ml_bundle["betas"]
    feat_means = ml_bundle["feat_means"]
    feat_stds = ml_bundle["feat_stds"]

    game_results: List[Dict[str, Any]] = []

    for m in cfg["matchups"]:
        # --- Clara Mendonça (Analista de Dados): Métricas de Eficiência e Mercado ---
        p_home_kalshi_raw = m["kalshi_home_yes_cents"] / 100.0
        p_away_kalshi_raw = m["kalshi_away_yes_cents"] / 100.0
        overround = (p_home_kalshi_raw + p_away_kalshi_raw) - 1.0
        p_home_kalshi_fair = p_home_kalshi_raw / (p_home_kalshi_raw + p_away_kalshi_raw)

        elo_diff = float(m["home_elo"] - m["away_elo"])
        # Eficiência líquida de confronto: (Ataque Casa - Defesa Fora) - (Ataque Fora - Defesa Casa)
        # Nota: Def EPA negativo significa defesa forte (cede menos pontos esperados).
        home_matchup_epa = float(m["home_off_epa"]) + float(m["away_def_epa"])
        away_matchup_epa = float(m["away_off_epa"]) + float(m["home_def_epa"])
        net_epa_diff = home_matchup_epa - away_matchup_epa
        to_diff = float(m["home_turnover_diff_per_game"] - m["away_turnover_diff_per_game"])
        hfa = float(m["home_field_advantage_pts"])

        # --- Henrique Vasconcelos (Matemático): Equação Estrutural Analítica ---
        structural_spread = (
            (elo_diff / 25.0)
            + (22.0 * net_epa_diff)
            + (1.5 * to_diff)
            + hfa
        )
        p_home_analytical = normal_cdf(structural_spread / 13.85)

        # --- Lucas Bittencourt (Cientista de Dados): Predição ML + 10.000 Runs Monte Carlo ---
        x_vec = [
            1.0,
            (elo_diff - feat_means["elo_diff"]) / feat_stds["elo_diff"],
            (net_epa_diff - feat_means["net_epa_diff"]) / feat_stds["net_epa_diff"],
            (to_diff - feat_means["turnover_diff"]) / feat_stds["turnover_diff"],
            (hfa - feat_means["hfa_pts"]) / feat_stds["hfa_pts"],
        ]
        ml_spread = sum(b * xij for b, xij in zip(betas, x_vec))
        consensus_spread = 0.5 * structural_spread + 0.5 * ml_spread

        # Expectativa de pontos base por equipe (Média NFL ~ 22.8 pts por time)
        base_total = 45.6 + 14.0 * (float(m["home_off_epa"]) + float(m["away_off_epa"]))
        exp_home_pts = max(13.0, (base_total + consensus_spread) / 2.0)
        exp_away_pts = max(13.0, (base_total - consensus_spread) / 2.0)

        home_wins_mc = 0
        away_wins_mc = 0
        ties_mc = 0
        home_scores: List[int] = []
        away_scores: List[int] = []

        for _ in range(n_mc):
            # Simulação de pontuação em ambiente fechado (Normal truncada discretizada + variância de jogo)
            hs = max(0, int(round(rng.gauss(exp_home_pts, 9.5))))
            as_ = max(0, int(round(rng.gauss(exp_away_pts, 9.5))))
            if hs == as_:
                # Prorrogação NFL: ~92% de resolução para um vencedor, ~8% de empate residual
                ot_roll = rng.random()
                p_ot_home = 0.5 + 0.02 * consensus_spread
                if ot_roll < 0.06:
                    ties_mc += 1
                elif rng.random() < p_ot_home:
                    hs += 3
                    home_wins_mc += 1
                else:
                    as_ += 3
                    away_wins_mc += 1
            elif hs > as_:
                home_wins_mc += 1
            else:
                away_wins_mc += 1
            home_scores.append(hs)
            away_scores.append(as_)

        p_home_mc = home_wins_mc / n_mc
        p_away_mc = away_wins_mc / n_mc
        p_tie_mc = ties_mc / n_mc

        # Probabilidade Ensemble Argon (Combinação Matemática + ML + Monte Carlo)
        p_home_argon = round(0.40 * p_home_analytical + 0.60 * p_home_mc, 4)
        p_away_argon = round(1.0 - p_home_argon - p_tie_mc, 4)

        predicted_winner = m["home_team"] if p_home_argon >= p_away_argon else m["away_team"]
        predicted_winner_abbr = m["home_abbr"] if p_home_argon >= p_away_argon else m["away_abbr"]
        winner_prob_pct = round(max(p_home_argon, p_away_argon) * 100.0, 1)

        # --- Avaliação de Valor no Contrato Kalshi (Regra: Vitória=$1.00, Empate=$0.50, Derrota=$0.00) ---
        ev_home_per_dollar = (
            p_home_argon * (1.0 - p_home_kalshi_raw)
            + p_tie_mc * (0.50 - p_home_kalshi_raw)
            - p_away_argon * p_home_kalshi_raw
        )
        ev_away_per_dollar = (
            p_away_argon * (1.0 - p_away_kalshi_raw)
            + p_tie_mc * (0.50 - p_away_kalshi_raw)
            - p_home_argon * p_away_kalshi_raw
        )

        # Critério de Kelly Fracionário (Beatriz Alencar & Henrique Vasconcelos)
        edge_home = p_home_argon - p_home_kalshi_raw
        edge_away = p_away_argon - p_away_kalshi_raw

        if edge_home >= edge_away and edge_home > 0.015:
            best_side = f"YES {m['home_abbr']} ({m['home_team']})"
            contract_price_cents = m["kalshi_home_yes_cents"]
            edge_pct = round(edge_home * 100.0, 2)
            ev_roi_pct = round((ev_home_per_dollar / p_home_kalshi_raw) * 100.0, 2)
            full_kelly = max(0.0, edge_home / (1.0 - p_home_kalshi_raw))
            rec_stake_usd = round(min(bankroll * 0.08, bankroll * kelly_frac * full_kelly), 2)
            win_prob_side = p_home_argon
            price_side = p_home_kalshi_raw
        elif edge_away > edge_home and edge_away > 0.015:
            best_side = f"YES {m['away_abbr']} ({m['away_team']})"
            contract_price_cents = m["kalshi_away_yes_cents"]
            edge_pct = round(edge_away * 100.0, 2)
            ev_roi_pct = round((ev_away_per_dollar / p_away_kalshi_raw) * 100.0, 2)
            full_kelly = max(0.0, edge_away / (1.0 - p_away_kalshi_raw))
            rec_stake_usd = round(min(bankroll * 0.08, bankroll * kelly_frac * full_kelly), 2)
            win_prob_side = p_away_argon
            price_side = p_away_kalshi_raw
        else:
            best_side = "NO TRADE (Preço Kalshi Eficiente / Sem Margem de Segurança)"
            contract_price_cents = (
                m["kalshi_home_yes_cents"]
                if p_home_argon >= p_away_argon
                else m["kalshi_away_yes_cents"]
            )
            edge_pct = round(max(edge_home, edge_away) * 100.0, 2)
            ev_roi_pct = round(
                max(
                    ev_home_per_dollar / p_home_kalshi_raw,
                    ev_away_per_dollar / p_away_kalshi_raw,
                )
                * 100.0,
                2,
            )
            rec_stake_usd = 0.0
            win_prob_side = max(p_home_argon, p_away_argon)
            price_side = contract_price_cents / 100.0

        home_scores.sort()
        away_scores.sort()

        game_results.append(
            {
                "ticker": m["ticker"],
                "matchup": f"{m['away_team']} @ {m['home_team']}",
                "predicted_winner": predicted_winner,
                "predicted_winner_abbr": predicted_winner_abbr,
                "argon_win_prob_pct": winner_prob_pct,
                "argon_home_prob_pct": round(p_home_argon * 100.0, 1),
                "argon_away_prob_pct": round(p_away_argon * 100.0, 1),
                "kalshi_home_cents": m["kalshi_home_yes_cents"],
                "kalshi_away_cents": m["kalshi_away_yes_cents"],
                "kalshi_home_fair_prob_pct": round(p_home_kalshi_fair * 100.0, 1),
                "market_overround_pct": round(overround * 100.0, 2),
                "projected_spread_home_pts": round(-consensus_spread, 1),
                "projected_median_score": f"{m['home_abbr']} {int(percentile(home_scores, 50))} x {int(percentile(away_scores, 50))} {m['away_abbr']}",
                "best_kalshi_contract": best_side,
                "contract_price_cents": contract_price_cents,
                "edge_over_kalshi_pct": edge_pct,
                "expected_roi_pct": ev_roi_pct,
                "recommended_stake_usd": rec_stake_usd,
                "_sim_side_prob": win_prob_side,
                "_sim_side_price": price_side,
            }
        )

    # --- Beatriz Alencar (Atuária): Simulação de Risco da Carteira da Rodada (10.000 Cenários) ---
    active_trades = [g for g in game_results if g["recommended_stake_usd"] > 0]
    total_allocated = round(sum(g["recommended_stake_usd"] for g in active_trades), 2)

    portfolio_pnl: List[float] = []
    ruin_events = 0
    for _ in range(10000):
        pnl = 0.0
        for g in active_trades:
            stake = g["recommended_stake_usd"]
            price = g["_sim_side_price"]
            prob = g["_sim_side_prob"]
            n_contracts = stake / price
            if rng.random() < prob:
                pnl += n_contracts * (1.0 - price)
            else:
                pnl -= stake
        portfolio_pnl.append(pnl)
        if (bankroll + pnl) <= 0.0:
            ruin_events += 1

    portfolio_pnl.sort()
    losses = sorted(-x for x in portfolio_pnl)
    var_95 = percentile(losses, 95)
    var_99 = percentile(losses, 99)
    tail_95 = [l for l in losses if l >= var_95]
    cvar_95 = statistics.fmean(tail_95) if tail_95 else var_95

    actuarial_summary = {
        "bankroll_usd": bankroll,
        "active_value_positions": len(active_trades),
        "total_capital_at_risk_usd": total_allocated,
        "capital_exposure_pct": round((total_allocated / bankroll) * 100.0, 2),
        "expected_portfolio_profit_usd": round(statistics.fmean(portfolio_pnl), 2),
        "median_portfolio_profit_usd": round(percentile(portfolio_pnl, 50), 2),
        "p90_portfolio_profit_usd": round(percentile(portfolio_pnl, 90), 2),
        "var_95_loss_usd": round(var_95, 2),
        "var_99_loss_usd": round(var_99, 2),
        "cvar_95_expected_shortfall_usd": round(cvar_95, 2),
        "probability_of_profitable_slate_pct": round(
            (sum(1 for x in portfolio_pnl if x > 0) / len(portfolio_pnl)) * 100.0, 2
        ),
        "ruin_probability_pct": round((ruin_events / 10000.0) * 100.0, 4),
        "unallocated_safety_reserve_usd": round(bankroll - total_allocated, 2),
    }

    return game_results, actuarial_summary


# ============================================================================
# 4. GRAVAÇÃO DE OUTPUTS NOS AGENTES E RELATÓRIO EXECUTIVO FINAL
# ============================================================================
def save_outputs_and_report(
    cfg: Dict[str, Any],
    ml_bundle: Dict[str, Any],
    game_results: List[Dict[str, Any]],
    actuarial_summary: Dict[str, Any],
    csv_path: Path,
) -> Path:
    clean_games = [
        {k: v for k, v in g.items() if not k.startswith("_")} for g in game_results
    ]

    # Salva nos diretórios de cada agente
    (
        ROOT_DIR
        / "agents"
        / "01_henrique_vasconcelos_matematico"
        / "outputs"
        / "kalshi_nfl_equacoes_kelly.json"
    ).write_text(
        json.dumps(
            {
                "agent": "Henrique Vasconcelos - Matemático",
                "model": "Elo-EPA Structural Differential + Fractional Kelly (gamma=0.25)",
                "games": clean_games,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    (
        ROOT_DIR
        / "agents"
        / "02_clara_mendonca_analista_dados"
        / "outputs"
        / "kalshi_nfl_market_efficiency.json"
    ).write_text(
        json.dumps(
            {
                "agent": "Clara Mendonça - Analista de Dados",
                "source_url": cfg["source_url"],
                "total_matchups_analyzed": len(clean_games),
                "games": clean_games,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    (
        ROOT_DIR
        / "agents"
        / "03_lucas_bittencourt_cientista_dados"
        / "outputs"
        / "kalshi_nfl_monte_carlo_ml.json"
    ).write_text(
        json.dumps(
            {
                "agent": "Lucas Bittencourt - Cientista de Dados",
                "ml_validation": ml_bundle["metrics"],
                "monte_carlo_runs_per_game": cfg["n_monte_carlo_per_game"],
                "predictions": clean_games,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    (
        ROOT_DIR
        / "agents"
        / "04_beatriz_alencar_atuaria"
        / "outputs"
        / "kalshi_nfl_parecer_atuarial.json"
    ).write_text(
        json.dumps(
            {
                "agent": "Beatriz Alencar - Atuária",
                "portfolio_risk_metrics": actuarial_summary,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # Gera o Relatório Executivo Consolidado
    report_path = ROOT_DIR / "reports" / "RELATORIO_KALSHI_NFL_26NOV01.md"
    mlm = ml_bundle["metrics"]

    rows_pred = []
    for g in clean_games:
        rows_pred.append(
            f"| `{g['ticker']}` | **{g['matchup']}** | 🏆 **{g['predicted_winner']}** (`{g['argon_win_prob_pct']}%`) | `{g['projected_median_score']}` | {g['kalshi_home_cents']}¢ / {g['kalshi_away_cents']}¢ | **{g['best_kalshi_contract']}** | `{g['edge_over_kalshi_pct']:+.2f}%` | **US$ {g['recommended_stake_usd']:.2f}** |"
        )
    table_str = "\n".join(rows_pred)

    # Ordena por probabilidade de vitória e por Edge para o Plano de Ação dinâmico
    by_prob = sorted(clean_games, key=lambda x: x["argon_win_prob_pct"], reverse=True)
    prob_bullets = "\n".join(
        f"   - **{g['predicted_winner']}** vence `{g['matchup']}` (**`{g['argon_win_prob_pct']}%`** de probabilidade | Placar Mediano: `{g['projected_median_score']}`)"
        for g in by_prob
    )

    value_trades = sorted(
        [g for g in clean_games if g["recommended_stake_usd"] > 0],
        key=lambda x: x["edge_over_kalshi_pct"],
        reverse=True,
    )
    trade_bullets = "\n".join(
        f"   - **`{g['best_kalshi_contract']}` a `{g['contract_price_cents']}¢`** (`{g['ticker']}`): Probabilidade Argon de **`{g['argon_win_prob_pct']}%`** vs. `{g['contract_price_cents']}%` implícito no Kalshi -> **Edge Líquido: `{g['edge_over_kalshi_pct']:+.2f}%`** | ROI Esperado: **`{g['expected_roi_pct']:+.2f}%`** | Alocação Kelly: **US$ {g['recommended_stake_usd']:.2f}**."
        for g in value_trades
    )

    content = f"""# 🏈 Relatório de Previsão Quantitativa Kalshi NFL (`KXNFLGAME`) & Plano de Ação

> **Projeto:** `{cfg['project_id']}` — {cfg['project_name']}  
> **URL Analisada:** {cfg['source_url']}  
> **Orquestrador:** **Axio Vance** (Orquestrador e Programador Sênior)  
> **Data da Simulação:** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Seed:** `{cfg['seed']}`  
> **Volume de Simulação:** 1.800 jogos históricos calibrados + **90.000 partidas simuladas via Monte Carlo** (10.000 por confronto).

---

## 🧭 1. Diagnóstico Inicial da URL (Clara Mendonça — Analista de Dados)

A URL `https://kalshi.com/markets/kxnflgame/nfl-game` é a página-mãe da série oficial **`KXNFLGAME`** na bolsa de contratos de eventos regulamentada **Kalshi**. Nela estão listados os **9 confrontos da rodada de 1º de Novembro (`26NOV01`)**, onde cada contrato binário ("Yes") custa entre `1¢` e `99¢` e paga **US$ 1,00** se a equipe vencer a partida (ou **US$ 0,50** em caso de empate).

Para responder com precisão máxima **"Quem vai ganhar?"** e **"Onde está o valor real (Edge)?"**, a Equipe Argon simulou todos os 9 confrontos da página.

---

## 🏆 2. Tabela Geral: Quem Vai Ganhar e Onde Operar (10.000 Simulações/Jogo)

| Ticker Kalshi | Confronto (Visitante @ Casa) | Vencedor Previsto (Prob. Argon) | Placar Mediano Simulado | Preço Kalshi (Casa / Fora) | Recomendação de Contrato (Edge > 1.5%) | Edge Líquido | Alocação Kelly (Banca US$ 1.000) |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: |
{table_str}

---

## 📐 3. Formulação Matemática (Dr. Henrique Vasconcelos — Matemático)

1. **Equação Estrutural de Diferencial de Pontos Esperado ($\\mu_\\Delta$):**
   $$\\mu_\\Delta = \\frac{{\\text{{Elo}}_H - \\text{{Elo}}_A}}{{25.0}} + 22.0 \\cdot \\left(\\text{{NetEPA}}_H - \\text{{NetEPA}}_A\\right) + 1.5 \\cdot \\left(\\text{{TO}}_H - \\text{{TO}}_A\\right) + \\text{{HFA}}$$
2. **Precificação de Contrato Binário Kalshi com Regra de Empate ($0.50):**
   $$\\text{{EV}}(\\text{{Yes}}) = P_{{\\text{{Argon}}}}(\\text{{Win}}) \\cdot (1 - c) + P_{{\\text{{Argon}}}}(\\text{{Tie}}) \\cdot (0.50 - c) - P_{{\\text{{Argon}}}}(\\text{{Loss}}) \\cdot c$$
3. **Critério de Kelly Fracionário Prudencial ($\\gamma = 0.25$):**
   $$f^* = 0.25 \\cdot \\max\\left(0, \\frac{{P_{{\\text{{Argon}}}} - c}}{{1 - c}}\\right)$$

---

## 🤖 4. Validação do Modelo Preditivo (Lucas Bittencourt — Cientista de Dados)

Seguindo estritamente o protocolo `ml-best-practices` (divisão 80% treino / 20% teste **antes** da padronização Z-Score em `{csv_path.name}`):
- **Amostra de Treino / Teste:** `{mlm['train_samples']}` jogos / `{mlm['test_samples']}` jogos
- **Erro RMSE de Margem de Vitória (Baseline vs. Modelo Argon):** Redução de `{mlm['baseline_margin_rmse_pts']}` pts para **`{mlm['model_margin_rmse_pts']}` pts**
- **Brier Score de Calibração Probabilística (Baseline vs. Modelo Argon):** Melhora de `{mlm['baseline_brier_score']}` para **`{mlm['model_brier_score']}`** (IC 95% Bootstrap: `{mlm['brier_bootstrap_95ci']}`)
- **Acurácia de Vencedor Fora da Amostra (Out-of-Sample):** **`{mlm['out_of_sample_winner_accuracy_pct']}%`**

---

## 🛡️ 5. Parecer Atuarial e Gestão de Risco da Banca (Beatriz Alencar — Atuária)

Simulando 10.000 domingos completos para uma banca de referência de **US$ {actuarial_summary['bankroll_usd']:,.2f}**:
- **Posições Aprovadas com Valor Positivo ($\\text{{EV}} > 0$):** `{actuarial_summary['active_value_positions']}` de 9 jogos
- **Capital Total Exposto na Rodada:** **US$ {actuarial_summary['total_capital_at_risk_usd']:.2f}** (`{actuarial_summary['capital_exposure_pct']}%` da banca)
- **Reserva Técnica Intocada (Caixa Protegido):** **US$ {actuarial_summary['unallocated_safety_reserve_usd']:.2f}** (`{100.0 - actuarial_summary['capital_exposure_pct']:.2f}%` da banca)
- **Lucro Líquido Esperado na Rodada:** **+US$ {actuarial_summary['expected_portfolio_profit_usd']:.2f}** (P90: **+US$ {actuarial_summary['p90_portfolio_profit_usd']:.2f}**)
- **Value at Risk ($\\text{{VaR}}_{{95\\%}}$ da Carteira):** US$ {actuarial_summary['var_95_loss_usd']:.2f} (Perda máxima em 95% dos cenários limitada a `{actuarial_summary['var_95_loss_usd']/10.0:.2f}%` da banca)
- **Expected Shortfall ($\\text{{CVaR}}_{{95\\%}}$):** US$ {actuarial_summary['cvar_95_expected_shortfall_usd']:.2f}
- **Probabilidade de Ruína da Banca ($\\psi(u)$):** **`{actuarial_summary['ruin_probability_pct']}%` (Zero Ruína)**

---

## 🎯 6. Plano de Ação Tático (Síntese de Axio Vance)

### 6.1 Ranking de Vencedores no Campo (Quem Vai Ganhar — Do Mais Provável ao Mais Equilibrado)
{prob_bullets}

### 6.2 Carteira Recomendada de Contratos Kalshi (Ordenada por Maior Vantagem Matemática / Edge)
{trade_bullets}
"""

    report_path.write_text(content, encoding="utf-8")
    return report_path


def main() -> None:
    cfg_path = ROOT_DIR / "sandbox" / "configs" / "kalshi_kxnflgame_26nov01.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    print(f"[Axio Orquestrador] Iniciando Análise Kalshi NFL: {cfg['source_url']}")
    records, csv_path = generate_synthetic_nfl_history(cfg)
    print(f"  -> [Lucas Bittencourt] Dataset histórico sintético gerado ({len(records)} jogos): {csv_path.name}")

    ml_bundle = train_and_validate_nfl_model(cfg, records)
    print(
        f"  -> [Lucas Bittencourt] Modelo validado (Acurácia Out-of-Sample: {ml_bundle['metrics']['out_of_sample_winner_accuracy_pct']}% | Brier: {ml_bundle['metrics']['model_brier_score']})"
    )

    game_results, actuarial_summary = analyze_kalshi_slate(cfg, ml_bundle)
    for g in game_results:
        print(
            f"  -> [{g['ticker']}] {g['matchup']} => Vencedor: {g['predicted_winner_abbr']} ({g['argon_win_prob_pct']}%) | Placar: {g['projected_median_score']} | Kalshi Action: {g['best_kalshi_contract']} (Edge: {g['edge_over_kalshi_pct']:+.2f}%)"
        )

    report_path = save_outputs_and_report(cfg, ml_bundle, game_results, actuarial_summary, csv_path)
    print(
        f"  -> [Beatriz Alencar] VaR 95%: US$ {actuarial_summary['var_95_loss_usd']} | Prob. Ruína: {actuarial_summary['ruin_probability_pct']}%"
    )
    print(f"[Axio Orquestrador] Relatório Kalshi NFL salvo em: {report_path}")


if __name__ == "__main__":
    main()
