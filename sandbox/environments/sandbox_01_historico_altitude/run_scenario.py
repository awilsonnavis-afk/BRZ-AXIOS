"""
Script Isolado de Execução de Sandbox (sandbox_01_historico_altitude)
Gerado por: Axio Vance — Orquestrador Equipe Argon
"""
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

def main():
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    rng = random.Random(cfg["seed"])
    n_runs = cfg["n_monte_carlo_runs"]
    p_kc_mean = cfg["p_kc_mean"]
    p_kc_sd = cfg["p_kc_epistemic_sd"]
    exp_kc_pts = cfg["exp_kc_pts"]
    exp_den_pts = cfg["exp_den_pts"]
    score_sd = cfg["score_sd"]
    ask_kc = cfg["entry_ask_kc"]
    ask_den = cfg["entry_ask_den"]

    kc_wins = 0
    one_score_games = 0
    kc_blowouts_7plus = 0
    den_blowouts_7plus = 0
    pnl_kc_100usd = []
    pnl_den_100usd = []

    for _ in range(n_runs):
        # Amostra probabilidade epistêmica e placar do jogo
        ks = max(0, int(round(rng.gauss(exp_kc_pts, score_sd))))
        ds = max(0, int(round(rng.gauss(exp_den_pts, score_sd))))
        if ks == ds:
            if rng.random() < p_kc_mean:
                ks += 3
            else:
                ds += 3
        margin_kc = ks - ds
        if abs(margin_kc) <= 7:
            one_score_games += 1
        if margin_kc >= 8:
            kc_blowouts_7plus += 1
        if margin_kc <= -8:
            den_blowouts_7plus += 1

        if margin_kc > 0:
            kc_wins += 1
            pnl_kc_100usd.append(100.0 * ((1.0 - ask_kc) / ask_kc))
            pnl_den_100usd.append(-100.0)
        else:
            pnl_kc_100usd.append(-100.0)
            pnl_den_100usd.append(100.0 * ((1.0 - ask_den) / ask_den))

    sim_p_kc = kc_wins / n_runs
    # Combina prior analítico do cenário (70%) + realização estocástica de placar (30%)
    final_p_kc = round(0.70 * p_kc_mean + 0.30 * sim_p_kc, 4)
    final_p_den = round(1.0 - final_p_kc, 4)

    ev_kc_pct = round(((final_p_kc * (1.0 - ask_kc) - final_p_den * ask_kc) / ask_kc) * 100.0, 2)
    ev_den_pct = round(((final_p_den * (1.0 - ask_den) - final_p_kc * ask_den) / ask_den) * 100.0, 2)

    out = {
        "sandbox_id": cfg["sandbox_id"],
        "scenario_title": cfg["scenario_title"],
        "hypothesis": cfg["hypothesis"],
        "n_monte_carlo_runs": n_runs,
        "seed": cfg["seed"],
        "prob_kc_win_pct": round(final_p_kc * 100.0, 2),
        "prob_den_win_pct": round(final_p_den * 100.0, 2),
        "epistemic_95ci_kc_pct": [
            round(max(0.05, final_p_kc - 1.96 * p_kc_sd) * 100.0, 2),
            round(min(0.95, final_p_kc + 1.96 * p_kc_sd) * 100.0, 2),
        ],
        "one_score_game_prob_pct": round((one_score_games / n_runs) * 100.0, 2),
        "kc_win_by_8plus_prob_pct": round((kc_blowouts_7plus / n_runs) * 100.0, 2),
        "den_win_by_8plus_prob_pct": round((den_blowouts_7plus / n_runs) * 100.0, 2),
        "entry_ask_kc_cents": round(ask_kc * 100, 1),
        "entry_ask_den_cents": round(ask_den * 100, 1),
        "expected_roi_kc_contract_pct": ev_kc_pct,
        "expected_roi_den_contract_pct": ev_den_pct,
        "recommended_winner": "Kansas City Chiefs" if final_p_kc >= 0.5 else "Denver Broncos",
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Sandbox {cfg['sandbox_id']}] Concluída -> P(KC)={out['prob_kc_win_pct']}% | P(DEN)={out['prob_den_win_pct']}% | ROI(KC)={ev_kc_pct:+.2f}%")

if __name__ == "__main__":
    main()
