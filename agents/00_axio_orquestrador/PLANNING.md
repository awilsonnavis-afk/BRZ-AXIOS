# 🗺️ PLANNING.md — Planejamento Mestre (Axio Vance)

> **Status Atual do Sistema:** `OPERACIONAL / PRONTO PARA PROJETOS`  
> **Última Atualização:** 2026-11-01  
> **Responsável:** Axio Vance — Orquestrador e Programador Sênior

---

## 📌 1. Checklist de Fundação da Equipe Argon
- [x] Pesquisar requisitos operacionais, cognitivos e ferramental da equipe multidisciplinar (`docs/PESQUISA_ARQUITETURA_EQUIPE.md`).
- [x] Construir Banco de Dados de Referências de comunidades, fóruns, redes sociais e canais do YouTube (`database/references.db` e `database/CATALOGO_REFERENCIAS.md`).
- [x] Definir identidades (`SOUL.md`), manuais agnósticos de IA (`AGENTS.md`), memória (`MEMORY.md`), planejamento (`PLANNING.md`) e ferramentas (`TOOLS.md`) para todos os membros.
- [x] Implementar o Motor Computacional de Simulação e Validação em Ambiente Fechado (`core/argon_engine.py`).
- [x] Executar simulação de validação completa (Benchmarking + Geração de Dados Estatísticos + Modelagem + Risco Atuarial + Relatório de Previsões e Plano de Ação).

---

## 🚀 2. Template de Plano para Novos Projetos (Copiar ao Iniciar Nova Demanda)

```markdown
### Projeto: [NOME DO PROJETO / IDEIA]
- **Objetivo Principal:** [O que queremos validar ou prever?]
- **Horizonte de Simulação:** [Ex: 12, 24 ou 36 meses]
- **Orçamento / Capital Inicial em Risco:** [Valor em R$ ou US$]
- **Status por Agente:**
  - [ ] Clara Mendonça (Analista de Dados): Coleta de benchmarks e diagnóstico inicial
  - [ ] Henrique Vasconcelos (Matemático): Equações do sistema e otimização
  - [ ] Lucas Bittencourt (Cientista de Dados): Geração sintética, Monte Carlo e predição
  - [ ] Beatriz Alencar (Atuária): Cálculo de VaR, CVaR, probabilidade de ruína e solvência
  - [ ] Axio Vance (Orquestrador): Consolidação do Relatório e Plano de Ação
```


---

## 🏈 3. Projeto Ativo Concluído: `PROJ-002-KALSHI-NFL` (2026-11-01)
- **URL:** https://kalshi.com/markets/kxnflgame/nfl-game?utm_source=kalshiweb_eventpage
- **Objetivo Principal:** Prever os vencedores dos 9 jogos da série `KXNFLGAME` (rodada `26NOV01`) e estruturar um Plano de Ação com Critério de Kelly e blindagem atuarial.
- **Status por Agente:**
  - [x] Clara Mendonça (Analista de Dados): Extração dos 9 confrontos, desvigagem de odds Kalshi e análise de Net EPA ([kalshi_nfl_market_efficiency.json](file:///c:/NWX/nwx-Argon/agents/02_clara_mendonca_analista_dados/outputs/kalshi_nfl_market_efficiency.json))
  - [x] Henrique Vasconcelos (Matemático): Equação de diferencial de pontos Elo-EPA e otimização de Kelly fracionária ([kalshi_nfl_equacoes_kelly.json](file:///c:/NWX/nwx-Argon/agents/01_henrique_vasconcelos_matematico/outputs/kalshi_nfl_equacoes_kelly.json))
  - [x] Lucas Bittencourt (Cientista de Dados): Geração de 1.800 jogos sintéticos, validação Out-of-Sample (62.78% acurácia, Brier 0.2243) e 90.000 simulações Monte Carlo ([kalshi_nfl_monte_carlo_ml.json](file:///c:/NWX/nwx-Argon/agents/03_lucas_bittencourt_cientista_dados/outputs/kalshi_nfl_monte_carlo_ml.json))
  - [x] Beatriz Alencar (Atuária): Cálculo de VaR 95% (US$ 129.50), CVaR 95% e Probabilidade de Ruína (0.0%) ([kalshi_nfl_parecer_atuarial.json](file:///c:/NWX/nwx-Argon/agents/04_beatriz_alencar_atuaria/outputs/kalshi_nfl_parecer_atuarial.json))
  - [x] Axio Vance (Orquestrador): Consolidação do relatório executivo em [RELATORIO_KALSHI_NFL_26NOV01.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_KALSHI_NFL_26NOV01.md)


---

## 🎯 4. Projeto Concluído com Dados 100% Reais: `PROJ-003-KC-DEN-CALIBRACAO-REAL` (2026-11-01)
- **Alvo:** Afinamento de assertividade no confronto **Kansas City Chiefs @ Denver Broncos (`KXNFLGAME-26NOV01KCDEN`)** com dados reais da API da Kalshi + `7.548` jogos oficiais do `nflverse` (`sandbox/data/games.csv`).
- **Entregáveis Validados:**
  - [x] Coleta da API Oficial Kalshi (`KXNFLGAME-26NOV01KCDEN-KC` e `-DEN`: Pré-jogo `53¢ / 48¢`, Ao vivo `60¢ / 41¢`, Volume `8,87M` contratos).
  - [x] Backtest Walk-Forward em `7.391` jogos concluídos (`1999–2026`) e validação fora da amostra nos `398` jogos reais de `2025–2026` ([kc_den_real_backtest.py](file:///c:/NWX/nwx-Argon/core/kc_den_real_backtest.py)).
  - [x] Elevação da acurácia fora da amostra do Modelo Fundamental de `62.81%` (Gen 1) para **`64.82%` (Gen 2 com `QB_Elo`, Expectativa Pitagórica e H2H)** e **`65.33%` (Gen 3 Ensemble)**.
  - [x] Relatório executivo salvo em [RELATORIO_KC_VS_DEN_CALIBRACAO_REAL.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_KC_VS_DEN_CALIBRACAO_REAL.md).


---

## ⚖️ 5. Projeto Multi-Sandbox & Tribunal Atuarial Concluído: `PROJ-004-MULTI-SANDBOX-TRIBUNAL-KCDEN` (2026-11-01)
- **Objetivo:** Expandir as fontes de dados reais (incluindo os 24 mercados de Spread Alternativo `KXNFLSPREAD` e os 19 mercados de Total de Pontos `KXNFLTOTAL` da Kalshi + `nfl_teams.csv`), criar **5 cenários em sandboxes isoladas** (`sandbox/environments/sandbox_01..05`) e validar em **Gemini 4 Argon** com **5 Atuários Pessimistas, 5 Atuários Otimistas e 1 Juiz Supremo**.
- **Status:**
  - [x] Expansão da base de dados real (`45` mercados Kalshi + `7.548` jogos `nflverse` + `29` referências em `database/references.db`).
  - [x] Execução isolada das 5 sandboxes (`60.000` simulações Monte Carlo em [multi_sandbox_tribunal_engine.py](file:///c:/NWX/nwx-Argon/core/multi_sandbox_tribunal_engine.py)).
  - [x] Validação em paralelo por 3 colegiados em Gemini Argon ([Pessimistas](conversation://47bd71f9-780d-48f8-9594-3a5d9f5cc752), [Otimistas](conversation://a40ea5a4-57fb-4275-8d2f-e0ceac03ce48) e [Juiz Supremo](conversation://2d10eb84-dc14-4eff-a87a-37605a3c86a3)).
  - [x] Dossiê final consolidado em [RELATORIO_MULTI_SANDBOX_E_TRIBUNAL_ATUARIAL.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_MULTI_SANDBOX_E_TRIBUNAL_ATUARIAL.md).

---

## 🕵️‍♂️ 6. Inteligência Granular de Jogadores (`05_gabriel_torres`) & Boleta Operacional de Contratos: `PROJ-005-SCOUT-TRADING-DESK` (2026-11-01)
- **Objetivo:** Criar o agente **Gabriel Torres (`agents/05_gabriel_torres_investigador_fontes/`)** para extrair elencos, lesões (`ACT`/`INA`/`RES`) e performance individual (`weekly_rosters_2026.csv`, `stats_player_week_2026.csv`, `stats_team_week_2026.csv`), responder *"O que poderia favorecer ou ameaçar essa predição?"*, alimentar o debate entre os 5 Atuários Pessimistas e 5 Otimistas e gerar uma **Boleta Operacional de Contratos Kalshi** com valores, probabilidades de fechamento (`100¢` vs `0¢`) e vendas antecipadas escalonadas (`65¢`, `76¢`, Stop-Loss `36¢`).
- **Status:**
  - [x] Criação da pasta completa de `agents/05_gabriel_torres_investigador_fontes/` (`SOUL.md`, `AGENTS.md`, `PLANNING.md`, `MEMORY.md`, `TOOLS.md`).
  - [x] Extração de `weekly_rosters_2026.csv` (6,48 MB), `stats_player_week_2026.csv` (3,34 MB) e `stats_team_week_2026.csv` (88 KB) em [gabriel_scout_and_trading_desk.py](file:///c:/NWX/nwx-Argon/core/gabriel_scout_and_trading_desk.py).
  - [x] Dossiê de lesões/performance e Boleta Operacional salvos em [dossie_kc_den_jogadores_lesoes_performance.json](file:///c:/NWX/nwx-Argon/agents/05_gabriel_torres_investigador_fontes/outputs/dossie_kc_den_jogadores_lesoes_performance.json) e [RELATORIO_OPERACAO_CONTRATOS_E_INTELIGENCIA_JOGADORES.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_OPERACAO_CONTRATOS_E_INTELIGENCIA_JOGADORES.md).

---

## 🇧🇷 7. Validação de Busca e Operações Brasil (Polymarket + Kalshi): `PROJ-006-BRAZIL-POLYMARKET-KALSHI` (2026-11-01)
- **Objetivo:** Validar a busca automatizada nas APIs oficiais da **Polymarket (`gamma-api.polymarket.com`)** e **Kalshi (`api.elections.kalshi.com/trade-api/v2`)** para todas as operações que envolvem o **Brasil**, parear contratos entre as duas bolsas e gerar o relatório com Boletas Operacionais.
- **Status:**
  - [x] Implementação do scanner multi-bolsa [brazil_markets_scanner.py](file:///c:/NWX/nwx-Argon/core/brazil_markets_scanner.py) (`30` eventos ativos na Polymarket, `97` séries e `201` eventos na Kalshi, sendo `20` com contratos ativos agora).
  - [x] Implementação do motor de análise e arbitragem [brazil_polymarket_kalshi_engine.py](file:///c:/NWX/nwx-Argon/core/brazil_polymarket_kalshi_engine.py).
  - [x] Geração do relatório completo com 4 Boletas Operacionais Brasil em [RELATORIO_BRASIL_POLYMARKET_E_KALSHI.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_BRASIL_POLYMARKET_E_KALSHI.md).
  - [x] Priorização Editorial por Volume (`60` operações, `US$ 2.68M+` em volume) em [brazil_editorial_prioritizer.py](file:///c:/NWX/nwx-Argon/core/brazil_editorial_prioritizer.py) e [PAUTA_EDITORIAL_E_RANKING_VOLUME_BRASIL.md](file:///c:/NWX/nwx-Argon/reports/PAUTA_EDITORIAL_E_RANKING_VOLUME_BRASIL.md).
  - [x] Auditoria da Operação Real ao Vivo na Kalshi (`KC Chiefs vs DEN Broncos`, `130.23 shares` a `53.75¢`, venda de `104 shares` a `77¢` no Q3 recuperando `US$ 77.29` em caixa e mantendo `26.23 shares` em *Free-Roll*) em [AVALIACAO_HALFTIME_KC_17_13_DEN_E_POSICAO_REAL.md](file:///c:/NWX/nwx-Argon/reports/AVALIACAO_HALFTIME_KC_17_13_DEN_E_POSICAO_REAL.md).

---

## 🏛️ 8. Integração Diária do Grafo Argon no BRZ News (`Hunter Vance`, `BRZ.PREDICTION` e `BRZ.DESK Prediction`): `PROJ-008-BRZ-NEWS-DAILY-PREDICTION-GRAPH` (2026-11-01)
- **Objetivo:** Analisar os repositórios do Lucas (`lucascs1/brz-news-backend` e `lucascs1/brz-news-frontend`), mapear o funcionamento do `Hunter Vance v2` (`src/agents/hunter_vance/hunter_v2.py` e `config/hunter_sources.json`), e implementar o grafo diário que alimenta as pautas editoriais, a página pública/assinante **`BRZ.PREDICTION`** e a mesa institucional **`BRZ.DESK Prediction`**.
- **Status:**
  - [x] Análise completa do `hunter_v2.py`, `capital_signals.py`, `importance.py`, `focus.py` (4 janelas `09h`, `11h`, `17h`, `19h ET`), `LANES.yml` e `DATA_CONTRACT.md` no backend, além de `TradingDesk.tsx`, `OrderTicket.tsx` e `prediction-markets.ts` no frontend.
  - [x] Implementação do motor de integração diária [brz_news_daily_prediction_graph.py](file:///c:/NWX/nwx-Argon/core/brz_news_daily_prediction_graph.py).
  - [x] Geração dos contratos JSON prontos para o Firestore (`brz-news-prod`):
    - [hunter_prediction_pautas.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/hunter_prediction_pautas.json) (3 pautas completas com `capital_signal` 6 campos e `headline_boost_safe`).
    - [firestore_brz_prediction_public.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/firestore_brz_prediction_public.json) (`prediction_radar/latest` com 15 mercados Tier 1/2 e arbitragem Polymarket vs Kalshi para a página `BRZ.PREDICTION`).
    - [firestore_brz_desk_prediction_pro.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/firestore_brz_desk_prediction_pro.json) (`desk_predictions/latest` com Orderbook, Inteligência Gabriel Torres, Tribunal 5x5 + Juiz e Boleta em 3 Lotes para a página `BRZ.DESK Prediction`).
  - [x] Especificação arquitetural e plano de PRs por Lane documentados em [ARQUITETURA_INTEGRACAO_BRZ_NEWS_HUNTER_E_PREDICTION_DESK.md](file:///c:/NWX/nwx-Argon/reports/ARQUITETURA_INTEGRACAO_BRZ_NEWS_HUNTER_E_PREDICTION_DESK.md).

