# ⚖️ Dossiê Multi-Sandbox & Sentença do Tribunal Atuarial (5 Pessimistas vs. 5 Otimistas + Juiz Supremo)

> **Projeto:** `PROJ-004-MULTI-SANDBOX-TRIBUNAL-KCDEN`  
> **Evento Auditado:** `KXNFLGAME-26NOV01KCDEN` — **Kansas City Chiefs @ Denver Broncos** (01/11/2026)  
> **Orquestrador Líder:** **Axio Vance** — Equipe Argon  
> **Modelo de Validação Judicial:** **Gemini 4 Argon** (3 Subagentes Independentes em Paralelo)  
> **Motor Computacional:** [multi_sandbox_tribunal_engine.py](file:///c:/NWX/nwx-Argon/core/multi_sandbox_tribunal_engine.py)

---

## 📚 1. Expansão das Fontes de Dados Reais (`sandbox/data/` & `database/references.db`)

Para eliminar qualquer ponto cego, ampliamos nossa base para **4 repositórios reais de dados** + **29 referências indexadas** em [references.db](file:///c:/NWX/nwx-Argon/database/references.db):
1. **Base Histórica Oficial da NFL (`nflverse` — [games.csv](file:///c:/NWX/nwx-Argon/sandbox/data/games.csv)):** `7.548` jogos de 1999 a 2026 (`7.391` concluídos), incluindo QBs titulares, treinadores (`Andy Reid` vs. `Sean Payton`), descanso, altitude/estádio e linhas históricas.
2. **Metadados Oficiais das 32 Franquias ([nfl_teams.csv](file:///c:/NWX/nwx-Argon/sandbox/data/nfl_teams.csv)):** Divisões e identificadores padronizados.
3. **Livro de Ofertas Principal Kalshi ([kalshi_kcden_latest.json](file:///c:/NWX/nwx-Argon/sandbox/data/kalshi_kcden_latest.json)):** Mais de **`10,75 milhões` de contratos negociados** (`6,20M` em KC e `4,56M` em DEN), com cotações pré-jogo (`53¢` KC / `48¢` DEN) e em tempo real (`58¢–60¢` KC / `41¢–43¢` DEN).
4. **Curva Completa de 43 Derivativos Kalshi ([kalshi_kcden_spread.json](file:///c:/NWX/nwx-Argon/sandbox/data/kalshi_kcden_spread.json) & [kalshi_kcden_total.json](file:///c:/NWX/nwx-Argon/sandbox/data/kalshi_kcden_total.json)):**
   - **24 Mercados de Spread Alternativo (`KXNFLSPREAD-26NOV01KCDEN-*`):** De `KC -1.5` até `KC -16.5` (`13¢`) e `DEN -1.5` até `DEN -16.5`.
   - **19 Mercados de Total de Pontos (`KXNFLTOTAL-26NOV01KCDEN-*`):** De `Over 20.5` (`99¢`) até `Over 60.5`.

---

## 🧪 2. Os 5 Cenários Executados em Sandboxes Separadas (`sandbox/environments/`)

Cada cenário foi executado em seu próprio diretório e processo isolado (`15.000` simulações de Monte Carlo por sandbox = **`60.000` jogos simulados**):

| Sandbox Isolada | Hipótese / Regime Modelado | $P(\text{Vitória KC})$ | $P(\text{Vitória DEN})$ | IC 95% Epistêmico (KC) | Jogo Decidido por $\le 7$ pts | Vitória por $8+$ pts (KC / DEN) | ROI Esperado KC (@53¢) | Vencedor do Cenário |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **[sandbox_01](file:///c:/NWX/nwx-Argon/sandbox/environments/sandbox_01_historico_altitude/results.json)** | **Histórico & Altitude de Mile High** (`1.609m`, linha `nflverse` `DEN -112` e derrota KC `20-3` p/ SEA na Sem. 7) | `47,54%` | **`52,46%`** | `[41,27% ; 53,81%]` | `42,43%` | `25,38%` / `32,19%` | `-10,30%` | **Denver Broncos** |
| **[sandbox_02](file:///c:/NWX/nwx-Argon/sandbox/environments/sandbox_02_dominancia_mahomes_pitagoras/results.json)** | **Dominância de QB & Saldo Pitagórico 2026** (`Mahomes 1711.4` vs `Nix 1668.2`, Saldo KC `+40` vs DEN `+3`, H2H `13-4` desde 2018 e `KC 31x10` na Sem. 1) | **`58,34%`** | `41,66%` | `[52,85% ; 63,83%]` | `42,38%` | `38,71%` / `18,91%` | **`+10,08%`** | **Kansas City Chiefs** |
| **[sandbox_03](file:///c:/NWX/nwx-Argon/sandbox/environments/sandbox_03_curva_derivativos_kalshi/results.json)** | **Microestrutura de 45 Derivativos Kalshi** (`24` Spreads + `19` Totais + `10,75M` contratos; `KC -7.5` a `24¢` pré / `28¢` live) | **`56,55%`** | `43,45%` | `[51,85% ; 61,25%]` | `44,07%` | `35,09%` / `20,84%` | **`+6,70%`** | **Kansas City Chiefs** |
| **[sandbox_04](file:///c:/NWX/nwx-Argon/sandbox/environments/sandbox_04_stress_trincheiras_divisional/results.json)** | **Guerra de Trincheiras Divisional** (`259` jogos divisionais reais com `Total <= 42.5` pts desde 2018, onde `50,19%` terminam em $\le 7$ pts) | **`51,46%`** | `48,54%` | `[44,60% ; 58,32%]` | **`50,57%`** | `26,06%` / `23,37%` | `-2,91%` | **Kansas City Chiefs** |
| **[sandbox_05](file:///c:/NWX/nwx-Argon/sandbox/environments/sandbox_05_tribunal_10_atuarios_juiz/results.json)** | **Tribunal Atuarial (5 Pessimistas + 5 Otimistas + Juiz Supremo)** | **`53,88%`** | `46,12%` | `[48,60% ; 58,20%]` | `44,86%` | `31,31%` / `23,83%` | **`+1,66%`** (@53¢) | **Kansas City Chiefs (9x1)** |

---

## 🛡️ 3. Bancada dos 5 Atuários Pessimistas (`Média P(KC) = 50,90%`)

Validado pelo Subagente Gemini Argon ([Bancada 5 Atuários Pessimistas](conversation://47bd71f9-780d-48f8-9594-3a5d9f5cc752)):

| Código | Atuário(a) Pessimista | Tese Central de Risco / Solvência | $P(\text{KC})$ | Voto em Campo | Teto Kelly | Voto Financeiro no Contrato Kalshi |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **`PESS-01`** | **Dr. Artur Varella** | **Spread Bid-Ask & Solvência II:** O limite inferior do IC 95% nos Cenários 1 (`41,3%`), 4 (`44,6%`) e Gen 3 (`49,9%`) é menor que o Ask de `53¢`, gerando $\text{CVaR}_{95\%}$ negativo. | `51,20%` | KC Chiefs | `0,00%` | **VETADO (`NO TRADE` a 53¢ e 58¢)** |
| **`PESS-02`** | **Dra. Helena Siqueira** | **Altitude de Mile High (`1.609m`) & Linha Vegas (`DEN -112`):** Casas tradicionais fecharam com `50,43%` limpo para Denver, e KC marcou apenas 3 pts na Semana 7 (`20-3` vs SEA). | `48,60%` | **DEN Broncos** | `0,00%` | **VETADO EM KC** |
| **`PESS-03`** | **Dr. Marcos Fontes** | **Compressão Divisional de Baixo Total (`41.5 pts`):** Em 259 jogos divisionais reais $\le 42,5$ pts, **`50,19%`** terminam decididos por $\le 7$ pts (um único *turnover* decide). | `50,80%` | KC Chiefs | `0,50%` | **VETADO (Variância de 1 posse)** |
| **`PESS-04`** | **Dra. Lívia Capanema** | **Encolhimento de James-Stein (`n = 6` jogos):** O saldo de `+40` pts de KC em 2026 tem amostra curta e exige *shrinkage* de 50% em direção ao prior de mercado. | `51,50%` | KC Chiefs | `0,50%` | **CAUTELA MÁXIMA ($\le 0,5\%$ da banca)** |
| **`PESS-05`** | **Dr. Renato Albuquerque** | **Seleção Adversa In-Play (`58¢–60¢`):** Entrar ao vivo a `58¢+` transfere riqueza para robôs de baixa latência ($\text{ROI esperado} = -9,66\%$). | `52,40%` | KC Chiefs | `0,00%` | **VETADO AO VIVO (`58¢–60¢`)** |

---

## 🚀 4. Bancada dos 5 Atuários Otimistas (`Média P(KC) = 56,30%`)

Validado pelo Subagente Gemini Argon ([Bancada 5 Atuários Otimistas](conversation://a40ea5a4-57fb-4275-8d2f-e0ceac03ce48)):

| Código | Atuário(a) Otimista | Tese Central de Valor / Assimetria | $P(\text{KC})$ | Voto em Campo | Alocação Kelly | Voto Financeiro no Contrato Kalshi |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **`OTIM-01`** | **Dra. Camila Vasconcelos** | **Prêmio de `QB_Elo` & Hegemonia Histórica:** `Mahomes (1711.4)` vs `Nix (1668.2)` e `Oladokun (1481.0)`. Desde 2018, KC venceu **`13 de 17` (`76,47%`)** contra DEN e **`5 de 7` (`71,43%`)** em Denver! | **`58,20%`** | **KC Chiefs** | `3,50%` | **APROVADO (`YES KC` @ 53¢ / Hold)** |
| **`OTIM-02`** | **Dr. Eduardo Bastos** | **Descolamento Pitagórico (`+40` vs `+3`) & `31-10`:** DEN é um "falso 5-2" (`144 PF / 141 PA`, Pitágoras `50,9%`), enquanto KC (`5-1`) tem `143 PF / 103 PA` (`62,3%`) e venceu DEN por **`31-10`** na Sem. 1. | **`56,90%`** | **KC Chiefs** | `3,00%` | **APROVADO (`YES KC` @ 53¢)** |
| **`OTIM-03`** | **Dra. Fernanda Prado** | **Smart Money Institucional na Kalshi (`10,75M` contratos):** O fluxo real (`6,20M` contratos em KC) corrigiu a linha estática antiga já no pré-jogo (`53¢` vs `48¢`) e puxou para `58¢–60¢`. | **`56,10%`** | **KC Chiefs** | `2,50%` | **APROVADO (Seguir Fluxo Institucional)** |
| **`OTIM-04`** | **Dr. Gustavo Meirelles** | **Assimetria na Curva de 24 Spreads (`KXNFLSPREAD`):** O strike `KC -7.5` (`KC8` a `24¢` pré / `28¢` live) mostra cauda direita espessa (`38,7%` de chance de vitória por 8+ pts no Cenário 2). | **`55,80%`** | **KC Chiefs** | `2,50%` | **APROVADO (`KC Moneyline` + `KC -7.5`)** |
| **`OTIM-05`** | **Dra. Beatriz Alencar** | **Prova Empírica em 398 Jogos Reais (2025–2026):** O modelo `Gen 2` elevou a acurácia fora da amostra para **`64,82%`** (Brier `0,2225`), validando o favoritismo de KC com trava prudencial. | **`54,50%`** | **KC Chiefs** | `1,50%` | **APROVADO COM TRAVA (Até `53,5¢` pré)** |

---

## ⚖️ 5. Sentença Final Irrecorrível do Juiz Supremo (`Dr. Salomão Valente`)

Validado pelo Subagente Gemini Argon ([Juiz Supremo do Tribunal Atuarial](conversation://2d10eb84-dc14-4eff-a87a-37605a3c86a3)):

1. **Agregação Supra-Bayesiana (Ponderação em Log-Odds):**
   - Média das 4 Sandboxes (`60.000` simulações): **`53,47%`**
   - Média da Bancada dos 5 Atuários Pessimistas: **`50,90%`**
   - Média da Bancada dos 5 Atuários Otimistas: **`56,30%`**
   - **Probabilidade Consolidada Final do Juiz Supremo:** **`53,88%` para o Kansas City Chiefs** vs. **`46,12%` para o Denver Broncos** (Intervalo de Credibilidade de 95% do Tribunal: **`[48,60% ; 58,20%]`**).

2. **VEREDITO 1 — QUEM VAI GANHAR O JOGO NO CAMPO?**
   - 🏆 **KANSAS CITY CHIEFS (Por 9 votos a 1 no Tribunal Atuarial e `53,88%` de probabilidade consolidada).**
   - **Por quê:** Mesmo os Atuários Pessimistas (`PESS-01`, `PESS-03`, `PESS-04` e `PESS-05`) reconhecem que, ao expurgar os QBs reservas de 2025 (`Chris Oladokun`), **Patrick Mahomes (`QB_Elo 1711.4`, `71,43%` de vitórias na altitude de Denver e `31-10` sobre Bo Nix na Semana 1)** é o favorito legítimo para vencer a partida.

3. **VEREDITO 2 — QUAL A DECISÃO FINANCEIRA CORRETA NA KALSHI?**
   - **No Preço Pré-Jogo (`53¢`):** **APROVADA ENTRADA TÁTICA CONSERVADORA DE `1,0%` DA BANCA (`US$ 10,00` para banca de `US$ 1.000,00`) EM `YES KC` ATÉ O TETO DE `53¢`**, mantendo **`99,0%` do capital blindado em Reserva Técnica**, conciliando o *Edge* positivo apontado pela Bancada Otimista (`56,30%`) com a trava de variância de jogos divisionais imposta pela Bancada Pessimista (`50,90%`).
   - **No Preço Ao Vivo (`58¢ a 60¢`):** **BLOQUEIO UNÂNIME DE NOVA COMPRA (`HOLD` / `NO NEW ENTRY`).** A `58¢–60¢`, o mercado já andou a favor da nossa previsão e ultrapassou o valor justo pré-jogo (`53,88¢`), dando razão à Bancada Pessimista contra comprar topo em andamento. Quem entrou a `52¢–53¢` mantém a posição ou realiza lucro parcial.
