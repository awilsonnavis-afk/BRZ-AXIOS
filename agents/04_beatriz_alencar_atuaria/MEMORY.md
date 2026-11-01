# 💾 MEMORY.md — Memória Persistente (Beatriz Alencar - Atuária)

## 🛡️ 1. Critérios Atuariais de Aprovação de Projetos (Padrão Argon)
- **Critério 1 — Probabilidade de Ruína ($\psi(u)$):**
  - $\psi(u) \le 1.0\%$: **Solvência Grau Investimento (Aprovado)**
  - $1.0\% < \psi(u) \le 5.0\%$: **Risco Moderado (Aprovado com Exigência de Reserva Técnica Adicional)**
  - $\psi(u) > 5.0\%$: **Alto Risco de Insolvência (Requer Reestruturação de Capital ou Custos Fixos)**
- **Critério 2 — Cobertura de Cauda ($\text{CVaR}_{95\%}$):**
  - A reserva de contingência recomendada deve cobrir pelo menos o déficit esperado nos 5% piores cenários ($\text{CVaR}_{95\%}$).
- **Critério 3 — Análise de Sobrevivência de Clientes/Receita:**
  - Taxa de retenção mensal $S(1) = 1 - q_x$ determina a expectativa de vida contratual $e_0 = \frac{1}{q_x}$ sob risco constante (Weibull/Exponencial).

## 📜 2. Log de Entregas e Handoffs
- **[2026-11-01]:** Módulo atuarial de cálculo de VaR, CVaR, Probabilidade de Ruína e Reserva de Solvência integrado ao motor `core/argon_engine.py`.
