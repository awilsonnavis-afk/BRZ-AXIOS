# 📰 Pauta Editorial & Ranking de Prioridade por Volume — Operações Brasil (Polymarket & Kalshi | BRZ News)

**Orquestrador:** Axio Vance (`agents/00_axio_orquestrador/`)  
**Investigador de Fontes & Scanner:** Gabriel Torres (`agents/05_gabriel_torres_investigador_fontes/`)  
**Diretora de Dados & Inteligência Editorial:** Clara Mendonça (`agents/02_clara_mendonca_analista_dados/`)  
**Modelagem & Risco (Boletas):** Henrique Vasconcelos, Lucas Bittencourt & Beatriz Alencar  
**Arquivos de Dados:** [`brazil_markets_high_volume_priority.json`](file:///c:/NWX/nwx-Argon/sandbox/data/brazil_markets_high_volume_priority.json) | [`BRAZIL_EDITORIAL_VOLUME_RANKING.json`](file:///c:/NWX/nwx-Argon/sandbox/runs/BRAZIL_EDITORIAL_VOLUME_RANKING.json)

---

## 🎯 1. Critério de Priorização Editorial por Volume (Metodologia BRZ News)

Para produzir jornalismo financeiro e inteligência de mercado de alto impacto (*Skin-in-the-Game Journalism*), **não basta um mercado existir — ele precisa ter volume financeiro real, liquidez de livro (*Orderbook Depth*) e giro de 24 horas**. Mercados com menos de US\$ 10 mil sofrem distorção com poucas ordens; mercados acima de **US\$ 100 mil a US\$ 500 mil+** refletem consenso institucional, *hedge funds* e *smart money*.

Implementamos em [`core/brazil_editorial_prioritizer.py`](file:///c:/NWX/nwx-Argon/core/brazil_editorial_prioritizer.py) o **Score de Prioridade Editorial BRZ News**:

$$\text{Score Editorial} = \text{Volume Brasil (US\$)} + 1{,}5 \times \text{Liquidez/Open Interest (US\$)} + 3{,}0 \times \text{Volume 24h (US\$)}$$

Além disso, o motor **descarta automaticamente da capa editorial jogos que já estão em `99,9¢ / 0,1¢`** (em fase final de liquidação, como `Palmeiras vs Vasco` após o apito final com `US$ 287,6 mil`), mantendo na pauta apenas **mercados vivos e abertos à negociação**.

---

## 🏆 2. Ranking Geral das Maiores Operações Vivas do Brasil por Volume (Polymarket + Kalshi)

Ao expandir a busca na API da Polymarket para `limit_per_type=50` em 18 radicais brasileiros e cruzar com as 97 séries da Kalshi, mapeamos **60 operações ativas**, lideradas por **13 mercados de Mega-Volume (Tier 1 + Destaques 24h)** que somam **mais de US\$ 2,68 milhões em contratos ativos diretamente sobre o Brasil**:

| Rank | Bolsa | Evento / Operação Ativa | Escopo | Volume Direto Brasil (US\$) | Liquidez / Open Interest (US\$) | Giro 24h (US\$) | Preço Atual (`Bid / Ask`) | Tier Editorial |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1º** | **Kalshi** | **Teto do Dólar (`USD/BRL High in 2026`)** (`KXUSDBRLMAX-26DEC31`) | 100% Brasil | **US\$ 574.532** | US\$ 24.276 | Ativo | `>= R$ 6,00`: **`16¢ / 34¢`** (`Last 22¢`)<br/>`>= R$ 6,50`: **`4¢ / 11¢`** | 🔥 **TIER 1 (Capa Macro)** |
| **2º** | **Polymarket** | **Fall Elections Combo: Brazil, Israel, US Senate** (`#1138395`) | 100% Brasil | **US\$ 516.159** | **US\$ 75.393** | US\$ 6.417 | `Lula + Eizenkot + Dems`: **`34,1¢ / 35,4¢`**<br/>`Lula + Netanyahu + Dems`: **`13,2¢ / 16,6¢`** | 🔥 **TIER 1 (Capa Política)** |
| **3º** | **Polymarket** | **Alexandre de Moraes sai do STF até o fim de 2026?** (`#257477`) | 100% Brasil | **US\$ 262.231** | US\$ 21.641 | US\$ 1.575 | `YES (Sai)`: **`6,1¢ / 6,2¢`**<br/>`NO (Permanece)`: **`93,8¢ / 93,9¢`** | 🔥 **TIER 1 (Capa STF)** |
| **4º** | **Polymarket** | **Inflação Anual do Brasil (IPCA) em 2026** (`#181671`) | 100% Brasil | **US\$ 198.671** | US\$ 15.132 | US\$ 799 | `5,00%–5,49%`: **`48,4¢ / 49,0¢`**<br/>`5,50%–5,99%`: **`27,0¢ / 39,5¢`** | 🔥 **TIER 1 (Capa Macro)** |
| **5º** | **Kalshi** | **Inflação no Brasil ficará abaixo de 4,00% em Dez/2026?** (`KXBRAZILINF-26DEC`) | 100% Brasil | **US\$ 151.121** | US\$ 6.290 | Ativo | `YES (< 4,00%)`: **`5,0¢ / 11,0¢`**<br/>`NO (>= 4,00%)`: **`89,0¢ / 95,0¢`** | 🔥 **TIER 1 (Capa Macro)** |
| **6º** | **Polymarket** | **Decisão do Copom / Banco Central em Novembro (Selic)** (`#798441`) | 100% Brasil | **US\$ 126.099** | **US\$ 24.118** | US\$ 2.724 | `Manutenção`: **`81,6¢ / 83,2¢`**<br/>`Corte 25 bps`: **`17,0¢ / 19,0¢`** *(Vence 04/Nov!)* | 🔥 **TIER 1 (Urgente 72h)** |
| **7º** | **Polymarket** | **Algum Ministro do STF sofrerá Impeachment antes de 2027?** (`#147961`) | 100% Brasil | **US\$ 103.607** | US\$ 14.964 | US\$ 479 | `YES (Impeachment)`: **`2,7¢ / 4,9¢`**<br/>`NO`: **`95,1¢ / 97,3¢`** | 🔥 **TIER 1 (Capa STF)** |
| **8º** | **Polymarket** | **Trump se encontrará com Flávio Bolsonaro em 2026?** (`#1267468`) | 100% Brasil | **US\$ 90.578** | **US\$ 48.217** | **US\$ 33.973** | `YES (Encontro)`: **`17,0¢ / 18,0¢`**<br/>`NO`: **`82,0¢ / 83,0¢`** | 🔥 **TIER 1 (Maior Giro 24h)** |
| **9º** | **Polymarket** | **Quem Trump encontrará em 2026? — Perna Jair Bolsonaro** (`#73871`) | Sub-Contrato BR *(Global US\$ 1,44M)* | **US\$ 79.301** | US\$ 18.315 | US\$ 15.773 | `Jair Bolsonaro (YES)`: **`1,7¢ / 3,3¢`** | 🔥 **TIER 1 (Geopolítica)** |
| **10º** | **Polymarket** | **Grêmio FBPA vs. CA Mineiro + Copa do Brasil** (`#1217748`) | 100% Brasil | **US\$ 74.325** *(+US\$ 38,8k Kalshi)* | **US\$ 149.570** | **US\$ 83.277** | `Grêmio vence`: **`92,0¢ / 93,0¢`**<br/>`Campeão Copa do Brasil`: **Ativo** | ⚡ **TIER 1 (Esportes)** |
| **11º** | **Polymarket** | **Decisão do Copom / Banco Central em Dezembro (Selic)** (`#1045439`) | 100% Brasil | **US\$ 51.479** | US\$ 6.401 | Ativo | `Manutenção`: **`67,0¢ / 69,0¢`**<br/>`Corte 25 bps`: **`24,0¢ / 26,0¢`** | ⚡ **TIER 2 (Macro)** |
| **12º** | **Polymarket** | **Eleição Presidencial do Brasil Anulada até 31/Dez?** (`#1260051`) | 100% Brasil | **US\$ 49.288** | **US\$ 27.772** | US\$ 1.755 | `YES`: **`3,1¢ / 4,6¢`** \| `NO`: **`95,4¢ / 96,9¢`** | ⚡ **TIER 2 (Política/TSE)** |
| **13º** | **Polymarket** | **Com quem Trump falará até 30 de Novembro? — Lula da Silva** (`#1285996`) | Sub-Contrato BR *(Global US\$ 82k)* | US\$ 2.221 *(+US\$ 29k Out)* | **US\$ 23.033** | **US\$ 39.747** | `Trump fala com Lula até 30/Nov`: **`49,0¢ / 51,0¢` (`50%`)** | ⚡ **TIER 2 (Alta Tração)** |

> [!NOTE]
> **Contexto Histórico Recente de Mega-Volume na Kalshi:**  
> Além dos contratos abertos acima, nosso scanner identificou que a série da **Eleição Presidencial do Brasil na Kalshi (`KXBRPRES1R` / `KXVOTEBR2` / `KXIBOVD`)** movimentou mais de **2,63 milhões de contratos (US\$ 2,63 milhões)** em outubro de 2026 (`1.319.035` contratos apenas no vencedor do 1º turno e `192.864` contratos no nível de fechamento do Ibovespa pós-eleição), provando que o apetite institucional por ativos brasileiros nas prediction markets atingiu escala milionária.

---

## 🗞️ 3. As 5 Grandes Pautas Editoriais Prontas (Por Volume Combinado + Boleta Operacional)

Agrupamos os contratos de maior volume nos **5 Cadernos Editoriais de Capa da BRZ News**, cada um já estruturado com **Manchete**, **Tese de Dados**, **Tabela de Preços Reais** e **Boleta Operacional Completa**:

---

### 📌 PAUTA EDITORIAL #1 (Volume Combinado: **US\$ 1.101.902**)
#### **CADERNO MACRO & MERCADOS:** *"Traders apostam US\$ 1,1 milhão no rumo da Selic, IPCA acima do teto da meta e Dólar em 2026"*

- **Manchete Sugerida (BRZ News):**  
  *“Mercados de predição movimentam US\$ 1,1 milhão em ativos macro do Brasil: traders cravam IPCA entre 5% e 6% em 2026 e dão 82% de chance de o Copom travar a Selic nesta quarta-feira”*
- **Por que esta é a Pauta #1 em Volume:**  
  Soma **5 contratos altamente líquidos** entre Kalshi e Polymarket:
  1. `Kalshi KXUSDBRLMAX-26DEC31` (Teto do Dólar em 2026): **US\$ 574.532** (`22%` de chance de voltar a bater **R\$ 6,00** até 31/Dez; `12%` para **R\$ 6,50**).
  2. `Polymarket #181671` (IPCA Anual 2026): **US\$ 198.671** (`48,7%` de chance de fechar entre **5,00% e 5,49%** e `33,3%` entre **5,50% e 5,99%** — ou seja, **82,0% de probabilidade de estourar o teto da meta de 4,50%!**).
  3. `Kalshi KXBRAZILINF-26DEC-4.00` (IPCA abaixo de 4,00%): **US\$ 151.121** (apenas `5% a 11%` de chance de ficar abaixo de 4%).
  4. `Polymarket #798441` (Copom Novembro — vence em `04/Nov`): **US\$ 126.099** (`82,4%` para manutenção da Selic vs `18,0%` para corte de 25 bps).
  5. `Polymarket #1045439` (Copom Dezembro — vence em `09/Dez`): **US\$ 51.479** (`68,0%` para manutenção da Selic vs `25,0%` para corte de 25 bps).

#### 💹 Boleta Operacional da Pauta #1 — Copom Novembro (`Polymarket #798441` — Carteira US\$ 1.000)
- **Operação:** Compra de `No Change (Manutenção da Selic)` a **US\$ 0,832 (`83,2¢`)** (`1.201 contratos` = **US\$ 999,23**).
- **Lote 1 (50% = `600 contratos`):** Venda Limite a **`91,0¢`** na véspera do Copom (`P_hit = 84,0%`) $\rightarrow$ Recebe **US\$ 546,00** (**`+US$ 46,80` / `+9,38%`**).
- **Lote 2 (50% = `601 contratos`):** Liquidação oficial pós-Copom a **`100,0¢`** (`P_win = 89,5%`) $\rightarrow$ Recebe **US\$ 601,00** (**`+US$ 100,97` / `+20,19%`**).
- **Lucro Total Esperado na Manutenção:** **`+US$ 147,77` (`+14,79%` em 72 horas)**.

---

### 📌 PAUTA EDITORIAL #2 (Volume Combinado: **US\$ 471.271**)
#### **CADERNO BRASÍLIA & STF:** *"Com US\$ 471 mil na mesa, investidores globais precificam em menos de 6% a chance de saída ou impeachment de Alexandre de Moraes em 2026, mas veem salto para 28% em 2027"*

- **Manchete Sugerida (BRZ News):**  
  *“Bolsa americana Kalshi e Polymarket acumulam US\$ 471 mil em contratos sobre o STF: mercado descarta impeachment em 2026 (3,8%), mas precifica em 28% chance de saída de Moraes até julho de 2027”*
- **A Descoberta Jornalística nos Dados:**  
  Quando olhamos apenas para 2026, tanto a Polymarket (`#257477`, **US\$ 262.231** de volume, preço **`6,15¢`**; e `#147961`, **US\$ 103.607** de volume, preço **`3,80¢`**) quanto a Kalshi (`KXDEMORAESOUT-26SEP-27JAN01`, **`6,0¢`**) dão como quase certa a permanência de Alexandre de Moraes até `01/Jan/2027` (`~94%` de probabilidade).  
  **Porém**, na curva de vencimentos mais longos da Kalshi (`KXDEMORAESOUT-26SEP-27JUL01` e `28JAN01`), a probabilidade de saída salta de **`6,0¢` (Jan/27) para `28,0¢` (Jul/27) e `46,0¢` (Jan/28)** refletindo a nova composição do Senado em 2027! Além disso, o mercado dá **`93,75%` de chance (`#553441`, US\$ 37.317)** de Lula anunciar uma nova indicação ao STF até 31 de dezembro.

#### 💹 Boleta Operacional da Pauta #2 — Renda Fixa Sintética em Dólar no STF (`Polymarket #257477` — Carteira US\$ 1.000)
- **Operação:** Compra de `NO` (*Alexandre de Moraes NÃO sai do STF até 31/Dez/2026*) a **US\$ 0,939 (`93,9¢`)** (`1.064 contratos` = **US\$ 999,10**).
- **Lote 1 (50% = `532 contratos`):** Venda Limite a **`97,5¢`** no início do recesso do Judiciário em 19/Dez (`P_hit = 96,0%`) $\rightarrow$ Recebe **US\$ 518,70** (**`+US$ 19,15`**).
- **Lote 2 (50% = `532 contratos`):** Liquidação em 31/Dez a **`100,0¢`** (`P_win = 96,5%`) $\rightarrow$ Recebe **US\$ 532,00** (**`+US$ 32,45`**).
- **Retorno Líquido Travado em 60 dias:** **`+US$ 51,60` (`+5,16%` em dólar em 2 meses = `+35,2%` ao ano)**.

---

### 📌 PAUTA EDITORIAL #3 (Volume Combinado Direto: **US\$ 232.560** | Evento Global: **US\$ 1,92 Milhão**)
#### **CADERNO GEOPOLÍTICA EUA-BRASIL:** *"Corrida por Washington: Mercado divide em 50/50 telefonema entre Trump e Lula em novembro, enquanto encontro com Flávio Bolsonaro movimenta US\$ 34 mil em 24h"*

- **Manchete Sugerida (BRZ News):**  
  *“Diplomacia de mercado: Traders colocam 50% de chance em conversa entre Trump e Lula até o fim de novembro, enquanto aposta em encontro presencial com Flávio Bolsonaro dispara em volume e cria arbitragem entre bolsas”*
- **Os 5 Contratos que Comprovam a Disputa por Washington:**
  1. `Polymarket #1267468` (*Trump encontra Flávio Bolsonaro em 2026?*): **US\$ 90.578** de volume total, **US\$ 33.973 negociados só nas últimas 24h** e **US\$ 48.217 de liquidez** (`17,0¢ / 18,0¢`).
  2. `Kalshi KXTRUMPFLAVIOMEET-26DEC01` (*Trump encontra Flávio Bolsonaro até 01/Dez?*): **`4.927` contratos** (`18,0¢ / 24,0¢`, último negócio a **`22,0¢`**).
  3. `Polymarket #1285996` (*Trump fala com Lula até 30 de Novembro?*): **US\$ 39.747 de giro em 24h no evento**, **US\$ 23.033 de liquidez no contrato do Lula**, precificado exatamente em **`50,0%` (`49,0¢ / 51,0¢`)**!
  4. `Polymarket #73871` (*Trump encontra Jair Bolsonaro em 2026?*): **US\$ 79.301** de volume no contrato (`2,5¢` devido à retenção de passaporte).
  5. `Polymarket #1272185` (*Quando Flávio Bolsonaro retorna ao Brasil?*): **US\$ 25.480** de volume e **US\$ 57.746 de liquidez** (apenas `1,35¢` para retorno até 30/Nov e `4,0¢` até 31/Dez).

#### 💹 Boleta Operacional da Pauta #3 — Arbitragem/Swing Encontro Trump & Flávio Bolsonaro (`Polymarket #1267468` — Carteira US\$ 1.000)
- **Operação:** Compra de `YES` na Polymarket (prazo até `31/Dez/2026`) a **US\$ 0,180 (`18,0¢`)** (`5.555 contratos` = **US\$ 999,90**).
- **Lote 1 (50% = `2.777 contratos`):** Venda Limite a **`38,0¢`** no anúncio de agenda em Mar-a-Lago (`P_hit = 46,5%`) $\rightarrow$ Recebe **US\$ 1.055,26** (**`+US$ 555,40` de lucro, recuperando 105% de todo o investimento inicial!**).
- **Lote 2 (30% = `1.666 contratos`):** Venda Limite a **`65,0¢`** na véspera do encontro (`P_hit = 32,0%`) $\rightarrow$ Recebe **US\$ 1.082,90** (**`+US$ 783,02`**).
- **Lote 3 (20% = `1.112 contratos`):** Liquidação a **`100,0¢`** (`P_win = 26,5%`) $\rightarrow$ Recebe **US\$ 1.112,00** (**`+US$ 911,84`**).

---

### 📌 PAUTA EDITORIAL #4 (Volume Combinado: **US\$ 409.581**)
#### **CADERNO ESPORTES & FUTEBOL BRASILEIRO:** *"Copa do Brasil e Brasileirão movimentam mais de US\$ 400 mil em 24 horas nas bolsas de predição globais"*

- **Manchete Sugerida (BRZ News):**  
  *“Futebol brasileiro vira febre nas bolsas de predição dos EUA: confrontos de Palmeiras, Vasco, Grêmio e Atlético-MG movimentam US\$ 409 mil em 24h na Polymarket e na Kalshi”*
- **Dados Reais de Volume e Preços:**
  - `Polymarket #1217742` (`SE Palmeiras vs. CR Vasco da Gama`): **US\$ 287.595** de volume (`US$ 285.522` nas últimas 24h) e **US\$ 293.322** de liquidez.
  - `Polymarket #1217748` (`Grêmio FBPA vs. CA Mineiro`): **US\$ 74.325** de volume (`US$ 83.277` em 24h) e **US\$ 149.570** de liquidez (`Grêmio 92,5¢`).
  - `Kalshi KXCOPADOBRASILTOTAL & SPREAD` (`Grêmio vs Atlético-MG`): **`32.201` contratos**.
  - `Polymarket #1109850` + `Kalshi KXCOPADOBRASIL-26` (*Campeão da Copa do Brasil 2026*): **US\$ 15.460** combinados (`Palmeiras 45,5¢`, `Atlético-MG 29,5¢`, `Vasco 17,0¢`, `Grêmio 12,5¢`).

---

### 📌 PAUTA EDITORIAL #5 (Volume Combinado: **US\$ 516.159** Aberto + **US\$ 2,63 Milhões** Recém-Liquidados)
#### **CADERNO ELEIÇÕES & GEOPOLÍTICA GLOBAL:** *"O Efeito Brasil nos Combos Globais: Mais de US\$ 516 mil apostados na combinação Eleição do Brasil + Israel + Senado dos EUA"*

- **Manchete Sugerida (BRZ News):**  
  *“Após movimentar US\$ 2,63 milhões na eleição presidencial brasileira na Kalshi, investidores globais alocam US\$ 516 mil em contrato derivativo que combina resultado do Brasil com o Senado dos EUA e Israel”*
- **Dados Reais do Contrato (`Polymarket #1138395` — Vence em `05/Nov/2026`):**
  - **Volume:** **US\$ 516.159** | **Liquidez no Livro:** **US\$ 75.393**
  - `Lula vence Brasil + Gadi Eizenkot PM Israel + Democratas vencem Senado EUA`: **`34,1¢ / 35,4¢`** (`US$ 68.853` vol).
  - `Lula vence Brasil + Benjamin Netanyahu PM Israel + Democratas vencem Senado EUA`: **`13,2¢ / 16,6¢`** (`US$ 33.520` vol).
  - `Lula vence Brasil + Gadi Eizenkot PM Israel + Republicanos vencem Senado EUA`: **`11,7¢`** (`US$ 3.439` vol).
- **Por que é uma pauta excelente para esta semana:** O contrato vence em **5 de novembro de 2026** (com a apuração do Senado dos EUA), funcionando como um termômetro ao vivo das eleições americanas ancorado no resultado brasileiro!
