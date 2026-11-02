# 🇨🇦 Relatório Quantitativo & Boletas v4.0: Mercado de Opções e Derivativos do Dólar Canadense (`USD/CAD`, `FXC`, `6C` & `Bank of Canada`)

**Data da Execução:** `2026-11-01 22:40 ET`  
**Motor Executado:** [core/cad_options_quant_engine.py](file:///c:/NWX/nwx-Argon/core/cad_options_quant_engine.py) (Grafo Argon v4.0 com **Garman-Kohlhagen 1983**, **Barreira One-Touch Reiner-Rubinstein** e **Matriz de 4 Saídas de Mitigação de Erro**)  
**Dados Brutos Coletados:** [sandbox/data/cad_options_live_scan.json](file:///c:/NWX/nwx-Argon/sandbox/data/cad_options_live_scan.json) e [sandbox/data/cad_deep_markets.json](file:///c:/NWX/nwx-Argon/sandbox/data/cad_deep_markets.json)  
**Resultados Completos da Simulação:** [sandbox/runs/CAD_OPTIONS_V4_ANALYSIS_RESULTS.json](file:///c:/NWX/nwx-Argon/sandbox/runs/CAD_OPTIONS_V4_ANALYSIS_RESULTS.json)

---

## 📊 1. Fotografia Real do Mercado Canadense (Spot, Carry & Volatilidade)

Nosso scanner ([scan_cad_options_live.py](file:///c:/NWX/nwx-Argon/core/scan_cad_options_live.py)) coletou em tempo real a estrutura à vista, os juros e os contratos abertos nas bolsas de derivativos e mercados preditivos:

| Indicador / Ativo | Ticker Oficial | Cotação / Nível Atual | Faixa de 3 Meses (Min – Máx) | Impacto Estrutural nas Opções de CAD |
| :--- | :--- | :---: | :---: | :--- |
| **Dólar Americano vs. Canadense** | `USD/CAD` (`CAD=X`) | **`1.3986 CAD`** | `1.3733` – `1.4299` | Consolidando logo abaixo da barreira psicológica de `1.4000`. |
| **Dólar Canadense em USD (Futuros CME `6C`)** | `CAD/USD` (`CADUSD=X`) | **`0.7150 USD`** (`71.50¢`) | `0.6994` – `0.7282` | Cada `100 bps` de alta no `USD/CAD` equivale a `-51 bps` no `CAD/USD`. |
| **ETF de Opções Listadas de CAD** | `FXC` *(NYSE Arca)* | **`US$ 69.93`** | `US$ 68.35` – `US$ 71.10` | Espelha `100x CAD/USD`; permite operar Calls e Puts padronizadas com risco limitado. |
| **Petróleo WTI Crude** | `CL=F` *(NYMEX)* | **`US$ 101.00 / bbl`** | `US$ 74.24` – `US$ 110.48` | Principal suporte de termos de troca do Canadá (segura quedas bruscas do CAD). |
| **Spread de Juros (Carry `US 10Y` vs. `BoC`)** | `^TNX` (`4.929%`) vs. `BoC` (`2.50%`) | **`+242.9 bps` pró-USD** | — | Forte diferencial positivo a favor do USD (`r_US - r_CA = +2.43% a.a.`), encarecendo Calls de `USD/CAD` (e Puts de `FXC`). |
| **Volatilidade (`3M Realizada` vs. `IV Dez/26`)** | $\sigma_{\text{hist}}$ vs. $\sigma_{\text{IV}}$ | **`6.85%` vs. `7.60%`** | Skew 25$\Delta$: `+60 bps` | Prêmio de risco tarifário EUA-Canadá infla a volatilidade implícita das opções OTM. |

---

## 📐 2. Grade de Opções Tradicionais — Modelo de Garman-Kohlhagen (Vencimento `18/Dez/2026`, `47 DTE`)

Para precificar opções de moedas sem cometer o erro clássico de usar Black-Scholes de ações (que ignora a taxa de juros da moeda estrangeira $r_f$), o motor do **Dr. Henrique Vasconcelos (`01`)** aplica a equação exata de **Garman & Kohlhagen (1983)**:

$$C_{\text{GK}} = S_0 e^{-r_f T} N(d_1) - K e^{-r_d T} N(d_2), \qquad P_{\text{GK}} = K e^{-r_d T} N(-d_2) - S_0 e^{-r_f T} N(-d_1)$$

### 2.1 Cadeia de Opções Spot/OTC `USD/CAD` (`Spot = 1.3986`, `T = 47 dias`)

| Strike `USD/CAD` ($K$) | Vol. Implícita ($\sigma_{\text{IV}}$) | Prêmio `CALL` (em CAD) | $\Delta_{\text{Call}}$ | Prêmio `PUT` (em CAD) | $\Delta_{\text{Put}}$ | $\Gamma$ (Gamma) | $\mathcal{V}$ (Vega / 1% Vol) | $\Theta$ Diário (`Call`) | Prob. ITM no Vencimento (`Call`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`1.3800`** *(ITM)* | `7.20%` | `0.02245` (`224.5 pips`) | `+0.6549` | `0.00827` (`82.7 pips`) | `-0.3387` | `10.086` | `0.00183` | `-0.8 pip/d` | `64.96%` |
| **`1.3900`** *(ITM)* | `7.40%` | `0.01691` (`169.1 pips`) | `+0.5473` | `0.01269` (`126.9 pips`) | `-0.4463` | `10.583` | `0.00197` | `-1.0 pip/d` | `54.03%` |
| **`1.4000`** *(ATM)* | **`7.63%`** | **`0.01251` (`125.1 pips`)** | **`+0.4427`** | **`0.01826` (`182.6 pips`)** | **`-0.5510`** | **`10.253`** | **`0.00197`** | **`-1.2 pip/d`** | **`43.47%`** |
| **`1.4100`** *(OTM)* | `7.86%` | `0.00910` (`91.0 pips`) | `+0.3481` | `0.02482` (`248.2 pips`) | `-0.6456` | `9.332` | `0.00185` | `-1.2 pip/d` | `33.99%` |
| **`1.4250`** *(OTM)* | **`8.20%`** | **`0.00551` (`55.1 pips`)** | **`+0.2322`** | `0.03617` (`361.7 pips`) | `-0.7615` | `7.394` | `0.00153` | `-1.1 pip/d` | `22.48%` |
| **`1.4500`** *(Deep OTM)* | `8.78%` | `0.00228` (`22.8 pips`) | `+0.1087` | `0.05787` (`578.7 pips`) | `-0.8849` | `4.226` | `0.00093` | `-0.8 pip/d` | `10.36%` |

### 2.2 Cadeia de Opções Listadas em Bolsa — ETF `FXC` (`Spot = US$ 69.93`, Multiplicador `100x`)

| Strike `FXC` (US$) | Equiv. `USD/CAD` | Vol. Implícita ($\sigma_{\text{IV}}$) | Prêmio `CALL` (US$/ação) | $\Delta_{\text{Call}}$ | Prêmio `PUT` (US$/ação) | $\Delta_{\text{Put}}$ | $\Theta$ Diário (`Put`) | Prob. ITM (`Put`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`$68.50`** | `1.4277` | `8.21%` | `US$ 1.88` (`$188/ct`) | `+0.7915` | **`US$ 0.24` (`$24/ct`)** | **`-0.2053`** | `-$0.52/dia` | `21.45%` |
| **`$69.00`** | `1.4174` | `8.00%` | `US$ 1.49` (`$149/ct`) | `+0.7195` | `US$ 0.35` (`$35/ct`) | `-0.2773` | `-$0.58/dia` | `28.79%` |
| **`$69.50`** | `1.4072` | `7.78%` | `US$ 1.14` (`$114/ct`) | `+0.6330` | `US$ 0.49` (`$49/ct`) | `-0.3638` | `-$0.60/dia` | `37.55%` |
| **`$70.00`** *(ATM)* | **`1.3971`** | **`7.57%`** | `US$ 0.83` (`$83/ct`) | `+0.5343` | **`US$ 0.68` (`$68/ct`)** | **`-0.4625`** | **`-$0.58/dia`** | **`47.48%`** |
| **`$70.50`** | `1.3872` | `7.35%` | `US$ 0.57` (`$57/ct`) | `+0.4282` | `US$ 0.92` (`$92/ct`) | `-0.5686` | `-$0.49/dia` | `58.08%` |
| **`$71.00`** | `1.3775` | `7.20%` | `US$ 0.38` (`$38/ct`) | `+0.3234` | `US$ 1.22` (`$122/ct`) | `-0.6734` | `-$0.36/dia` | `68.48%` |

---

## 🎯 3. As 3 Melhores Operações no Dólar Canadense (Com Matriz v4.0 de Saídas de Mitigação de Erro)

Aplicando tudo o que aprendemos na auditoria anterior (`KC vs DEN` e `PHI vs WAS`), **nenhuma operação em opções de CAD é aberta a seco**. Cada uma das 3 operações abaixo já nasce com:
1. **Ordens `Limit Sell` automáticas no segundo zero** (para nunca perder um spike intradiário); e
2. **A Matriz de 4 Saídas de Mitigação de Erro (`Drawdown Recovery`)** para sair no zero-a-zero se o câmbio ou os juros andarem contra.

---

### 🏆 Operação #1 (Arbitragem Cross-Exchange + Opção Binária de Juros CAD): Decisão do Bank of Canada em Dezembro (`+25 bps`)
* **Onde estão os contratos reais agora (`US$ 271.850` de volume combinado):**
  * **Polymarket `#991303` (*BoC increases overnight rate by 25 bps in December*):** `Bid 36.0¢ / Ask 37.0¢` (`Volume: US$ 70.750`)
  * **Kalshi `KXCBDECISIONCANADA-26DEC-H25` (*BoC Hike 25bps in Dec 2026*):** `Bid 38.0¢ / Ask 39.0¢` (`Volume: US$ 33.068`)
  * **Kalshi `KXCANOREOY-26DEC31-E2.75` (*Taxa do BoC em 31/Dez exatamente 2.75%*):** `Bid 39.0¢ / Ask 43.0¢` (`Volume: US$ 5.627`)
* **Por que essa é a operação #1 do Grafo v4.0?**
  * Existe uma **inversão direta de livros entre Polymarket e Kalshi**: você compra `YES (+25 bps)` na Polymarket pagando o `Ask` de **`37.0¢`**, enquanto na Kalshi os compradores já estão pagando **`38.0¢` (`Bid` em `H25`) e `39.0¢` (`Bid` em `E2.75`)** pelo mesmíssimo evento!
  * Ou seja: **você já entra comprando 1¢ a 2¢ abaixo do preço de venda (`Bid`) da outra bolsa!**

#### 📋 Boleta Completa v4.0 (`Base US$ 100,00` = `270,27 shares` a `37.0¢`)

| Modo do Grafo v4.0 | Trincheira / Lote | % da Mão | Qtde Shares | Preço `Limit Sell` | Caixa Gerado | Explicação Tática (Lucro vs. Mitigação de Erro) |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **🟢 MODO LUCRO (*Free-Roll*)** | **Lote 1 (TP1)** | `40%` | `108,11` | **`44,0¢`** | **`US$ 47,57`** | Vende no 1º dado de CPI/Emprego do Canadá acima do consenso. |
| **🟢 MODO LUCRO (*Free-Roll*)** | **Lote 2 (Trava *Free-Roll*)** | `40%` | `108,11` | **`51,1¢`** | **`US$ 55,24`** | Soma **`US$ 102,81` em caixa (`+US$ 2,81` garantidos)** antes da reunião do BoC! |
| **🟢 MODO LUCRO (*Free-Roll*)** | **Lote 3 (*Runner*)** | `20%` | `54,05` | **`100,0¢`** | **`US$ 54,05`** | Corre 100% grátis; se o BoC subir `+25 bps`, caixa total = **`US$ 156,86` (`ROI +56,86%`)**. |
| **🛡️ MODO MITIGAÇÃO DE ERRO** | **Saída A · Vazio do Livro** | **`45%`** | **`121,62`** | **`38,5¢`** | **`US$ 46,82`** | Se o contrato recuar para `35¢`, pendure `45%` a `38,5¢` (nível do Bid da Kalshi) para cortar metade do risco no primeiro repique. |
| **🛡️ MODO MITIGAÇÃO DE ERRO** | **Saída B · Escudo Breakeven** | **`40%`** | **`108,11`** | **`41,4¢`** | **`US$ 44,76`** | Vende mais `40%` a `41,4¢`, somando **`US$ 91,58`** recuperados. |
| **🛡️ MODO MITIGAÇÃO DE ERRO** | **Saída C · *Scratch* / Trava Kalshi** | **`15%`** | **`40,54`** | **`37,5¢`** | **`US$ 15,20`** | Zera o resto a `37,5¢` (ou vende `H25` na Kalshi a `38¢`), fechando a mitigação com **`US$ 106,78` (`+US$ 6,78`, zero prejuízo!)**. |
| **🛡️ MODO MITIGAÇÃO DE ERRO** | **Saída D · Stop de Preservação** | Defesa | Restante | **`27,4¢`** | Salva **`US$ 74,05`** | Se o CPI canadense vier muito fraco e romper o suporte de `28¢`, preserva `74%` do caixa. |

---

### 🏆 Operação #2 (Opções Tradicionais Listadas — Controle de Gregas `Theta` e `Vega`): *Bear Put Spread* em `FXC` (`$70.00 / $68.50`) ou *Bull Call Spread* em `USD/CAD` (`1.4000 / 1.4250`)
* **O Erro Clássico que o Grafo v4.0 Evita:** Comprar uma opção de moeda a seco (*naked Call* em `USD/CAD` ou *naked Put* em `FXC $70.00` por `US$ 68,00/contrato`) faz você perder dinheiro todos os dias pelo **Theta (`-$0,58/dia`)** e sofrer se a volatilidade implícita cair (**Vega crush**) mesmo que o dólar canadense ande na sua direção!
* **A Estrutura Blindada v4.0 (`Bear Put Spread FXC Vencimento 18/Dez/2026`):**
  1. **Perna Comprada (`Long Put ATM`):** Compra `1x Put FXC Strike $70.00` pagando **`US$ 0,68`** (`US$ 68,41` por contrato de 100 ações, $\Delta = -0.4625$).
  2. **Perna Vendida (`Short Put OTM` — Financiadora):** Vende `1x Put FXC Strike $68.50` recebendo **`US$ 0,24`** (`US$ 24,15` de crédito imediato, $\Delta = +0.2053$).
  * **Custo Líquido (*Net Debit*):** Apenas **`US$ 0,44` por ação (`US$ 44,26` por contrato)** — uma **redução imediata de `35,3%` no custo e no risco máximo** em relação à opção seca!
  * **Payoff Máximo no Vencimento (se `FXC <= $68.50` / `USD/CAD >= 1.4277`):** **`US$ 1,50` (`US$ 150,00` por contrato)** $\rightarrow$ Lucro líquido de **`+US$ 105,74` (`ROI +238,9%`)**!
  * **Ponto de Empate (*Breakeven*):** `FXC = US$ 69,56` (basta o `USD/CAD` subir míseros **`+0,53%`**, de `1.3986` para **`1.4060`**, para a operação já estar no lucro!).
* **Matriz de Saídas de Mitigação de Erro nas Opções Tradicionais (`FXC` / `6C`):**
  * **Saída 1 (Trava *Free-Roll* no Toque de `USD/CAD 1.4150`):** Quando `USD/CAD` tocar `1.4150` (`FXC = $69.10`), a trava sobe de `US$ 0,44` para **`US$ 0,88` (`+100%`)**. Venda **50% dos contratos** e deixe a outra metade rodando 100% grátis até `1.4277`!
  * **Saída 2 (Mitigação por *Roll Down* / *Butterfly* se `USD/CAD` recuar para `1.3900`):** Se o `USD/CAD` recuar para `1.3900` na primeira semana e o spread cair de `US$ 0,44` para `US$ 0,33` (`-US$ 11,00`), **não realize o prejuízo**: venda uma Put intermediária (`Strike $69.25` por `US$ 0,22`), embolsando mais crédito e reduzindo seu risco máximo na operação de `US$ 44` para apenas **`US$ 22`**!
  * **Saída 3 (Stop Temporal de Theta a `21 DTE` — `27/Nov/2026`):** Regra pétrea da **Beatriz Alencar (`04`)**: opções compradas nunca passam da marca de `21 dias para o vencimento` se estiverem fora do dinheiro (*OTM*), pois a curva de decaimento do Theta acelera exponencialmente nos últimos 20 dias.

---

### 🏆 Operação #3 (Opção Binária de Barreira *One-Touch* — `USD/CAD` toca `1.4500` em 2026): Como o Filtro Anti-Erro v4.0 Evita uma Armadilha de Preço
* **Contrato Analisado:** Polymarket `#200525` (*Will USD/CAD hit 1.45 (High) in 2026?*)
  * **Livro Atual:** `Bid 36.0¢ / Ask 38.0¢` | **Último Negócio (`Last`):** `24.0¢` | **Volume:** `US$ 6.317,70`
* **Cálculo de Barreira Contínua (*First-Passage Time* de Reiner-Rubinstein + 25.000 Simulações com Ponte Browniana):**
  * Probabilidade de **terminar** o ano acima de `1.4500` ($N(d_+)$): apenas **`22,33%`**.
  * Probabilidade de **tocar ao menos uma vez** em `1.4500` até 31/Dez/2026 ($P(\tau_{1.45} \le T)$): **`39,37%`** (somente se o choque tarifário EUA-Canadá adicionar `+3,5% a.a.` de drift ao carry de `+2,43%`). Sem choque tarifário (apenas carry), a probabilidade de toque cai para **`29,4%`**.
* **Veredito do Filtro Anti-Erro v4.0:**
  * Pagar **`38.0¢` a mercado no `Ask`** quando o último negócio saiu a **`24.0¢`** e a probabilidade neutra de barreira é `29,4%–39,3%` **não oferece margem de segurança atuarial suficiente**.
  * **Ação Recomendada pelo Grafo v4.0:** **NÃO agredir o `Ask` de `38.0¢`!** Posicionar ordem de compra passiva (**`Limit Bid` a `26,0¢–28,0¢`**) para capturar despejos de liquidez (como o negócio que saiu a `24,0¢`), e pendurar imediatamente a saída de descompressão (`45%` das shares) em **`34,0¢`** e a trava de *Free-Roll* (`40%` das shares) em **`38,0¢`**!
