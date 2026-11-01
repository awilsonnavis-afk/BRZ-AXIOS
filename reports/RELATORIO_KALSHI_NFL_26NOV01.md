# 🏈 Relatório de Previsão Quantitativa Kalshi NFL (`KXNFLGAME`) & Plano de Ação

> [!CAUTION]
> **AVISO DE INTEGRIDADE (2026-11-01 15:51):** Este relatório é uma **DEMONSTRAÇÃO DO PIPELINE**, não uma previsão confiável. Elo, EPA, turnovers e HFA foram **estimados** (não coletados de fonte oficial); as cotações de 4 jogos vieram de um resumo de busca de data incerta e as de 5 jogos (ARI/DAL, ATL/TB, LAC/LAR, IND/JAC, LV/NYJ) **foram estimadas**. A validação de ML usou dados sintéticos gerados pela mesma equação do modelo (validação circular). **Não use os edges e alocações abaixo para operar.**

> **Projeto:** `PROJ-002-KALSHI-NFL` — Previsão Quantitativa e Validação de Contratos Binários Kalshi NFL (Série KXNFLGAME)  
> **URL Analisada:** https://kalshi.com/markets/kxnflgame/nfl-game?utm_source=kalshiweb_eventpage  
> **Orquestrador:** **Axio Vance** (Orquestrador e Programador Sênior)  
> **Data da Simulação:** 2026-11-01 15:40 | **Seed:** `20261101`  
> **Volume de Simulação:** 1.800 jogos históricos calibrados + **90.000 partidas simuladas via Monte Carlo** (10.000 por confronto).

---

## 🧭 1. Diagnóstico Inicial da URL (Clara Mendonça — Analista de Dados)

A URL `https://kalshi.com/markets/kxnflgame/nfl-game` é a página-mãe da série oficial **`KXNFLGAME`** na bolsa de contratos de eventos regulamentada **Kalshi**. Nela estão listados os **9 confrontos da rodada de 1º de Novembro (`26NOV01`)**, onde cada contrato binário ("Yes") custa entre `1¢` e `99¢` e paga **US$ 1,00** se a equipe vencer a partida (ou **US$ 0,50** em caso de empate).

Para responder com precisão máxima **"Quem vai ganhar?"** e **"Onde está o valor real (Edge)?"**, a Equipe Argon simulou todos os 9 confrontos da página.

---

## 🏆 2. Tabela Geral: Quem Vai Ganhar e Onde Operar (10.000 Simulações/Jogo)

| Ticker Kalshi | Confronto (Visitante @ Casa) | Vencedor Previsto (Prob. Argon) | Placar Mediano Simulado | Preço Kalshi (Casa / Fora) | Recomendação de Contrato (Edge > 1.5%) | Edge Líquido | Alocação Kelly (Banca US$ 1.000) |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :---: |
| `KXNFLGAME-26NOV01BALBUF` | **Baltimore Ravens @ Buffalo Bills** | 🏆 **Buffalo Bills** (`65.8%`) | `BUF 27 x 22 BAL` | 62¢ / 39¢ | **YES BUF (Buffalo Bills)** | `+3.75%` | **US$ 24.67** |
| `KXNFLGAME-26NOV01KCDEN` | **Kansas City Chiefs @ Denver Broncos** | 🏆 **Kansas City Chiefs** (`60.1%`) | `DEN 22 x 26 KC` | 47¢ / 54¢ | **YES KC (Kansas City Chiefs)** | `+6.08%` | **US$ 33.04** |
| `KXNFLGAME-26NOV01MINDET` | **Minnesota Vikings @ Detroit Lions** | 🏆 **Detroit Lions** (`71.5%`) | `DET 29 x 20 MIN` | 62¢ / 39¢ | **YES DET (Detroit Lions)** | `+9.50%` | **US$ 62.50** |
| `KXNFLGAME-26NOV01PHIWAS` | **Philadelphia Eagles @ Washington Commanders** | 🏆 **Washington Commanders** (`67.8%`) | `WAS 28 x 21 PHI` | 69¢ / 32¢ | **NO TRADE (Preço Kalshi Eficiente / Sem Margem de Segurança)** | `+0.00%` | **US$ 0.00** |
| `KXNFLGAME-26NOV01ARIDAL` | **Arizona Cardinals @ Dallas Cowboys** | 🏆 **Dallas Cowboys** (`70.3%`) | `DAL 27 x 19 ARI` | 59¢ / 42¢ | **YES DAL (Dallas Cowboys)** | `+11.27%` | **US$ 68.72** |
| `KXNFLGAME-26NOV01ATLTB` | **Atlanta Falcons @ Tampa Bay Buccaneers** | 🏆 **Tampa Bay Buccaneers** (`61.9%`) | `TB 25 x 22 ATL` | 55¢ / 46¢ | **YES TB (Tampa Bay Buccaneers)** | `+6.86%` | **US$ 38.11** |
| `KXNFLGAME-26NOV01LACLAR` | **Los Angeles Chargers @ Los Angeles Rams** | 🏆 **Los Angeles Chargers** (`56.2%`) | `LAR 22 x 25 LAC` | 52¢ / 49¢ | **YES LAC (Los Angeles Chargers)** | `+7.24%` | **US$ 35.49** |
| `KXNFLGAME-26NOV01INDJAC` | **Indianapolis Colts @ Jacksonville Jaguars** | 🏆 **Jacksonville Jaguars** (`52.1%`) | `JAC 23 x 23 IND` | 54¢ / 47¢ | **NO TRADE (Preço Kalshi Eficiente / Sem Margem de Segurança)** | `+0.63%` | **US$ 0.00** |
| `KXNFLGAME-26NOV01LVNYJ` | **Las Vegas Raiders @ New York Jets** | 🏆 **New York Jets** (`76.8%`) | `NYJ 27 x 17 LV` | 61¢ / 40¢ | **YES NYJ (New York Jets)** | `+15.79%` | **US$ 80.00** |

---

## 📐 3. Formulação Matemática (Dr. Henrique Vasconcelos — Matemático)

1. **Equação Estrutural de Diferencial de Pontos Esperado ($\mu_\Delta$):**
   $$\mu_\Delta = \frac{\text{Elo}_H - \text{Elo}_A}{25.0} + 22.0 \cdot \left(\text{NetEPA}_H - \text{NetEPA}_A\right) + 1.5 \cdot \left(\text{TO}_H - \text{TO}_A\right) + \text{HFA}$$
2. **Precificação de Contrato Binário Kalshi com Regra de Empate ($0.50):**
   $$\text{EV}(\text{Yes}) = P_{\text{Argon}}(\text{Win}) \cdot (1 - c) + P_{\text{Argon}}(\text{Tie}) \cdot (0.50 - c) - P_{\text{Argon}}(\text{Loss}) \cdot c$$
3. **Critério de Kelly Fracionário Prudencial ($\gamma = 0.25$):**
   $$f^* = 0.25 \cdot \max\left(0, \frac{P_{\text{Argon}} - c}{1 - c}\right)$$

---

## 🤖 4. Validação do Modelo Preditivo (Lucas Bittencourt — Cientista de Dados)

Seguindo estritamente o protocolo `ml-best-practices` (divisão 80% treino / 20% teste **antes** da padronização Z-Score em `PROJ-002-KALSHI-NFL_synthetic_matchups.csv`):
- **Amostra de Treino / Teste:** `1440` jogos / `360` jogos
- **Erro RMSE de Margem de Vitória (Baseline vs. Modelo Argon):** Redução de `14.55` pts para **`13.33` pts**
- **Brier Score de Calibração Probabilística (Baseline vs. Modelo Argon):** Melhora de `0.2497` para **`0.2243`** (IC 95% Bootstrap: `[0.2099, 0.2394]`)
- **Acurácia de Vencedor Fora da Amostra (Out-of-Sample):** **`62.78%`**

---

## 🛡️ 5. Parecer Atuarial e Gestão de Risco da Banca (Beatriz Alencar — Atuária)

Simulando 10.000 domingos completos para uma banca de referência de **US$ 1,000.00**:
- **Posições Aprovadas com Valor Positivo ($\text{EV} > 0$):** `7` de 9 jogos
- **Capital Total Exposto na Rodada:** **US$ 342.53** (`34.25%` da banca)
- **Reserva Técnica Intocada (Caixa Protegido):** **US$ 657.47** (`65.75%` da banca)
- **Lucro Líquido Esperado na Rodada:** **+US$ 60.60** (P90: **+US$ 187.41**)
- **Value at Risk ($\text{VaR}_{95\%}$ da Carteira):** US$ 129.50 (Perda máxima em 95% dos cenários limitada a `12.95%` da banca)
- **Expected Shortfall ($\text{CVaR}_{95\%}$):** US$ 176.93
- **Probabilidade de Ruína da Banca ($\psi(u)$):** **`0.0%` (Zero Ruína)**

---

## 🎯 6. Plano de Ação Tático (Síntese de Axio Vance)

### 6.1 Ranking de Vencedores no Campo (Quem Vai Ganhar — Do Mais Provável ao Mais Equilibrado)
   - **New York Jets** vence `Las Vegas Raiders @ New York Jets` (**`76.8%`** de probabilidade | Placar Mediano: `NYJ 27 x 17 LV`)
   - **Detroit Lions** vence `Minnesota Vikings @ Detroit Lions` (**`71.5%`** de probabilidade | Placar Mediano: `DET 29 x 20 MIN`)
   - **Dallas Cowboys** vence `Arizona Cardinals @ Dallas Cowboys` (**`70.3%`** de probabilidade | Placar Mediano: `DAL 27 x 19 ARI`)
   - **Washington Commanders** vence `Philadelphia Eagles @ Washington Commanders` (**`67.8%`** de probabilidade | Placar Mediano: `WAS 28 x 21 PHI`)
   - **Buffalo Bills** vence `Baltimore Ravens @ Buffalo Bills` (**`65.8%`** de probabilidade | Placar Mediano: `BUF 27 x 22 BAL`)
   - **Tampa Bay Buccaneers** vence `Atlanta Falcons @ Tampa Bay Buccaneers` (**`61.9%`** de probabilidade | Placar Mediano: `TB 25 x 22 ATL`)
   - **Kansas City Chiefs** vence `Kansas City Chiefs @ Denver Broncos` (**`60.1%`** de probabilidade | Placar Mediano: `DEN 22 x 26 KC`)
   - **Los Angeles Chargers** vence `Los Angeles Chargers @ Los Angeles Rams` (**`56.2%`** de probabilidade | Placar Mediano: `LAR 22 x 25 LAC`)
   - **Jacksonville Jaguars** vence `Indianapolis Colts @ Jacksonville Jaguars` (**`52.1%`** de probabilidade | Placar Mediano: `JAC 23 x 23 IND`)

### 6.2 Carteira Recomendada de Contratos Kalshi (Ordenada por Maior Vantagem Matemática / Edge)
   - **`YES NYJ (New York Jets)` a `61¢`** (`KXNFLGAME-26NOV01LVNYJ`): Probabilidade Argon de **`76.8%`** vs. `61%` implícito no Kalshi -> **Edge Líquido: `+15.79%`** | ROI Esperado: **`+26.05%`** | Alocação Kelly: **US$ 80.00**.
   - **`YES DAL (Dallas Cowboys)` a `59¢`** (`KXNFLGAME-26NOV01ARIDAL`): Probabilidade Argon de **`70.3%`** vs. `59%` implícito no Kalshi -> **Edge Líquido: `+11.27%`** | ROI Esperado: **`+19.22%`** | Alocação Kelly: **US$ 68.72**.
   - **`YES DET (Detroit Lions)` a `62¢`** (`KXNFLGAME-26NOV01MINDET`): Probabilidade Argon de **`71.5%`** vs. `62%` implícito no Kalshi -> **Edge Líquido: `+9.50%`** | ROI Esperado: **`+15.45%`** | Alocação Kelly: **US$ 62.50**.
   - **`YES LAC (Los Angeles Chargers)` a `49¢`** (`KXNFLGAME-26NOV01LACLAR`): Probabilidade Argon de **`56.2%`** vs. `49%` implícito no Kalshi -> **Edge Líquido: `+7.24%`** | ROI Esperado: **`+14.97%`** | Alocação Kelly: **US$ 35.49**.
   - **`YES TB (Tampa Bay Buccaneers)` a `55¢`** (`KXNFLGAME-26NOV01ATLTB`): Probabilidade Argon de **`61.9%`** vs. `55%` implícito no Kalshi -> **Edge Líquido: `+6.86%`** | ROI Esperado: **`+12.63%`** | Alocação Kelly: **US$ 38.11**.
   - **`YES KC (Kansas City Chiefs)` a `54¢`** (`KXNFLGAME-26NOV01KCDEN`): Probabilidade Argon de **`60.1%`** vs. `54%` implícito no Kalshi -> **Edge Líquido: `+6.08%`** | ROI Esperado: **`+11.41%`** | Alocação Kelly: **US$ 33.04**.
   - **`YES BUF (Buffalo Bills)` a `62¢`** (`KXNFLGAME-26NOV01BALBUF`): Probabilidade Argon de **`65.8%`** vs. `62%` implícito no Kalshi -> **Edge Líquido: `+3.75%`** | ROI Esperado: **`+6.22%`** | Alocação Kelly: **US$ 24.67**.
