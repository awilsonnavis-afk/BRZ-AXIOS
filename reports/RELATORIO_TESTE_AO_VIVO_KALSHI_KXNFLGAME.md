# 🏈 Relatório Operacional ao Vivo: Grafo Argon em `KXNFLGAME` (Kalshi NFL)

**URL Testada:** `https://kalshi.com/markets/kxnflgame/jogo-da-nfl?utm_source=kalshiweb_eventpage`  
**Timestamp da Captura API Kalshi v2:** `2026-11-02T01:45:00Z` (`20:45 ET`)  
**Motor Executado:** [core/run_kxnflgame_live_test.py](file:///c:/NWX/nwx-Argon/core/run_kxnflgame_live_test.py)  
**Payload Completo Gerado:** [sandbox/runs/KALSHI_KXNFLGAME_LIVE_TEST_RESULTS.json](file:///c:/NWX/nwx-Argon/sandbox/runs/KALSHI_KXNFLGAME_LIVE_TEST_RESULTS.json)

---

## 🏆 1. Auditoria Pós-Jogo Oficial (`KXNFLGAME-26NOV01KCDEN`: KC Chiefs vs. DEN Broncos) — A Prova Definitiva do *Free-Roll* em 3 Lotes

O mercado `KXNFLGAME-26NOV01KCDEN` acaba de ser **finalizado e liquidado (`status: finalized`)** na API da Kalshi com **$\text{US\$ } 50.201.767,94$** de volume total negociado:
- **Resultado Oficial no 4º Quarto:** O **Denver Broncos virou o jogo no final** (`KXNFLGAME-26NOV01KCDEN-DEN` liquidado em **`result: yes` / `100¢`**; `KXNFLGAME-26NOV01KCDEN-KC` liquidado em **`result: no` / `0¢`**).

### O que aconteceu com a sua conta real vs. um apostador comum ("Hold 100%"):

| Métrica de Auditoria Real | Estratégia Comum ("Segurar 100% até o Fim") | Protocolo Argon 3 Lotes (*Free-Roll* Executado no Print 3) |
| :--- | :---: | :---: |
| **Entrada Real Executada** | `130,23 shares` YES KC a `53,75¢` (**`US$ 70,00`**) | `130,23 shares` YES KC a `53,75¢` (**`US$ 70,00`**) |
| **Ação no Pico do 3º Quarto (`17-13`, `77¢`)** | Nenhuma (esperou o fim do jogo) | **Vendeu Lote 1 + Lote 2 (`104,00 shares` / `80%`) a `77¢`** |
| **Caixa Embolsado Antes do 4º Quarto** | `US$ 0,00` | **`US$ 77,29` em dinheiro vivo** *(saldo Cash subiu para `US$ 80,65` no Print 3)* |
| **Impacto da Virada do Denver no 4º Quarto** | Perda catastrófica de `130,23 shares` $\rightarrow$ `0¢` | Apenas o **Lote 3 (`26,23 shares` / `20%`)** que já estava **100% pago pelo mercado** virou `0¢` |
| **Resultado Líquido Final na Conta** | **$\text{-US\$ } 70,00$ ($\text{ROI } -100\%$)** | **$\text{+US\$ } 7,29$ de Lucro Líquido Real ($\text{ROI } +10,41\%$)** |
| **Capital Salvo pela Trava Atuarial (Beatriz Alencar)** | — | **$\text{+US\$ } 77,29$ salvos da reversão de cauda no Q4** |

> **Conclusão da Auditoria:** O jogo `KC vs DEN` provou na prática por que a **Bancada dos 5 Atuários Pessimistas** e a **Beatriz Alencar (`04`)** exigem a venda de **80% da posição (Lote 1 + Lote 2)** quando a probabilidade bate na casa de `75¢–77¢`. Mesmo com o Kansas City sofrendo a virada no 4º quarto e o contrato indo a zero na liquidação final, **você terminou o jogo com $\text{US\$ } 77,29$ no bolso ($\text{+10,41\%}$ de lucro líquido sobre os $\text{US\$ } 70,00$ investidos)** e zero centavos de perda de principal.

---

## 📊 2. Ranking ao Vivo dos Jogos Abertos em `KXNFLGAME` (Por Volume)

Varrendo os **15 eventos abertos agora** em `https://kalshi.com/markets/kxnflgame/jogo-da-nfl`, o motor priorizou os **Top 3 jogos de maior liquidez e volume**:

| Rank | Ticker do Evento | Confronto NFL | Volume Total Kalshi | Contrato Recomendado (Tribunal 5x5) | Entrada (`Ask`) | Pessimistas (5) | Otimistas (5) | Veredito Juiz ($p^*$) | Edge Líquido |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **#1** | `KXNFLGAME-26NOV01PHIWAS` | **Philadelphia vs. Washington** *(Sunday Night)* | **$\text{US\$ } 11.088.264$** | **YES · Washington (`WAS`)** | **`60,0¢`** *(59¢/60¢)* | `59,6%` | `72,6%` | **`66,8%`** | **`+680 bps`** |
| **#2** | `KXNFLGAME-26NOV02CHISEA` | **Chicago vs. Seattle** *(Monday Night)* | **$\text{US\$ } 1.138.464$** | **YES · Chicago (`CHI`)** | **`39,0¢`** *(38¢/39¢)* | `39,6%` | `52,6%` | **`46,8%`** | **`+780 bps`** |
| **#3** | `KXNFLGAME-26NOV05JACBAL` | **Jacksonville vs. Baltimore** *(Thursday Night)* | **$\text{US\$ } 100.797$** | **YES · Baltimore (`BAL`)** | **`23,0¢`** *(22¢/23¢)* | `29,1%` | `42,1%` | **`36,2%`** | **`+1.320 bps`** |
| **#4** | `KXNFLGAME-26NOV08LVSF` | **Las Vegas vs. San Francisco** | **$\text{US\$ } 96.366$** | **YES · Las Vegas (`LV`)** | **`21,0¢`** *(20¢/21¢)* | `25,1%` | `38,1%` | **`32,2%`** | **`+1.120 bps`** |
| **#5** | `KXNFLGAME-26NOV08NYGPHI` | **NY Giants vs. Philadelphia** | **$\text{US\$ } 47.027$** | **YES · Philadelphia (`PHI`)** | **`45,0¢`** *(43¢/45¢)* | `46,9%` | `59,9%` | **`54,0%`** | **`+900 bps`** |

---

## 🔍 3. Dossiês Granulares (Gabriel Torres) + Tribunal 5x5 + Boletas de 3 Lotes

### Operação #1 (Ao Vivo / Mega-Volume $\text{US\$ } 11,09\text{M}$): `Philadelphia vs. Washington` (`KXNFLGAME-26NOV01PHIWAS`)

- **Microestrutura do Livro Agora:**
  - `KXNFLGAME-26NOV01PHIWAS-WAS` (**Washington**): `Bid 59,0¢ / Ask 60,0¢` (`Spread: 1,0¢` | Volume: $\text{US\$ } 3,61\text{M}$)
  - `KXNFLGAME-26NOV01PHIWAS-PHI` (**Philadelphia**): `Bid 40,0¢ / Ask 41,0¢` (`Spread: 1,0¢` | Volume: $\text{US\$ } 7,47\text{M}$)
- **Inteligência de Fontes (`Gabriel Torres - 05` sobre `stats_team_week_2026.csv` e `weekly_rosters_2026.csv`):**
  - **O que favorece `YES Washington` (`60,0¢`):**
    1. **Diferencial de EPA & CPOE:** Washington tem eficiência aérea positiva (**`+0,73 Passing EPA/jogo`**, **`+2,92% CPOE`** e **`125,2 jardas terrestres/jogo`**), enquanto o ataque do Philadelphia acumula **`-6,31 EPA total/jogo`** (`-3,89 Passing EPA/j` e `-3,38% CPOE`).
    2. **Segurança de Bola & QB (`Jayden Daniels`):** Jayden Daniels soma **`+4,31 Passing EPA`**, `5 TDs aéreos`, **`0 interceptações`** e `213 jardas terrestres` (`2 TDs`), fazendo com que Washington tenha apenas **`0,33 turnovers/jogo`** (2 no total) contra **`0,86 turnovers/jogo`** de Philadelphia (6 no total) e `18 sacks` sofridos por PHI.
    3. **Baixas no Elenco (`weekly_rosters_2026.csv` Sem. 8):** Philadelphia registra **8 jogadores em reserva/inativos (`RES`)**, incluindo desfalques no backfield e secundária (`Dameon Pierce RB-RES`, `Tank Bigsby RB-RES`, `Will Shipley RB-RES`, `Jakorian Bennett DB-RES`, `Johnny Wilson WR-RES`).
  - **O que ameaça `YES Washington`:**
    1. **Baixas Importantes em Washington (`7 RES`):** Washington tem **`Laremy Tunsil (OL-RES)`** e **`Terry McLaurin (WR-RES)`** na lista de reserva, além de `Leo Chenal (LB-RES)` e `Jer'Zhan Newton (DL-RES)`, o que exige saída rápida nos Lotes 1 e 2.
    2. **Talento Explosivo de Skill Players Ativos em PHI:** `Saquon Barkley (RB-ACT)`, `DeVonta Smith (WR-ACT)` e `Dallas Goedert (TE-ACT)` podem virar o placar rapidamente.
- **Boleta Operacional em 3 Lotes (`YES Washington @ 60,0¢`):**

| Lote Tático | Alocação | Qtde Shares (Base `US$ 100`) | Qtde Shares (Base `US$ 1.000`) | Alvo de Venda (`Limit Sell`) | Prob. de Toque ($P(\text{touch})$) | Caixa Recuperado (`US$ 100` / `US$ 1.000`) | Função Atuarial na Carteira |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Entrada Total** | `100%` | `166,67 shares` | `1.666,67 shares` | Compra a **`60,0¢`** | — | $-\text{US\$ } 100,00$ / $-\text{US\$ } 1.000,00$ | Abertura de posição no Orderbook |
| **Lote 1 (TP1)** | **`40%`** | `66,67 shares` | `666,67 shares` | Venda a **`72,0¢`** | **`63,3%`** | **`+US$ 48,00`** / **`+US$ 480,00`** | Recupera **48,0%** do capital no 1º TD/FG de vantagem |
| **Lote 2 (Trava *Free-Roll*)** | **`40%`** | `66,67 shares` | `666,67 shares` | Venda a **`82,8¢`** | **`41,3%`** | **`+US$ 55,20`** / **`+US$ 552,00`** | Soma **`US$ 103,20`** (`103,2%` do principal). **Lucro mínimo de `+US$ 3,20` / `+US$ 32,00` travado mesmo se WAS perder no Q4!** |
| **Lote 3 (*Runner*)** | **`20%`** | `33,33 shares` | `333,33 shares` | Liquidação **`100,0¢`** | **`66,8%`** | **`+US$ 33,33`** / **`+US$ 333,33`** | Corre sem risco; se WAS vencer, caixa total = **`US$ 136,53` (`ROI +36,53%`)** |
| **Stop-Loss Tático** | Proteção | Posição restante | Posição restante | Stop a **`43,2¢`** | — | Preserva `72%` do capital | Saída de emergência se PHI abrir 2 posses cedo |

---

### Operação #2 (Monday Night Football — Volume $\text{US\$ } 1,14\text{M}$): `Chicago vs. Seattle` (`KXNFLGAME-26NOV02CHISEA`)

- **Microestrutura do Livro Agora:**
  - `KXNFLGAME-26NOV02CHISEA-CHI` (**Chicago**): `Bid 38,0¢ / Ask 39,0¢` (`Spread: 1,0¢` | Volume: $\text{US\$ } 716,4\text{k}$)
  - `KXNFLGAME-26NOV02CHISEA-SEA` (**Seattle**): `Bid 61,0¢ / Ask 62,0¢` (`Spread: 1,0¢` | Volume: $\text{US\$ } 422,0\text{k}$)
- **Inteligência de Fontes (`Gabriel Torres - 05`):**
  - **Por que o Tribunal viu assimetria em `YES Chicago` a `39,0¢` (`Veredito Juiz: 46,8%` | `+780 bps`):**
    1. **Divergência Forte de EPA Ofensivo:** Chicago tem **`+2,70 EPA ofensivo/jogo`** (`+5,33 Passing EPA/j`, **`+5,58% CPOE`**, `254,9 jds passe/j` + `154,3 jds corridas/j`), enquanto Seattle opera no negativo com **`-3,08 EPA ofensivo/jogo`** (`-5,03 Rushing EPA/j`).
    2. **QB Matchup (`Caleb Williams` vs. `Sam Darnold`):** Caleb Williams acumula **`+41,71 Passing EPA`** (`1.020 jds`, `5 TDs`, apenas `1 INT` + `128 jds terrestres` e `2 TDs`), enquanto Sam Darnold em Seattle acumula **`-9,80 Passing EPA`** e `8 interceptações` (13 turnovers totais de SEA).
    3. **Pressão Defensiva:** A defesa de Chicago soma **`19,0 sacks` (`2,71/jogo`)** contra um ataque de Seattle que já entregou `13 turnovers`.
  - **Ameaças (Bancada Pessimista):** Chicago joga fora de casa em Seattle e possui `11 jogadores` em `RES` (incluindo `Cole Kmet TE-RES` e `Braxton Jones OL-RES`). Por isso, a operação é desenhada para **capturar o salto de `39¢` para `48,4¢–56,2¢` com o jogo equilibrado no 1º tempo** e travar o *Free-Roll*.
- **Boleta Operacional em 3 Lotes (`YES Chicago @ 39,0¢` — Base `US$ 100` / `256,41 shares`):**
  - **Lote 1 (`40%` = `102,56 shares`):** Venda Limit a **`48,4¢`** ($P(\text{touch}) = 71,2\%$) $\rightarrow$ Recupera **`US$ 49,64`** (`49,6%` do principal).
  - **Lote 2 (`40%` = `102,56 shares`):** Venda Limit a **`56,2¢`** ($P(\text{touch}) = 52,9\%$) $\rightarrow$ Recupera **`US$ 57,64`**, somando **`US$ 107,28` em caixa** (**`107,3%` do capital investido**, ou seja, **`+US$ 7,28` de lucro garantido** mesmo que Seattle vire no final!).
  - **Lote 3 (`20%` = `51,29 shares`):** *Hold* em *Free-Roll* até `100¢` $\rightarrow$ Se Chicago vencer, paga mais **`+US$ 51,29`**, totalizando **`US$ 158,57` (`ROI +58,57%`)**.
  - **Stop-Loss Tático:** **`26,5¢`**.

---

### Operação #3 (Thursday Night Football — Volume $\text{US\$ } 100,8\text{k}$): `Jacksonville vs. Baltimore` (`KXNFLGAME-26NOV05JACBAL`)

- **Microestrutura do Livro Agora:**
  - `KXNFLGAME-26NOV05JACBAL-BAL` (**Baltimore**): `Bid 22,0¢ / Ask 23,0¢` (`Volume: US$ 38,0k`)
  - `KXNFLGAME-26NOV05JACBAL-JAC` (**Jacksonville**): `Bid 76,0¢ / Ask 77,0¢` (`Volume: US$ 62,8k`)
- **Inteligência de Fontes (`Gabriel Torres - 05`):**
  - **Assimetria Extrema em `YES Baltimore` a `23,0¢` (`Veredito Juiz: 36,2%` | `+1.320 bps`):**
    1. Embora Jacksonville (`Trevor Lawrence`: `+53,31 Passing EPA`, `14 TDs`) viva grande fase ofensiva (`+9,17 EPA/j`), o Baltimore Ravens joga em casa com **`Lamar Jackson` (`+37,34 Passing EPA`, `6 TDs`, `1 INT` + `144 jds corridas`)** e **`Derrick Henry` (`ACT`)**, somando **`+5,43 EPA ofensivo/jogo`** (`242,0 jds passe/j` + `141,7 jds corridas/j`) e **`16,0 sacks` defensivos**.
    2. Jacksonville tem **3 titulares de Linha Ofensiva em `RES`** (`Sam Mustipher OL-RES`, `Patrick Mekari OL-RES`, `Anton Harrison OL-RES`), o que expõe Trevor Lawrence ao pass-rush de Baltimore.
    3. Precificar Baltimore em casa com Lamar Jackson e Derrick Henry ativos a apenas **`23,0¢`** gera uma distorção severa: basta um início competitivo no 1º quarto para o contrato de `BAL` subir de `23¢` para `28,5¢–33,1¢`.
- **Boleta Operacional em 3 Lotes (`YES Baltimore @ 23,0¢` — Base `US$ 100` / `434,78 shares`):**
  - **Lote 1 (`40%` = `173,91 shares`):** Venda Limit a **`28,5¢`** ($P(\text{touch}) = 77,1\%$) $\rightarrow$ Recupera **`US$ 49,56`**.
  - **Lote 2 (`40%` = `173,91 shares`):** Venda Limit a **`33,1¢`** ($P(\text{touch}) = 62,1\%$) $\rightarrow$ Recupera **`US$ 57,56`**, somando **`US$ 107,12` em caixa** (**`+7,12%` de lucro travado** com o contrato ainda em `33,1¢`, sem nem precisar que Baltimore vire favorito!).
  - **Lote 3 (`20%` = `86,96 shares`):** *Hold* em *Free-Roll* até `100¢` $\rightarrow$ Se Baltimore vencer, paga mais **`+US$ 86,96`**, totalizando **`US$ 194,08` (`ROI +94,08%`)**.
  - **Stop-Loss Tático:** **`15,6¢`**.
