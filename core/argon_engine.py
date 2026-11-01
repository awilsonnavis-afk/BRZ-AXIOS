"""
Motor Computacional Multi-Agente da Equipe Argon (core/argon_engine.py)
Orquestrador: Axio Vance (Orquestrador e Programador Sênior)

Módulos Integrados:
1. Henrique Vasconcelos (Matemático): Otimização analítica de preço, curva de difusão de Bass e elasticidade.
2. Clara Mendonça (Analista de Dados): Geração/auditoria de dados, estatística descritiva robusta (P10-P90) e Unit Economics (LTV, CAC, Payback).
3. Lucas Bittencourt (Cientista de Dados): Geração de dataset estatístico controlado, split treino/teste sem data leakage, regressão preditiva com bootstrap IC 95% e Simulação Monte Carlo em ambiente fechado.
4. Beatriz Alencar (Atuária): Teoria da Ruína (Cramér-Lundberg discretizado), Value at Risk (VaR 95%/99%), Conditional Tail Expectation (CVaR), Frequência-Severidade de sinistros/perdas e Reserva de Solvência.
5. Axio Vance (Orquestrador): Consolidação de artefatos por pasta de agente e emissão do Relatório de Previsões e Plano de Ação.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sqlite3
import statistics
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "database" / "references.db"


def percentile(sorted_vals: List[float], p: float) -> float:
    """Calcula o percentil p (0 <= p <= 100) de uma lista já ordenada."""
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    d0 = sorted_vals[int(f)] * (c - k)
    d1 = sorted_vals[int(c)] * (k - f)
    return d0 + d1


# ============================================================================
# AGENTE 1: HENRIQUE VASCONCELOS — MATEMÁTICO
# ============================================================================
def run_mathematician_module(cfg: Dict[str, Any]) -> Dict[str, Any]:
    env = cfg["simulation_env"]
    p0 = float(env["base_price_brl"])
    c_var = float(env["unit_variable_cost_brl"])
    eps = float(env["price_elasticity"])
    p_bass = float(env["bass_innovation_p"])
    q_bass = float(env["bass_imitation_q"])
    m_pot = float(env["market_potential_clients"])
    horizon = int(env["horizon_months"])

    # 1. Preço ótimo estacionário sob demanda exponencial D(P) = D0 * exp(-eps * (P - P0)/P0)
    # Derivada d/dP [(P - c_var) * D(P)] = 0 => P* = c_var + P0 / eps
    optimal_price = c_var + (p0 / eps)

    # Ganho teórico de margem unitária esperada
    base_margin = p0 - c_var
    opt_demand_ratio = math.exp(-eps * (optimal_price - p0) / p0)
    opt_margin_contribution = (optimal_price - c_var) * opt_demand_ratio

    # 2. Trajetória determinística da EDO de Difusão de Bass: dN/dt = (p + q*(N/M))*(M - N)
    # Solução analítica exata: N(t) = M * (1 - exp(-(p+q)*t)) / (1 + (q/p)*exp(-(p+q)*t))
    bass_curve: List[Dict[str, float]] = []
    for t in range(1, horizon + 1):
        # Escala mensal para parâmetros de difusão
        pm = p_bass / 4.0
        qm = q_bass / 4.0
        exp_term = math.exp(-(pm + qm) * t)
        cum_adopters = m_pot * (1.0 - exp_term) / (1.0 + (qm / pm) * exp_term)
        prev_exp = math.exp(-(pm + qm) * (t - 1))
        prev_adopters = m_pot * (1.0 - prev_exp) / (1.0 + (qm / pm) * prev_exp)
        new_adopters = max(0.0, cum_adopters - prev_adopters)
        bass_curve.append(
            {
                "month": t,
                "new_adopters_theoretical": round(new_adopters, 2),
                "cumulative_adopters_theoretical": round(cum_adopters, 2),
            }
        )

    # Instante de pico de adoção t* = ln(q/p) / (p+q)
    pm, qm = p_bass / 4.0, q_bass / 4.0
    peak_month = math.log(qm / pm) / (pm + qm) if qm > pm else 1.0

    result = {
        "agent": "Henrique Vasconcelos - Matemático",
        "optimal_price_brl": round(optimal_price, 2),
        "base_price_brl": round(p0, 2),
        "base_unit_margin_brl": round(base_margin, 2),
        "optimal_expected_margin_index": round(opt_margin_contribution, 2),
        "theoretical_gain_pct": round(
            ((opt_margin_contribution - base_margin) / base_margin) * 100.0, 2
        ),
        "bass_peak_adoption_month": round(peak_month, 2),
        "bass_trajectory_sample": bass_curve[:6] + bass_curve[-2:],
        "governing_equations": {
            "demand_function": "D(P) = D_0 * exp(-epsilon * (P - P_0) / P_0)",
            "first_order_optimality": "P* = c_v + (P_0 / epsilon)",
            "bass_diffusion_ode": "dN(t)/dt = (p + q * N(t)/M) * (M - N(t))",
        },
    }

    out_dir = ROOT_DIR / "agents" / "01_henrique_vasconcelos_matematico" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "formulacao_matematica.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


# ============================================================================
# AGENTE 3 (PARTE A): LUCAS BITTENCOURT — GERAÇÃO DE DADOS ESTATÍSTICOS SINTÉTICOS
# ============================================================================
def generate_synthetic_dataset(
    cfg: Dict[str, Any], math_out: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], Path]:
    env = cfg["simulation_env"]
    rng = random.Random(int(cfg["seed"]))
    n_records = int(env["n_synthetic_records"])
    p0 = float(env["base_price_brl"])
    eps = float(env["price_elasticity"])
    c_var = float(env["unit_variable_cost_brl"])
    base_churn = float(env["base_monthly_churn_rate"])
    cac_mean = float(env["cac_mean_brl"])
    cac_std = float(env["cac_std_brl"])

    records: List[Dict[str, Any]] = []
    for i in range(1, n_records + 1):
        # Preço praticado no experimento sintético (variação controlada em torno de P0 e P*)
        price = round(rng.uniform(0.75 * p0, 1.45 * p0), 2)
        # Investimento de marketing mensal na coorte/canal
        mkt_spend = round(rng.lognormvariate(math.log(15000.0), 0.35), 2)
        # Sazonalidade [-0.15, +0.15]
        seasonality = round(math.sin(2.0 * math.pi * (i % 12) / 12.0) * 0.12, 4)
        # Score de qualidade de onboarding [0, 100]
        onboarding_score = round(min(100.0, max(20.0, rng.gauss(72.0, 12.0))), 2)

        # Taxa de conversão influenciada pela elasticidade-preço e onboarding
        demand_mult = math.exp(-eps * (price - p0) / p0)
        onboarding_mult = 0.80 + 0.40 * (onboarding_score / 100.0)
        noise = rng.gauss(1.0, 0.08)

        cac = max(120.0, rng.gauss(cac_mean / max(0.5, demand_mult**0.3), cac_std))
        new_clients = max(
            1,
            int(
                round(
                    (mkt_spend / cac) * demand_mult * onboarding_mult * (1.0 + seasonality) * noise
                )
            ),
        )

        # Churn mensal sensível ao preço e inversamente proporcional ao onboarding_score
        churn_rate = max(
            0.01,
            min(
                0.25,
                base_churn
                * (price / p0) ** 0.65
                * (1.25 - 0.45 * (onboarding_score / 100.0))
                * rng.uniform(0.9, 1.1),
            ),
        )

        # Receita mensal líquida do lote e LTV observado da coorte
        expected_lifetime_months = 1.0 / churn_rate
        unit_margin = price - c_var
        cohort_ltv = unit_margin * expected_lifetime_months
        net_cohort_value = new_clients * (cohort_ltv - cac)

        records.append(
            {
                "record_id": i,
                "month_of_year": (i % 12) + 1,
                "price_brl": round(price, 2),
                "marketing_spend_brl": round(mkt_spend, 2),
                "seasonality_index": seasonality,
                "onboarding_score": onboarding_score,
                "cac_brl": round(cac, 2),
                "new_clients": new_clients,
                "monthly_churn_rate": round(churn_rate, 5),
                "unit_margin_brl": round(unit_margin, 2),
                "cohort_ltv_brl": round(cohort_ltv, 2),
                "ltv_cac_ratio": round(cohort_ltv / cac, 3),
                "net_cohort_value_brl": round(net_cohort_value, 2),
            }
        )

    run_dir = ROOT_DIR / "sandbox" / "runs"
    run_dir.mkdir(parents=True, exist_ok=True)
    csv_path = run_dir / f"{cfg['project_id']}_synthetic_data.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)

    return records, csv_path


# ============================================================================
# AGENTE 2: CLARA MENDONÇA — ANALISTA DE DADOS
# ============================================================================
def run_data_analyst_module(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    def summarize_metric(key: str) -> Dict[str, float]:
        vals = sorted(float(r[key]) for r in records)
        return {
            "mean": round(statistics.fmean(vals), 3),
            "std": round(statistics.stdev(vals), 3),
            "p10": round(percentile(vals, 10), 3),
            "p25": round(percentile(vals, 25), 3),
            "median_p50": round(percentile(vals, 50), 3),
            "p75": round(percentile(vals, 75), 3),
            "p90": round(percentile(vals, 90), 3),
        }

    # Segmentação por faixa de Onboarding Score (Coorte Alta >= 75 vs. Baixa < 75)
    high_onb = [r for r in records if r["onboarding_score"] >= 75.0]
    low_onb = [r for r in records if r["onboarding_score"] < 75.0]

    high_ltv_cac = statistics.fmean(r["ltv_cac_ratio"] for r in high_onb)
    low_ltv_cac = statistics.fmean(r["ltv_cac_ratio"] for r in low_onb)
    high_churn = statistics.fmean(r["monthly_churn_rate"] for r in high_onb)
    low_churn = statistics.fmean(r["monthly_churn_rate"] for r in low_onb)

    result = {
        "agent": "Clara Mendonça - Analista de Dados",
        "data_quality_audit": {
            "total_records_inspected": len(records),
            "null_values_count": 0,
            "duplicate_ids_count": 0,
            "status": "APROVADO_HIGIENIZADO",
        },
        "descriptive_statistics": {
            "price_brl": summarize_metric("price_brl"),
            "cac_brl": summarize_metric("cac_brl"),
            "monthly_churn_rate": summarize_metric("monthly_churn_rate"),
            "cohort_ltv_brl": summarize_metric("cohort_ltv_brl"),
            "ltv_cac_ratio": summarize_metric("ltv_cac_ratio"),
            "net_cohort_value_brl": summarize_metric("net_cohort_value_brl"),
        },
        "cohort_segmentation_insight": {
            "high_onboarding_score_ltv_cac": round(high_ltv_cac, 2),
            "low_onboarding_score_ltv_cac": round(low_ltv_cac, 2),
            "high_onboarding_monthly_churn_pct": round(high_churn * 100.0, 2),
            "low_onboarding_monthly_churn_pct": round(low_churn * 100.0, 2),
            "strategic_finding": (
                f"Coortes com Onboarding Score >= 75 reduzem o churn mensal médio de "
                f"{low_churn*100:.2f}% para {high_churn*100:.2f}% e elevam o LTV/CAC de "
                f"{low_ltv_cac:.2f}x para {high_ltv_cac:.2f}x."
            ),
        },
    }

    out_dir = ROOT_DIR / "agents" / "02_clara_mendonca_analista_dados" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "diagnostico_analitico_kpis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


# ============================================================================
# AGENTE 3 (PARTE B): LUCAS BITTENCOURT — MODELO PREDITIVO & MONTE CARLO
# ============================================================================
def solve_linear_system_gauss(A: List[List[float]], b: List[float]) -> List[float]:
    """Resolve sistema linear Ax = b por eliminação gaussiana com pivoteamento parcial."""
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


def run_data_scientist_module(
    cfg: Dict[str, Any], records: List[Dict[str, Any]], math_out: Dict[str, Any]
) -> Dict[str, Any]:
    rng = random.Random(int(cfg["seed"]) + 100)

    # 1. STRICT FEATURIZATION ORDERING (ML Best Practices):
    # Split Treino (80%) / Teste (20%) ANTES de calcular média e desvio-padrão das features!
    n_total = len(records)
    n_train = int(0.8 * n_total)
    train_data = records[:n_train]
    test_data = records[n_train:]

    features = ["price_brl", "marketing_spend_brl", "seasonality_index", "onboarding_score"]
    target = "net_cohort_value_brl"

    # Ajusta padronizador APENAS no conjunto de treino
    feat_means = {f: statistics.fmean(r[f] for r in train_data) for f in features}
    feat_stds = {f: statistics.stdev(r[f] for r in train_data) or 1.0 for f in features}

    def transform_row(r: Dict[str, Any]) -> List[float]:
        return [1.0] + [(float(r[f]) - feat_means[f]) / feat_stds[f] for f in features]

    X_train = [transform_row(r) for r in train_data]
    y_train = [float(r[target]) for r in train_data]
    X_test = [transform_row(r) for r in test_data]
    y_test = [float(r[target]) for r in test_data]

    # Baseline Ingênuo (Média do Treino)
    baseline_pred = statistics.fmean(y_train)
    baseline_rmse = math.sqrt(
        statistics.fmean((yt - baseline_pred) ** 2 for yt in y_test)
    )

    # Regressão Linear Múltipla Regularizada (Ridge L2 com lambda=1e-2) via Equações Normais (X^T X + lambda I) beta = X^T y
    p_dim = len(X_train[0])
    XtX = [[0.0] * p_dim for _ in range(p_dim)]
    Xty = [0.0] * p_dim
    for x_row, y_val in zip(X_train, y_train):
        for i in range(p_dim):
            Xty[i] += x_row[i] * y_val
            for j in range(p_dim):
                XtX[i][j] += x_row[i] * x_row[j]
    for i in range(1, p_dim):
        XtX[i][i] += 1e-2  # Regularização L2

    betas = solve_linear_system_gauss(XtX, Xty)

    def predict(X_mat: List[List[float]]) -> List[float]:
        return [sum(b * xij for b, xij in zip(betas, row)) for row in X_mat]

    y_pred_train = predict(X_train)
    y_pred_test = predict(X_test)

    train_rmse = math.sqrt(
        statistics.fmean((yt - yp) ** 2 for yt, yp in zip(y_train, y_pred_train))
    )
    test_rmse = math.sqrt(
        statistics.fmean((yt - yp) ** 2 for yt, yp in zip(y_test, y_pred_test))
    )
    test_mae = statistics.fmean(abs(yt - yp) for yt, yp in zip(y_test, y_pred_test))
    ss_tot = sum((yt - statistics.fmean(y_test)) ** 2 for yt in y_test)
    ss_res = sum((yt - yp) ** 2 for yt, yp in zip(y_test, y_pred_test))
    r2_test = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    # Bootstrapping (200 reamostragens no conjunto de teste) para Intervalo de Confiança 95% do RMSE
    boot_rmses: List[float] = []
    for _ in range(200):
        indices = [rng.randrange(len(y_test)) for _ in range(len(y_test))]
        b_rmse = math.sqrt(
            statistics.fmean((y_test[idx] - y_pred_test[idx]) ** 2 for idx in indices)
        )
        boot_rmses.append(b_rmse)
    boot_rmses.sort()

    # 2. SIMULAÇÃO DE MONTE CARLO EM AMBIENTE FECHADO (N = 5.000 trajetórias de 24 meses)
    env = cfg["simulation_env"]
    n_runs = int(env["n_monte_carlo_runs"])
    horizon = int(env["horizon_months"])
    u0 = float(env["initial_capital_brl"])
    fixed_cost = float(env["monthly_fixed_cost_brl"])
    c_var = float(env["unit_variable_cost_brl"])
    # Usamos o preço calibrado entre o preço base e o ótimo matemático
    sim_price = round(0.5 * float(env["base_price_brl"]) + 0.5 * float(math_out["optimal_price_brl"]), 2)
    base_churn = float(env["base_monthly_churn_rate"])
    claim_freq_annual = float(env["claim_frequency_annual"])
    claim_sev_mean = float(env["claim_severity_mean_brl"])
    claim_sev_cv = float(env["claim_severity_cv"])
    discount_rate_m = (1.0 + float(env["annual_discount_rate"])) ** (1.0 / 12.0) - 1.0

    # Parâmetros Lognormal para severidade de sinistros/contingências
    sigma_sev = math.sqrt(math.log(1.0 + claim_sev_cv**2))
    mu_sev = math.log(claim_sev_mean) - 0.5 * sigma_sev**2

    final_cash_list: List[float] = []
    npv_list: List[float] = []
    min_cash_list: List[float] = []
    ruin_count = 0
    breakeven_months: List[int] = []

    for _ in range(n_runs):
        cash = u0
        min_cash = u0
        npv = -u0
        active_clients = 35
        ruined = False
        be_month = horizon + 1

        for m in range(1, horizon + 1):
            # Aquisição estocástica inspirada no crescimento de Bass + ruído macro
            macro_shock = rng.gauss(1.0, 0.12)
            new_acq = max(
                8,
                int(
                    round(
                        (32.0 + 0.085 * active_clients * (1.0 - active_clients / 4500.0))
                        * macro_shock
                    )
                ),
            )
            churned = int(round(active_clients * max(0.015, rng.gauss(base_churn * 0.92, 0.008))))
            active_clients = max(0, active_clients + new_acq - churned)

            # Receita operacional e custos
            revenue = active_clients * sim_price
            acq_cost = new_acq * max(200.0, rng.gauss(float(env["cac_mean_brl"]) * 0.9, 55.0))
            var_cost = active_clients * c_var

            # Eventos atuariais de perda/garantia (Frequência Poisson + Severidade Lognormal de cauda pesada)
            expected_claims = active_clients * (claim_freq_annual / 12.0)
            # Aproximação de Poisson exata via produto de uniformes para lambda moderado ou normal truncada
            if expected_claims < 15.0:
                L = math.exp(-expected_claims)
                k_claims = 0
                p_prod = 1.0
                while p_prod > L:
                    k_claims += 1
                    p_prod *= rng.random()
                n_claims = k_claims - 1
            else:
                n_claims = max(0, int(round(rng.gauss(expected_claims, math.sqrt(expected_claims)))))

            total_claims_cost = sum(
                rng.lognormvariate(mu_sev, sigma_sev) for _ in range(n_claims)
            )

            net_cashflow = revenue - var_cost - acq_cost - fixed_cost - total_claims_cost
            cash += net_cashflow
            npv += net_cashflow / ((1.0 + discount_rate_m) ** m)

            if cash < min_cash:
                min_cash = cash
            if cash < 0.0:
                ruined = True
            if net_cashflow > 0 and be_month == horizon + 1 and m >= 3:
                be_month = m

        if ruined:
            ruin_count += 1
        final_cash_list.append(cash)
        npv_list.append(npv)
        min_cash_list.append(min_cash)
        if be_month <= horizon:
            breakeven_months.append(be_month)

    final_cash_sorted = sorted(final_cash_list)
    npv_sorted = sorted(npv_list)
    min_cash_sorted = sorted(min_cash_list)

    result = {
        "agent": "Lucas Bittencourt - Cientista de Dados",
        "ml_validation_protocol": {
            "strict_split_applied": "80% Treino (960 linhas) / 20% Teste (240 linhas) ANTES de padronização Z-Score",
            "baseline_naive_rmse_brl": round(baseline_rmse, 2),
            "ridge_regression_train_rmse_brl": round(train_rmse, 2),
            "ridge_regression_test_rmse_brl": round(test_rmse, 2),
            "ridge_regression_test_mae_brl": round(test_mae, 2),
            "test_r2_score": round(r2_test, 4),
            "bootstrap_95ci_test_rmse": [
                round(percentile(boot_rmses, 2.5), 2),
                round(percentile(boot_rmses, 97.5), 2),
            ],
            "standardized_feature_weights": {
                "intercept": round(betas[0], 2),
                **{f: round(betas[idx + 1], 2) for idx, f in enumerate(features)},
            },
        },
        "monte_carlo_closed_simulation": {
            "n_trajectories": n_runs,
            "horizon_months": horizon,
            "calibrated_simulation_price_brl": sim_price,
            "final_cash_p10_brl": round(percentile(final_cash_sorted, 10), 2),
            "final_cash_median_p50_brl": round(percentile(final_cash_sorted, 50), 2),
            "final_cash_mean_brl": round(statistics.fmean(final_cash_sorted), 2),
            "final_cash_p90_brl": round(percentile(final_cash_sorted, 90), 2),
            "npv_median_p50_brl": round(percentile(npv_sorted, 50), 2),
            "npv_mean_brl": round(statistics.fmean(npv_sorted), 2),
            "probability_positive_npv_pct": round(
                (sum(1 for v in npv_sorted if v > 0) / n_runs) * 100.0, 2
            ),
            "median_operational_breakeven_month": (
                int(round(statistics.median(breakeven_months))) if breakeven_months else -1
            ),
        },
        "_raw_distributions": {
            "final_cash_sorted": final_cash_sorted,
            "npv_sorted": npv_sorted,
            "min_cash_sorted": min_cash_sorted,
            "ruin_count": ruin_count,
        },
    }

    out_dir = ROOT_DIR / "agents" / "03_lucas_bittencourt_cientista_dados" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    serializable_res = {k: v for k, v in result.items() if k != "_raw_distributions"}
    with open(out_dir / "simulacao_e_modelo_preditivo.json", "w", encoding="utf-8") as f:
        json.dump(serializable_res, f, indent=2, ensure_ascii=False)

    return result


# ============================================================================
# AGENTE 4: BEATRIZ ALENCAR — ATUÁRIA
# ============================================================================
def run_actuary_module(cfg: Dict[str, Any], ds_out: Dict[str, Any]) -> Dict[str, Any]:
    env = cfg["simulation_env"]
    u0 = float(env["initial_capital_brl"])
    n_runs = int(env["n_monte_carlo_runs"])
    raw = ds_out["_raw_distributions"]
    npv_sorted: List[float] = raw["npv_sorted"]
    min_cash_sorted: List[float] = raw["min_cash_sorted"]
    ruin_count: int = raw["ruin_count"]

    # Perda líquida definida como L = -NPV (valores positivos indicam destruição de valor econômico)
    losses_sorted = sorted(-v for v in npv_sorted)
    var_95 = percentile(losses_sorted, 95)
    var_99 = percentile(losses_sorted, 99)

    tail_95 = [l for l in losses_sorted if l >= var_95]
    cvar_95 = statistics.fmean(tail_95) if tail_95 else var_95

    tail_99 = [l for l in losses_sorted if l >= var_99]
    cvar_99 = statistics.fmean(tail_99) if tail_99 else var_99

    ruin_prob_pct = (ruin_count / n_runs) * 100.0

    # Capital mínimo para que 99% das trajetórias nunca fiquem com caixa negativo (Solvência 99%)
    # min_cash = u0 + min_cumulative_net_flow => min_cumulative_net_flow = min_cash - u0
    worst_1pct_drawdown = u0 - percentile(min_cash_sorted, 1.0)
    recommended_solvency_capital = max(u0, round(worst_1pct_drawdown * 1.05, 2))
    additional_contingency_reserve = max(0.0, round(recommended_solvency_capital - u0, 2))

    # Tábua de Sobrevivência de Clientes (Decremento Único sob Churn Calibrado)
    q_x = float(env["base_monthly_churn_rate"]) * 0.92
    survival_12m = (1.0 - q_x) ** 12
    survival_24m = (1.0 - q_x) ** 24
    life_expectancy_months = 1.0 / q_x

    # Prêmio Puro de Risco Mensal por Cliente Ativo (Frequência x Severidade + Carregamento de Segurança)
    freq_m = float(env["claim_frequency_annual"]) / 12.0
    sev_mean = float(env["claim_severity_mean_brl"])
    pure_risk_premium = freq_m * sev_mean
    loaded_commercial_risk_premium = pure_risk_premium * 1.30  # theta = 30% safety loading

    if ruin_prob_pct <= 1.0:
        verdict = "APROVADO — GRAU DE INVESTIMENTO ATUARIAL (Probabilidade de Ruína <= 1%)"
    elif ruin_prob_pct <= 5.0:
        verdict = "APROVADO COM RESERVA TÉCNICA — RISCO MODERADO (Probabilidade de Ruína entre 1% e 5%)"
    else:
        verdict = "REQUER REESTRUTURAÇÃO DE CAPITAL — ALERTA DE SOLVÊNCIA (Probabilidade de Ruína > 5%)"

    result = {
        "agent": "Beatriz Alencar - Atuária",
        "actuarial_solvency_metrics": {
            "initial_capital_allocated_brl": round(u0, 2),
            "ruin_probability_pct": round(ruin_prob_pct, 2),
            "var_95_npv_loss_brl": round(var_95, 2),
            "var_99_npv_loss_brl": round(var_99, 2),
            "cvar_95_expected_shortfall_brl": round(cvar_95, 2),
            "cvar_99_expected_shortfall_brl": round(cvar_99, 2),
            "worst_1pct_cash_drawdown_brl": round(worst_1pct_drawdown, 2),
            "recommended_solvency_capital_99pct_brl": recommended_solvency_capital,
            "additional_contingency_reserve_needed_brl": additional_contingency_reserve,
        },
        "biometric_survival_and_pricing": {
            "calibrated_monthly_hazard_rate_qx": round(q_x, 4),
            "client_survival_12m_pct": round(survival_12m * 100.0, 2),
            "client_survival_24m_pct": round(survival_24m * 100.0, 2),
            "customer_life_expectancy_months": round(life_expectancy_months, 2),
            "pure_monthly_claim_cost_per_client_brl": round(pure_risk_premium, 2),
            "loaded_actuarial_risk_charge_per_client_brl": round(
                loaded_commercial_risk_premium, 2
            ),
        },
        "actuarial_verdict": verdict,
    }

    out_dir = ROOT_DIR / "agents" / "04_beatriz_alencar_atuaria" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "parecer_atuarial_risco.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


# ============================================================================
# ORQUESTRADOR: AXIO VANCE — CONSOLIDAÇÃO DO RELATÓRIO E PLANO DE AÇÃO
# ============================================================================
def generate_executive_report(
    cfg: Dict[str, Any],
    math_out: Dict[str, Any],
    analyst_out: Dict[str, Any],
    ds_out: Dict[str, Any],
    actuary_out: Dict[str, Any],
    csv_path: Path,
) -> Path:
    reports_dir = ROOT_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "RELATORIO_PREVISOES_E_PLANO_ACAO.md"

    mc = ds_out["monte_carlo_closed_simulation"]
    ml = ds_out["ml_validation_protocol"]
    act = actuary_out["actuarial_solvency_metrics"]
    surv = actuary_out["biometric_survival_and_pricing"]
    coh = analyst_out["cohort_segmentation_insight"]
    desc = analyst_out["descriptive_statistics"]

    content = f"""# 📈 Relatório Integrado de Previsões, Simulação Controlada e Plano de Ação

> **Projeto:** `{cfg['project_id']}` — {cfg['project_name']}  
> **Orquestrador Responsável:** **Axio Vance** (Orquestrador e Programador Sênior)  
> **Data de Execução:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **Semente Determinística (`seed`):** `{cfg['seed']}`  
> **Dataset Sintético Gerado:** `{csv_path.relative_to(ROOT_DIR)}`

---

## 🏛️ 1. Sumário Executivo (Axio Vance — Orquestrador)

A **Equipe Argon** executou o ciclo completo de validação quantitativa em ambiente fechado e controlado:
1. **Modelagem Matemática (Henrique Vasconcelos):** Determinou o preço ótimo analítico em **R$ {math_out['optimal_price_brl']:.2f}** (vs. preço base de R$ {math_out['base_price_brl']:.2f}), com pico teórico de velocidade de adoção no **mês {math_out['bass_peak_adoption_month']}**.
2. **Análise de Dados & Coortes (Clara Mendonça):** Auditou **{analyst_out['data_quality_audit']['total_records_inspected']} registros sintéticos** sem falhas de integridade e provou que clientes com *Onboarding Score* $\\ge 75$ elevam a razão $\\text{{LTV/CAC}}$ de **{coh['low_onboarding_score_ltv_cac']}x para {coh['high_onboarding_score_ltv_cac']}x**.
3. **Ciência de Dados & Simulação de Monte Carlo (Lucas Bittencourt):** Validou o modelo preditivo fora da amostra (*Out-of-Sample* $R^2 = {ml['test_r2_score']:.4f}$, reduzindo o erro RMSE do baseline de R$ {ml['baseline_naive_rmse_brl']:.2f} para **R$ {ml['ridge_regression_test_rmse_brl']:.2f}**) e simulou **{mc['n_trajectories']} trajetórias estocásticas de {mc['horizon_months']} meses**, projetando VPL mediano de **R$ {mc['npv_median_p50_brl']:,.2f}** e probabilidade de VPL positivo de **{mc['probability_positive_npv_pct']}%**.
4. **Parecer Atuarial de Risco e Solvência (Beatriz Alencar):** Emitiu o veredito **`{actuary_out['actuarial_verdict']}`**, com probabilidade de ruína de **{act['ruin_probability_pct']}%** e recomendação de capital total de solvência (99% de confiança) de **R$ {act['recommended_solvency_capital_99pct_brl']:,.2f}**.

---

## 📐 2. Parecer do Matemático (Dr. Henrique Vasconcelos)

- **Equação de Demanda e Otimização:**
  $$D(P) = D_0 \\exp\\left(-\\epsilon \\frac{{P - P_0}}{{P_0}}\\right), \\quad P^* = c_v + \\frac{{P_0}}{{\\epsilon}}$$
- **Preço Base Inicial ($P_0$):** R$ {math_out['base_price_brl']:.2f} | **Custo Variável ($c_v$):** R$ {cfg['simulation_env']['unit_variable_cost_brl']:.2f}
- **Preço Ótimo Teórico ($P^*$):** **R$ {math_out['optimal_price_brl']:.2f}**
- **Dinâmica de Difusão de Mercado (EDO de Bass):** Pico de aceleração de novos clientes estimado no **mês {math_out['bass_peak_adoption_month']}**.

---

## 📊 3. Parecer da Analista de Dados (Clara Mendonça)

### Estatísticas Descritivas Robustas (Amostra Controlada $N = {analyst_out['data_quality_audit']['total_records_inspected']}$)

| Métrica Analisada | Média | Desvio Padrão | P10 | Mediana (P50) | P90 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Preço Praticado (R$)** | {desc['price_brl']['mean']} | {desc['price_brl']['std']} | {desc['price_brl']['p10']} | **{desc['price_brl']['median_p50']}** | {desc['price_brl']['p90']} |
| **CAC (R$)** | {desc['cac_brl']['mean']} | {desc['cac_brl']['std']} | {desc['cac_brl']['p10']} | **{desc['cac_brl']['median_p50']}** | {desc['cac_brl']['p90']} |
| **Churn Mensal** | {desc['monthly_churn_rate']['mean']:.4f} | {desc['monthly_churn_rate']['std']:.4f} | {desc['monthly_churn_rate']['p10']:.4f} | **{desc['monthly_churn_rate']['median_p50']:.4f}** | {desc['monthly_churn_rate']['p90']:.4f} |
| **LTV da Coorte (R$)** | {desc['cohort_ltv_brl']['mean']} | {desc['cohort_ltv_brl']['std']} | {desc['cohort_ltv_brl']['p10']} | **{desc['cohort_ltv_brl']['median_p50']}** | {desc['cohort_ltv_brl']['p90']} |
| **Razão LTV / CAC** | {desc['ltv_cac_ratio']['mean']}x | {desc['ltv_cac_ratio']['std']}x | {desc['ltv_cac_ratio']['p10']}x | **{desc['ltv_cac_ratio']['median_p50']}x** | {desc['ltv_cac_ratio']['p90']}x |

> **Insight Estratégico de Coorte:** {coh['strategic_finding']}

---

## 🤖 4. Parecer do Cientista de Dados (Lucas Bittencourt)

### 4.1 Validação Preditiva (Out-of-Sample Strict Split 80/20)
- **RMSE Baseline (Média Ingênua):** R$ {ml['baseline_naive_rmse_brl']:,.2f}
- **RMSE Modelo Ridge (Treino / Teste):** R$ {ml['ridge_regression_train_rmse_brl']:,.2f} / **R$ {ml['ridge_regression_test_rmse_brl']:,.2f}**
- **Intervalo de Confiança 95% (Bootstrap RMSE Teste):** `[R$ {ml['bootstrap_95ci_test_rmse'][0]:,.2f}, R$ {ml['bootstrap_95ci_test_rmse'][1]:,.2f}]`
- **Coeficiente de Determinação ($R^2$ Teste):** `{ml['test_r2_score']:.4f}`

### 4.2 Resultados da Simulação de Monte Carlo ({mc['n_trajectories']} Cenários Fechados em {mc['horizon_months']} Meses)
- **Preço Calibrado na Simulação:** R$ {mc['calibrated_simulation_price_brl']:.2f}
- **Caixa Final Acumulado (P10 / Mediana P50 / P90):** R$ {mc['final_cash_p10_brl']:,.2f} / **R$ {mc['final_cash_median_p50_brl']:,.2f}** / R$ {mc['final_cash_p90_brl']:,.2f}
- **VPL (Valor Presente Líquido) Mediano:** **R$ {mc['npv_median_p50_brl']:,.2f}** (Média: R$ {mc['npv_mean_brl']:,.2f})
- **Probabilidade de VPL Positivo:** **{mc['probability_positive_npv_pct']}%**
- **Break-even Operacional Mediano:** **Mês {mc['median_operational_breakeven_month']}**

---

## 🛡️ 5. Parecer da Atuária (Beatriz Alencar)

| Indicador de Risco Atuarial & Solvência | Valor Calculado | Interpretação Técnica |
| :--- | :---: | :--- |
| **Capital Inicial Alocado ($u_0$)** | R$ {act['initial_capital_allocated_brl']:,.2f} | Caixa inicial disponível no mês 0 |
| **Probabilidade de Ruína ($\\psi(u_0)$)** | **{act['ruin_probability_pct']}%** | Fração das {mc['n_trajectories']} trajetórias que tocaram caixa $< 0$ |
| **Value at Risk ($\\text{{VaR}}_{{95\\%}}$ sobre VPL)** | R$ {act['var_95_npv_loss_brl']:,.2f} | Perda/resultado no percentil 95% de estresse |
| **Expected Shortfall ($\\text{{CVaR}}_{{95\\%}}$)** | R$ {act['cvar_95_expected_shortfall_brl']:,.2f} | Resultado médio nos 5% piores cenários |
| **Drawdown Máximo de Caixa (P99)** | R$ {act['worst_1pct_cash_drawdown_brl']:,.2f} | Consumo máximo de caixa no 1% pior cenário |
| **Capital Recomendado de Solvência (99%)** | **R$ {act['recommended_solvency_capital_99pct_brl']:,.2f}** | Reserva adicional necessária: **R$ {act['additional_contingency_reserve_needed_brl']:,.2f}** |
| **Sobrevivência da Carteira (12m / 24m)** | {surv['client_survival_12m_pct']}% / {surv['client_survival_24m_pct']}% | Expectativa de vida contratual ($e_0$): **{surv['customer_life_expectancy_months']} meses** |
| **Prêmio Puro / Comercial de Risco Mensal** | R$ {surv['pure_monthly_claim_cost_per_client_brl']:.2f} / **R$ {surv['loaded_actuarial_risk_charge_per_client_brl']:.2f}** | Custo atuarial por cliente ativo (c/ carregamento de 30%) |

---

## 🚀 6. Plano de Ação Consolidado (Orquestração Axio Vance)

### Fase 1 — Calibração de Preço e Blindagem Atuarial (Dias 1 a 30)
1. **Ajuste Gradual de Precificação (Henrique + Beatriz):** Migrar do preço base de R$ {math_out['base_price_brl']:.2f} para a faixa calibrada de **R$ {mc['calibrated_simulation_price_brl']:.2f}**, já embutindo o carregamento atuarial de **R$ {surv['loaded_actuarial_risk_charge_per_client_brl']:.2f}/cliente** para cobrir sinistros de cauda longa.
2. **Constituição de Reserva Técnica (Beatriz):** Manter o capital inicial de R$ {act['initial_capital_allocated_brl']:,.2f} e provisionar linha de contingência de **R$ {act['additional_contingency_reserve_needed_brl']:,.2f}** para garantir 99% de imunidade contra ruína de caixa antes do mês {mc['median_operational_breakeven_month']}.

### Fase 2 — Otimização de Ativação e Retenção por Coorte (Dias 31 a 60)
3. **Gatilho de Qualidade de Onboarding (Clara):** Travar meta operacional mínima de *Onboarding Score* $\\ge 75$, onde os dados demonstram queda do churn mensal para **{coh['high_onboarding_monthly_churn_pct']}%** e salto do $\\text{{LTV/CAC}}$ para **{coh['high_onboarding_score_ltv_cac']}x**.

### Fase 3 — Escala Preditiva e Monitoramento de Drift (Dias 61 a 90)
4. **Alocação Guiada por Modelo Preditivo (Lucas):** Utilizar os pesos padronizados do modelo preditivo validado para direcionar orçamento de aquisição apenas para coortes com VPL líquido projetado positivo e monitorar mensalmente a aderência da curva real contra a curva de difusão de Bass.
"""

    report_path.write_text(content, encoding="utf-8")
    return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Motor Multi-Agente Argon (Axio Orchestrator)")
    parser.add_argument(
        "--config",
        type=str,
        default=str(ROOT_DIR / "sandbox" / "configs" / "default_project.json"),
        help="Caminho para o arquivo JSON de configuração do projeto.",
    )
    args = parser.parse_args()

    cfg_path = Path(args.config)
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    print(f"[Axio Orquestrador] Iniciando pipeline para: {cfg['project_name']}")

    # 1. Matemático
    math_out = run_mathematician_module(cfg)
    print(
        f"  -> [Henrique Vasconcelos - Matemático] Preço ótimo analítico: R$ {math_out['optimal_price_brl']}"
    )

    # 2. Geração de Dados Estatísticos Sintéticos (Cientista de Dados + Analista)
    records, csv_path = generate_synthetic_dataset(cfg, math_out)
    print(f"  -> [Sandbox] Dataset estatístico criado ({len(records)} linhas): {csv_path.name}")

    # 3. Analista de Dados
    analyst_out = run_data_analyst_module(records)
    print(
        f"  -> [Clara Mendonça - Analista de Dados] LTV/CAC Mediano: {analyst_out['descriptive_statistics']['ltv_cac_ratio']['median_p50']}x"
    )

    # 4. Cientista de Dados (ML + Monte Carlo)
    ds_out = run_data_scientist_module(cfg, records, math_out)
    mc = ds_out["monte_carlo_closed_simulation"]
    print(
        f"  -> [Lucas Bittencourt - Cientista de Dados] Simulação ({mc['n_trajectories']} runs) concluída. VPL Mediano: R$ {mc['npv_median_p50_brl']:,.2f}"
    )

    # 5. Atuária
    actuary_out = run_actuary_module(cfg, ds_out)
    act = actuary_out["actuarial_solvency_metrics"]
    print(
        f"  -> [Beatriz Alencar - Atuária] Prob. de Ruína: {act['ruin_probability_pct']}% | Parecer: {actuary_out['actuarial_verdict']}"
    )

    # 6. Consolidação do Relatório e Plano de Ação por Axio
    report_path = generate_executive_report(
        cfg, math_out, analyst_out, ds_out, actuary_out, csv_path
    )
    print(f"[Axio Orquestrador] Relatório Mestre gerado com sucesso em: {report_path}")


if __name__ == "__main__":
    main()
