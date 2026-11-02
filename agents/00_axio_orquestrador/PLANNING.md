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

## 🏛️ 8. Integração Diária do Grafo Argon no BRZ News (`Hunter Vance`, `BRZ.PREDICTION` e `BRZ.DESK Prediction` v3.0): `PROJ-008-BRZ-NEWS-DAILY-PREDICTION-GRAPH` (2026-11-01)
- **Objetivo:** Analisar os repositórios do Lucas (`lucascs1/brz-news-backend` e `lucascs1/brz-news-frontend`), mapear o funcionamento do `Hunter Vance v2` (`src/agents/hunter_vance/hunter_v2.py` e `config/hunter_sources.json`), e implementar o grafo diário v3.0 com **Filtro Estrito `100% BRASIL + ALTO VOLUME`**, **Terminal Diário `BRZ.DESK Prediction` por Ativo**, **Relatório Semanal `AXIOS` do Líder de Volume em `BRZ.PREDICTION`** e **Editorial/Redes Sociais focado em `Prediction & Market` (sem Política no principal)**.
- **Status:**
  - [x] Análise completa do `hunter_v2.py`, `capital_signals.py`, `importance.py`, `focus.py` (4 janelas `09h`, `11h`, `17h`, `19h ET`), `LANES.yml` e `DATA_CONTRACT.md` no backend, além de `TradingDesk.tsx`, `OrderTicket.tsx` e `prediction-markets.ts` no frontend.
  - [x] Teste ao vivo da página `KXNFLGAME` ([scan_kxnflgame_live.py](file:///c:/NWX/nwx-Argon/core/scan_kxnflgame_live.py) e [run_kxnflgame_live_test.py](file:///c:/NWX/nwx-Argon/core/run_kxnflgame_live_test.py)) e Post-Mortem oficial do jogo liquidado `KXNFLGAME-26NOV01KCDEN` (`US$ 50.20M` volume; virada de Denver no Q4 comprovou a eficácia matemática do *Free-Roll* no Q3, garantindo `+US$ 7.29` / `+10.41%` em dinheiro real contra `-100%` de quem segurou até o fim) em [RELATORIO_TESTE_AO_VIVO_KALSHI_KXNFLGAME.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_TESTE_AO_VIVO_KALSHI_KXNFLGAME.md).
  - [x] Implementação do motor v3.0 [brz_news_daily_prediction_graph.py](file:///c:/NWX/nwx-Argon/core/brz_news_daily_prediction_graph.py) e geração dos contratos JSON prontos para o Firestore (`brz-news-prod`):
    - [firestore_brz_desk_prediction_pro.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/firestore_brz_desk_prediction_pro.json) (`desk_predictions/latest` com 3 Workspaces Diários completos por ativo: `WS-01-USDBRL-DOLAR`, `WS-02-IPCA-INFLACAO-2026`, `WS-03-COPOM-SELIC-NOV`, incluindo Gráfico de Terminal, Orderbooks Kalshi + Polymarket lado a lado, Análise Fundamentalista, Análise Técnica/Gráfica, Notícias de Mercado, Tribunal 5x5 + Juiz e Boleta *Free-Roll*).
    - [firestore_brz_prediction_public.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/firestore_brz_prediction_public.json) (`prediction_radar/latest` com todos os 23 contratos Brasil qualificados `>= US$ 10k`, Relatório Semanal `AXIOS` do Líder de Volume `US$ 574.5K USD/BRL`, Feed de Notícias Catalisadoras e Arbitragem Cross-Exchange).
    - [hunter_prediction_pautas.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/hunter_prediction_pautas.json) (remoção de `Politics` das janelas principais em `focus.py`, 3 pautas com `capital_signal` e 2 Carrosséis de 6 slides com Hooks analíticos de 45–65 palavras focados em oportunidades de mercado).
  - [x] Criação do Canvas Interativo da Arquitetura GCP e UI em [grafo_prediction_gcp_canvas.html](file:///c:/NWX/nwx-Argon/reports/grafo_prediction_gcp_canvas.html) e documentação em [ARQUITETURA_INTEGRACAO_BRZ_NEWS_HUNTER_E_PREDICTION_DESK.md](file:///c:/NWX/nwx-Argon/reports/ARQUITETURA_INTEGRACAO_BRZ_NEWS_HUNTER_E_PREDICTION_DESK.md).
  - [x] Implementação do Grafo v4.0 com Matriz de Saídas de Mitigação de Erro (`Drawdown Recovery & Air-Pocket Decompression`) em [argon_error_mitigation_engine.py](file:///c:/NWX/nwx-Argon/core/argon_error_mitigation_engine.py), [ARGON_V4_ERROR_MITIGATION_EXITS.json](file:///c:/NWX/nwx-Argon/sandbox/runs/ARGON_V4_ERROR_MITIGATION_EXITS.json) e [AUDITORIA_ERROS_E_MATRIZ_MITIGACAO_SAIDAS_V4.md](file:///c:/NWX/nwx-Argon/reports/AUDITORIA_ERROS_E_MATRIZ_MITIGACAO_SAIDAS_V4.md).

---

## 🇨🇦 9. Teste Multi-Domínio do Grafo v4.0: Mercado de Opções e Derivativos do Dólar Canadense (`PROJ-009-CAD-OPTIONS-V4`) (2026-11-01)
- **Objetivo:** Validar o Grafo Argon v4.0 (com precificação **Garman-Kohlhagen 1983**, **Barreira Contínua One-Touch Reiner-Rubinstein** e **Matriz de 4 Saídas de Mitigação de Erro**) no mercado de Opções Tradicionais (`USD/CAD`, `FXC`, futuros CME `6C`) e Opções Binárias de Eventos (`Kalshi` e `Polymarket`) para o Dólar Canadense (`CAD`).
- **Status:**
  - [x] Coleta de dados reais de mercado ([scan_cad_options_live.py](file:///c:/NWX/nwx-Argon/core/scan_cad_options_live.py) e [scan_cad_deep.py](file:///c:/NWX/nwx-Argon/core/scan_cad_deep.py)): `USD/CAD Spot = 1.3986`, `CAD/USD = 0.7150`, `FXC = US$ 69.93`, `WTI = US$ 101.00`, `US 10Y = 4.929%`, `121` séries e `269` eventos na Kalshi + `8` eventos ativos na Polymarket (`US$ 271.85K` de volume nos mercados do Bank of Canada).
  - [x] Execução do motor quantitativo v4.0 ([cad_options_quant_engine.py](file:///c:/NWX/nwx-Argon/core/cad_options_quant_engine.py)) e geração do payload completo ([CAD_OPTIONS_V4_ANALYSIS_RESULTS.json](file:///c:/NWX/nwx-Argon/sandbox/runs/CAD_OPTIONS_V4_ANALYSIS_RESULTS.json)).
  - [x] Consolidação das cadeias de opções (Gregas $\Delta, \Gamma, \mathcal{V}, \Theta$), arbitragem Polymarket vs. Kalshi (`BoC +25 bps` em Dezembro: Compra `37.0¢` na Polymarket vs. `Bid 38.0¢–39.0¢` na Kalshi) e trava vertical `Bear Put Spread FXC $70.00 / $68.50` em [RELATORIO_OPCOES_DOLAR_CANADENSE_V4.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_OPCOES_DOLAR_CANADENSE_V4.md).

---

## 🐋 10. Grafo Estatístico Unificado `NWX-Argon v5.0`: Fluxo Institucional de Opções ("Whale Flow") + Análise Técnica + Fundamentalista (`FMP`/`BRAPI`) + Notícias — Conta TradeStation `*8131`: `PROJ-010-NWX-ARGON-WHALE-OPTIONS` (2026-11-01)
- **Objetivo:** Retornar 100% ao objetivo original do grafo (`NWX-Argon`: previsões puramente estatísticas, sem mercados de apostas), indexar as fontes institucionais de opções (`ICE Data Services / OPRA`, `CBOE LiveVol`, `Unusual Whales`, `SpotGamma GEX`, `ORATS`, `Polygon.io Options` e `TradeStation WebAPI v3`) ao lado das APIs `FMP` e `BRAPI` no GCP da `NWX Invest`, auditar a conta real na **TradeStation (`Entity *8131`: Account Value `US$ 3,828.67`, Cash Available `US$ 2,507.17`, Buying Power `US$ 10,028.68`)** e unir **Notícias em Tempo Real + Análise Fundamentalista + Análise Técnica + Fluxo Baleia em Opções** para encontrar onde os grandes estão colocando o dinheiro.
- **Status:**
  - [x] Indexação das 7 fontes institucionais de opções (`OPT-001` a `OPT-007`) em [referencias_comunidades_canais.json](file:///c:/NWX/nwx-Argon/database/referencias_comunidades_canais.json), [references.db](file:///c:/NWX/nwx-Argon/database/references.db) e [CATALOGO_REFERENCIAS.md](file:///c:/NWX/nwx-Argon/database/CATALOGO_REFERENCIAS.md) (`36` fontes totais).
  - [x] Implementação e execução do motor de auditoria e simulação Monte Carlo (`25.000` trajetórias de piramidação na conta TradeStation `*8131`) em [nwx_argon_whale_options_engine.py](file:///c:/NWX/nwx-Argon/core/nwx_argon_whale_options_engine.py) e [NWX_ARGON_WHALE_OPTIONS_AND_ACCOUNT_AUDIT.json](file:///c:/NWX/nwx-Argon/sandbox/runs/NWX_ARGON_WHALE_OPTIONS_AND_ACCOUNT_AUDIT.json).
  - [x] Implementação e execução do motor unificado (`Técnica + Fundamentalista FMP/BRAPI + Notícias RSS ao vivo + Fluxo Institucional de Opções + Boletas v4.0 com Ghetto Spread Anti-PDT`) em [nwx_argon_unified_options_intelligence.py](file:///c:/NWX/nwx-Argon/core/nwx_argon_unified_options_intelligence.py) e [NWX_ARGON_UNIFIED_OPTIONS_SIGNALS.json](file:///c:/NWX/nwx-Argon/sandbox/runs/NWX_ARGON_UNIFIED_OPTIONS_SIGNALS.json).
  - [x] Dossiê executivo consolidado em [RELATORIO_NWX_ARGON_OPCOES_WHALE_FLOW_E_CONTA_TRADESTATION.md](file:///c:/NWX/nwx-Argon/reports/RELATORIO_NWX_ARGON_OPCOES_WHALE_FLOW_E_CONTA_TRADESTATION.md).





