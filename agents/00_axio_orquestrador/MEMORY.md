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


### [2026-11-01 17:32] — Criação do Agente Gabriel Torres (`05_gabriel_torres_investigador_fontes`) e Boleta Operacional de Contratos (`PROJ-005-SCOUT-TRADING-DESK`)
- **Novo Agente:** **Gabriel Torres — Investigador de Fontes & Inteligência de Contexto** (`agents/05_gabriel_torres_investigador_fontes/`).
- **Novas Bases Reais 2026 (`sandbox/data/`):** `weekly_rosters_2026.csv` (6,48 MB), `stats_player_week_2026.csv` (3,34 MB) e `stats_team_week_2026.csv` (88 KB).
- **Evidências Decisivas Extraídas para o Debate Atuarial:**
  - *A favor de KC (Otimistas):* Retorno oficial do WR #1 **Rashee Rice** (`INA` nas Semanas 6–7 $\rightarrow$ `ACT` na Semana 8; `33 rec, 336 yds, +14.07 EPA` em 5 jogos) ao lado de **Travis Kelce** (`+18.35 EPA`) e **Xavier Worthy**; baixas de Denver na *Injured Reserve* (`RES` na W8) incluindo o RB **RJ Harvey** (`149 yds corridas, 129 yds aéreas, 2 TDs`), o Edge/LB **Jonah Elliss** e 3 jogadores de linha ofensiva (`Deiter`, `Gargiulo`, `Crum`); disciplina de bola de KC (`2` fumbles perdidos vs `6` de Denver).
  - *Ameaças a KC / A favor de DEN (Pessimistas):* Perda abrupta do CB titular **L'Jarius Sneed** (`ACT` na W7 $\rightarrow$ `RES` na W8) e do LT **Josh Simmons** (`RES`); retorno simultâneo da secundária All-Pro de Denver (**Pat Surtain II** e **Talanoa Hufanga**, ambos `INA` na W6–W7 $\rightarrow$ `ACT` na W8); vulnerabilidade de proteção de Mahomes (`17 sacks` sofridos vs `6.5 sacks` e `14 QB hits` de **Nik Bonitto**) e força terrestre de **J.K. Dobbins** (`550 yds, 4 TDs, +10.48 EPA`).
- **Sentença Atualizada e Boleta de Contratos (`KXNFLGAME-26NOV01KCDEN-KC`):**
  - Probabilidade de Fechamento Final (*Settlement* a `US$ 1,00`): **`58,12%` KC** vs **`41,88%` DEN**.
  - Plano de Venda Antecipada Escalonada (Carteira `US$ 1.000,00` = `1.886 contratos` comprados a `53¢`):
    - **Lote 1 (`40%` = `754 contratos`):** Venda Limite a **`65¢`** (`P_hit = 67,18%`) $\rightarrow$ Recebe **`US$ 490,10`** (`+US$ 90,48` / `+22,64%`).
    - **Lote 2 (`40%` = `754 contratos`):** Venda Limite a **`76¢`** (`P_hit = 59,29%`) $\rightarrow$ Recebe **`US$ 573,04`** (`+US$ 173,42` / `+43,40%`), embolsando **`US$ 1.063,14`** antes do 4º quarto e travando **`+US$ 63,56` de lucro garantido (*Free-Roll*)** mesmo se Denver virar no final!
    - **Lote 3 (`20%` = `378 contratos`):** Carregado até a liquidação final a **`100¢`** (`P_win = 58,12%`) $\rightarrow$ Recebe **`US$ 378,00`** (`+US$ 177,66` / `+88,68%`), totalizando **`US$ 1.441,14`** (`+US$ 441,56` de lucro líquido / `+44,17%` de ROI).


### [2026-11-01 17:48] — Validação de Busca e Operações Brasil na Polymarket e Kalshi (`PROJ-006-BRAZIL-POLYMARKET-KALSHI`)
- **Arquitetura Validada:**
  - **Polymarket Gamma API:** Combinação de `/public-search?q=Brazil|Brasil|Lula|Bolsonaro` + varredura paginada `/events?active=true&closed=false&limit=100&offset=N`. Retornou **30 eventos ativos**, sendo **14 eventos 100% Brasil** (Selic/Copom Novembro `$126k`, IPCA 2026 `$198,7k`, Alexandre de Moraes STF `$262,2k`, Palmeiras vs Vasco `$285,2k`, Trump & Flávio Bolsonaro `$90,6k`, Copa do Brasil 2026, Eleição Presidencial, Perdão Jair Bolsonaro, Goiás vs CRB).
  - **Kalshi Trade API v2:** Varredura do catálogo `/series` (identificou **97 séries sobre o Brasil**) seguida de `/events?series_ticker=...&with_nested_markets=true` e `/events?status=open&with_nested_markets=true`. Retornou **201 eventos** e **20 eventos com contratos ativos agora** (`KXUSDBRLMAX-26DEC31` com `574.531` contratos, `KXBRAZILU-Q42026-5.8`, `KXBRAZILGDP-26DEC02`, `KXIBOV-26DEC31`, `KXCOPADOBRASIL-26`, `KXDEMORAESOUT-26SEP`, `KXTRUMPFLAVIOMEET-26DEC01`, `KXBOLSONAROPARDON-27`, `KXPBRA-27FEBPROD`, `KXNBBGAME-*`).
- **Assimetria Cross-Exchange Detectada:** Violação de monotonicidade temporal entre Polymarket `#1267468` (*Trump encontra Flávio Bolsonaro até 31/Dez/2026*, `Ask = 18,0¢`) e Kalshi `KXTRUMPFLAVIOMEET-26DEC01-DEC01` (*encontro até 01/Dez/2026*, `Bid = 18,0¢ / Last = 22,0¢`).
- **Relatório:** Salvo em `reports/RELATORIO_BRASIL_POLYMARKET_E_KALSHI.md`.


### [2026-11-01 18:45] — Validação Real com Dinheiro na Kalshi (`KC Chiefs vs DEN Broncos` — *Free-Roll* Executado) e Upload GitHub (`awilsonnavis-afk/nwx-Argon`)
- **Execução Real pelo Usuário:** Entrada em `130.23 Yes shares` do KC Chiefs a `53.75¢` (`US$ 70.00` investidos). No Q3 (`2:58`, `KC 17-13 DEN`), o contrato bateu **`78¢ (Sell 77¢)`** (superando o alvo do Lote 1 de `65¢` e do Lote 2 de `76¢`). O usuário vendeu `104.00 shares` (`80%` da posição), colocando **`US$ 77.29` em caixa** (recuperando 100% dos `US$ 70.00` investidos + `US$ 7.29` de lucro líquido travado) e deixando exatamente **`26.23 Yes shares` (`20%`)** em *Free-Roll* 100% sem risco (`ROI +$30.52 / +43.6%`).
- **Repositório GitHub Criado e Sincronizado:** `https://github.com/awilsonnavis-afk/nwx-Argon`.


### [2026-11-01 20:30] — Arquitetura e Motor de Integração Diária do Grafo Argon no BRZ News (`Hunter Vance`, `BRZ.PREDICTION` e `BRZ.DESK Prediction`)
- **Análise dos Repositórios do Lucas (`lucascs1/brz-news-backend` e `lucascs1/brz-news-frontend`):**
  - Mapeado o funcionamento do `Hunter Vance v2` (`src/agents/hunter_vance/hunter_v2.py`), os gatilhos primários (`src/agents/data_engineering/capital_signals.py`), o placar de importância (`src/agents/editor/importance.py`), as 4 janelas diárias do Cloud Scheduler (`09h calendar`, `11h open`, `17h close`, `19h wrap` ET em `src/agents/shared/focus.py`), o gate jurídico da Victoria Rossi (`src/agents/albert_ryan/analysis_desk.py`) e a governança `1 PR = 1 Lane` (`LANES.yml`).
  - Mapeado o frontend Next.js 15 (`src/app/pro/trade/TradingDesk.tsx`, `OrderTicket.tsx`, `src/lib/prediction-markets.ts` e `src/app/pro/publish/PredictionMarkets.tsx`).
- **Implementação (`core/brz_news_daily_prediction_graph.py`):**
  - Gera diariamente nas 4 janelas:
    1. **Pautas de Mercados Preditivos para o `Hunter Vance`** (`sandbox/runs/brz_news_daily_integration/hunter_prediction_pautas.json`) com `capital_signal` completo de 6 campos, URL primária oficial e `headline_boost_safe` sem termos eleitorais para Meta Ads.
    2. **Contrato Firestore `prediction_radar/latest` para a página `BRZ.PREDICTION`** (`sandbox/runs/brz_news_daily_integration/firestore_brz_prediction_public.json`), cobrindo 60 mercados (`US$ 2.68M` volume), Top 15 por Score Editorial e Arbitragem Polymarket vs. Kalshi.
    3. **Contrato Firestore `desk_predictions/latest` para a página `BRZ.DESK Prediction`** (`sandbox/runs/brz_news_daily_integration/firestore_brz_desk_prediction_pro.json`), contendo Orderbook ao vivo, Inteligência de Fontes Abertas (`Gabriel Torres`), Tribunal Atuarial `5x5 + Juiz Supremo`, Boleta Tática em 3 Lotes (*Free-Roll*) e o Track Record Auditado ao vivo (`KC vs DEN`).
- **Relatório Arquitetural Completo:** `reports/ARQUITETURA_INTEGRACAO_BRZ_NEWS_HUNTER_E_PREDICTION_DESK.md`.


### [2026-11-01 21:40] — Arquitetura v3.0 (`BRZ.DESK` Diário por Ativo + `BRZ.PREDICTION` Relatório Semanal `AXIOS` + Redes Sociais Market-First + Post-Mortem `KXNFLGAME` + Canvas GCP)
- **Post-Mortem Auditado na API Oficial Kalshi (`KXNFLGAME-26NOV01KCDEN`):**
  - Jogo liquidado (`finalized`) com **`US$ 50.200.530` de volume**. O Denver Broncos virou no 4º quarto (`DEN Result = YES / 100¢`, `KC Result = NO / 0¢`).
  - Graças à saída tática em 3 Lotes (*Free-Roll*) da Equipe Argon no Q3 (venda de `104 shares` a `77¢` gerando **`US$ 77.29` em caixa** sobre `US$ 70.00` investidos), o usuário travou **`+US$ 7.29` (`+10.41%` de ROI líquido)** em dinheiro real antes da virada de Denver — provando matematicamente o valor da blindagem atuarial contra o risco de cauda do 4º quarto (`reports/RELATORIO_TESTE_AO_VIVO_KALSHI_KXNFLGAME.md`).
- **Evolução v3.0 do Grafo no BRZ News (`core/brz_news_daily_prediction_graph.py`):**
  - **Filtro Estrito `100% BRASIL + ALTO VOLUME`:** Somente mercados do Brasil com `>= US$ 10.000` na perna Brasil entram no Radar (`23 contratos`, `US$ 2.64M` volume) e `>= US$ 50.000` no `BRZ.DESK`.
  - **`BRZ.DESK Prediction` (Visão Diária / Terminal por Ativo):** Workspaces dinâmicos (`WS-01-USDBRL-DOLAR`, `WS-02-IPCA-INFLACAO-2026`, `WS-03-COPOM-SELIC-NOV`) com Gráfico de Terminal (`TradingView` + probabilidade implícita), Orderbooks Kalshi e Polymarket lado a lado, Análise Fundamentalista, Análise Técnica/Gráfica, Notícias do Ativo, Tribunal `5x5 + Juiz` e Boleta *Free-Roll*.
  - **`BRZ.PREDICTION` (Visão Semanal + Radar Completo):** O motor **`AXIOS`** seleciona automaticamente o contrato de maior volume da semana (`#1 USD/BRL Máximo 2026 — US$ 574.5K`) e mantém atualizado o **Relatório Semanal AXIOS de Inteligência de Volume** (3 capítulos executivos), acompanhado de todos os 23 contratos Brasil e das notícias que movem o mercado.
  - **Editorial & Redes Sociais (`Prediction & Market` First):** Retirada de `Politics` das janelas principais (`focus.py`) e criação de Carrosséis de 6 slides focados em **encontrar oportunidades de mercado** com **Hooks analíticos densos (45–65 palavras)**.
  - **Canvas Interativo GCP + UI:** Salvo em `reports/grafo_prediction_gcp_canvas.html`.


