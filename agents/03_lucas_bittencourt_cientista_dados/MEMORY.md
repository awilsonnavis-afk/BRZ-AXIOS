# 💾 MEMORY.md — Memória Persistente (Lucas Bittencourt - Cientista de Dados)

## 🧪 1. Protocolo de Experimentação e Simulação da Equipe
- **Semente Padrão de Reprodutibilidade:** `SEED = 42` (configurável por experimento em `sandbox/configs/`).
- **Regra ML Best Practices:**
  1. Split Treino/Teste (80%/20%) ou Cronológico estrito antes de padronização (`Z-score`).
  2. Comparação obrigatória contra *Baseline* (Média/Mediana ou Regressão Linear Simples) antes de aprovar modelos multivariados ou não-lineares.
  3. Cálculo de Intervalo de Confiança de 95% via *Bootstrapping* para RMSE, MAE e $R^2$.

## 📜 2. Log de Entregas e Handoffs
- **[2026-11-01]:** Motor de dados sintéticos e simulação Monte Carlo em ambiente fechado integrado ao `core/argon_engine.py`.
