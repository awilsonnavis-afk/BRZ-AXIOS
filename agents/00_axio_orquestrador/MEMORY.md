# 💾 MEMORY.md — Memória Persistente do Orquestrador (Axio Vance)

> **Propósito:** Registro cronológico e imutável de decisões arquiteturais, estado da equipe, parâmetros globais e handoffs para que qualquer modelo de IA possa continuar o trabalho exatamente de onde parou.

---

## 🏛️ 1. Contexto Permanente da Equipe
- **Orquestrador:** Axio Vance (`agents/00_axio_orquestrador`)
- **Matemático:** Henrique Vasconcelos (`agents/01_henrique_vasconcelos_matematico`)
- **Analista de Dados:** Clara Mendonça (`agents/02_clara_mendonca_analista_dados`)
- **Cientista de Dados:** Lucas Bittencourt (`agents/03_lucas_bittencourt_cientista_dados`)
- **Atuária:** Beatriz Alencar (`agents/04_beatriz_alencar_atuaria`)

---

## 📜 2. Log de Decisões e Checkpoints

### [2026-11-01] — Inicialização da Arquitetura Argon
- **Contexto:** Criação da estrutura completa da equipe a pedido do usuário.
- **Decisões Técnicas:**
  1. Adotado banco híbrido JSON + SQLite (`database/references.db`) com 25 fontes de alta relevância (MathOverflow, CrossValidated, Kaggle, Data Hackers, IBA/SUSEP, SOA/CAS, IMPA, 3Blue1Brown, StatQuest, etc.).
  2. Criado o motor `core/argon_engine.py` capaz de operar em ambiente fechado (sem depender de APIs externas instáveis) para gerar dados estatísticos, simular cenários de Monte Carlo, ajustar regressões/modelos preditivos, calcular métricas atuariais ($\text{VaR}$, $\text{CVaR}$, Probabilidade de Ruína, Índice de Solvência) e emitir relatórios completos em Markdown.
- **Próximo Passo para Qualquer IA:** Ao receber um novo projeto do usuário, ler este arquivo, criar uma nova seção de projeto em `PLANNING.md` e executar o pipeline dos 4 especialistas.


### [2026-11-01 15:40] — Execução do Projeto `PROJ-002-KALSHI-NFL` (`KXNFLGAME`)
- **Contexto:** O usuário solicitou testar a equipe com a página de mercados da NFL na Kalshi (`https://kalshi.com/markets/kxnflgame/nfl-game?utm_source=kalshiweb_eventpage`) para responder "Quem vai ganhar?".
- **Execução:**
  - Criado motor especializado `core/kalshi_nfl_engine.py` e configuração `sandbox/configs/kalshi_kxnflgame_26nov01.json`.
  - Simulados todos os 9 confrontos da série `KXNFLGAME-26NOV01*` com 10.000 iterações de Monte Carlo por jogo (90.000 partidas simuladas) e modelo preditivo validado em 1.800 jogos sintéticos (`PROJ-002-KALSHI-NFL_synthetic_matchups.csv`).
  - Identificados os vencedores mais prováveis em campo (NYJ 76.8%, DET 71.5%, DAL 70.3%, WAS 67.8%, BUF 65.8%, TB 61.9%, KC 60.1%, LAC 56.2%, JAC 52.1%) e separado o que é "favorito no campo" do que possui "Valor Esperado Positivo (Edge) no contrato Kalshi".


### [2026-11-01 15:51] — ⚠️ CORREÇÃO DE INTEGRIDADE do `PROJ-002-KALSHI-NFL`
- **Para qualquer IA que continuar:** os resultados do PROJ-002 são **ilustrativos**, não previsões válidas.
  1. Elo / Off-Def EPA / Turnovers / HFA em `sandbox/configs/kalshi_kxnflgame_26nov01.json` foram **estimados**, não coletados de fonte (nflverse, etc.).
  2. Preços Kalshi: BUF/BAL, KC/DEN, PHI/WAS, DET/MIN vieram de um resumo de busca (covers.com) com data incerta; os outros 5 jogos foram **estimados**. Nenhum preço foi lido da API da Kalshi.
  3. A "validação out-of-sample" (62.78%, Brier 0.2243) usou dados sintéticos gerados pela **mesma equação** do modelo estrutural → validação circular, sem evidência de poder preditivo real.
  4. Os "edges" decorrem dessas entradas estimadas; não usar para operar.
- **Próximo passo obrigatório:** reconstruir com dados reais (API pública da Kalshi + nflverse) e backtest histórico real antes de qualquer conclusão. Ver plano de melhoria na conversa de 2026-11-01 15:51.


### [2026-11-01 16:51] — Calibração com Dados 100% Reais (`PROJ-003-KC-DEN-CALIBRACAO-REAL`)
- **Fontes:** `sandbox/data/games.csv` (`nflverse`, 7.391 jogos concluídos de 1999 a Sem. 7 de 2026) + API pública da Kalshi (`KXNFLGAME-26NOV01KCDEN`).
- **Descoberta Principal de Engenharia de Features:** O modelo Elo Simples (Gen 1) errava ao projetar apenas `33.30%` para KC porque punia o time pelas derrotas das Semanas 16-18 de 2025 com QBs reservas (`Chris Oladokun` e `Gardner Minshew`). Ao separar `QB_Elo` (`Patrick Mahomes = 1711.4` vs `Bo Nix = 1668.2` vs `Oladokun = 1481.0`) e incluir a Expectativa Pitagórica de 2026 (`KC 62.3%` com saldo `+40` vs `DEN 50.9%` com saldo `+3`) e o confronto direto da Semana 1 (`KC 31 x 10 DEN`), a acurácia real em 398 jogos de 2025-2026 subiu de `62.81%` para **`64.82%`** (e **`65.33%`** no Ensemble Gen 3), projetando **Kansas City Chiefs favorito com `53.98%` (Gen 2) / `52.87%` (Gen 3)** — em linha com o fechamento da Kalshi (`52.5%` mid / `53¢` ask) e confirmado pelo movimento ao vivo para `60¢`.


### [2026-11-01 17:03] — Execução Multi-Sandbox (`sandbox_01..05`) e Tribunal Atuarial (5 Pessimistas vs 5 Otimistas + Juiz Supremo em Gemini Argon)
- **Fontes Expandidas:** Adicionados `sandbox/data/kalshi_kcden_spread.json` (24 strikes de spread alternativo Kalshi), `sandbox/data/kalshi_kcden_total.json` (19 strikes de total de pontos Kalshi), `sandbox/data/kalshi_kcden_latest.json` (10,75M contratos) e `sandbox/data/nfl_teams.csv`.
- **Resultados das 5 Sandboxes Separadas (`KC Chiefs @ DEN Broncos`):**
  1. `sandbox_01_historico_altitude`: `P(KC) = 47.54%` | `P(DEN) = 52.46%`
  2. `sandbox_02_dominancia_mahomes_pitagoras`: `P(KC) = 58.34%` | `P(DEN) = 41.66%`
  3. `sandbox_03_curva_derivativos_kalshi`: `P(KC) = 56.55%` | `P(DEN) = 43.45%`
  4. `sandbox_04_stress_trincheiras_divisional`: `P(KC) = 51.46%` | `P(DEN) = 48.54%`
  5. `sandbox_05_tribunal_10_atuarios_juiz`: Bancada Pessimista (`50.90%`), Bancada Otimista (`56.30%`), Sentença Final do Juiz Supremo (**`53.88%` para Kansas City Chiefs**, placar **9 votos a 1** para vitória do KC no campo, com trava de exposição de `1.0%` até `53¢` no pré-jogo e bloqueio de nova entrada acima de `56¢–58¢` ao vivo).
