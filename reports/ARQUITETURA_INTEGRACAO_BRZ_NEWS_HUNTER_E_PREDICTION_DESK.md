# 🏛️ Arquitetura Completa: `BRZ.DESK Prediction` (Dia a Dia), `BRZ.PREDICTION` (Semanal AXIOS) & Novo Editorial de Mercado/Social

**Projeto GCP:** `brz-news-prod` (`projects/533645601719` · `us-central1` / `global`)  
**Motor Atualizado:** [core/brz_news_daily_prediction_graph.py](file:///c:/NWX/nwx-Argon/core/brz_news_daily_prediction_graph.py)  
**Protótipo Interativo em Canvas:** [grafo_prediction_gcp_canvas.html](file:///C:/Users/wilju/.gemini/antigravity/brain/a87e5d2d-eefb-4e61-a19c-d8ac42477f55/grafo_prediction_gcp_canvas.html)

---

## 🧭 1. Divisão Clara de Papel entre `BRZ.DESK` (Dia a Dia) e `BRZ.PREDICTION` (Semanal AXIOS)

| Dimensão | `BRZ.DESK Prediction` (`/pro/prediction-desk` & `/pro/trade`) | `BRZ.PREDICTION` (`/prediction` & `/pro/publish`) |
| :--- | :--- | :--- |
| **Horizonte Temporal** | **Dia a Dia / Intradiário (Operacional)** | **Semanal / Macro-Estratégico (Relatório + Radar Geral)** |
| **Como Funciona a Tela** | **100% Centrada na Predição Escolhida:** Quando o usuário clica em `BRL x Dólar (USD/BRL)` (ou `IPCA 2026`, `Copom Selic`), **toda a tela do Desk** muda para exibir o **Gráfico do Terminal**, o que está sendo colocado no **Kalshi + Polymarket**, a **Análise Fundamentalista**, a **Análise Gráfica/Técnica**, as **Notícias do Ativo** e a **Boleta em 3 Lotes**. | **Visão Geral + Relatório Semanal do AXIOS:** Lista todos os 23 predictions do Brasil com volume ($\ge \text{US\$ } 10\text{k}$), feed de notícias que movem o mercado e o **Relatório Semanal Oficial do AXIOS** sobre o contrato de **Principal Volume da Semana**. |
| **Papel do AXIOS (Axio Vance)** | Atualiza 4x ao dia (`09h`, `11h`, `17h`, `19h ET`) os livros de ofertas, níveis gráficos e gatilhos de lote de cada workspace. | Roda continuamente para identificar o **#1 Maior Volume da Semana** (hoje: `USD/BRL Kalshi` com $\text{US\$ } 574.531$), gerando e mantendo atualizado o relatório executivo para os clientes. |
| **Documento Firestore** | `desk_predictions/latest` ([firestore_brz_desk_prediction_pro.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/firestore_brz_desk_prediction_pro.json)) | `prediction_radar/latest` ([firestore_brz_prediction_public.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/firestore_brz_prediction_public.json)) |

---

## 📈 2. Como Funciona a Página `BRZ.DESK Prediction` (Dia a Dia por Ativo Escolhido)

Quando o usuário seleciona uma predição na barra superior do Desk — por exemplo, **`BRL x Dólar (USD/BRL)`** (`WS-01-USDBRL-DOLAR`) — a página reconfigura simultaneamente **6 módulos sincronizados**:

1. **Módulo 1 — Gráfico do Terminal (`TradingView` + Curva Kalshi/Polymarket):**
   - Carrega automaticamente o gráfico `FX_IDC:USDBRL` (com atalhos rápidos para `AMEX:EWZ`, `NYSE:ITUB`, `NYSE:PBR`, `TVC:DXY`) sobreposto à série histórica das probabilidades implícitas na Kalshi (`R$ 6,00` a `22¢` e `R$ 6,50` a `12¢`) e à banda técnica de exaustão (`R$ 5,8650 – R$ 5,9200`).
2. **Módulo 2 — Livros de Ofertas Kalshi & Polymarket Lado a Lado (*"O que está sendo colocado"*):**
   - Mostra exatamente onde o dinheiro institucional está posicionado naquele tema:
     - **Na Kalshi (`KXUSDBRLMAX-26DEC31` — $\text{US\$ } 574.531$ Vol):**
       - Strike `R$ 6,00+`: `16¢ Bid / 34¢ Ask` (`Last 22¢` · $\text{US\$ } 173.222$ Vol · `6.917 OI`)
       - Strike `R$ 6,50+` (**Alvo Principal**): `11¢ Bid / 12¢ Ask` no YES e **`88¢ Bid / 89¢ Ask` no NO** ($\text{US\$ } 127.001$ Vol · `8.425 OI` · Spread de `1¢`)
       - Strikes `R$ 6,75+` (`10¢`) e `R$ 7,00+` (`2¢`)
     - **No Polymarket (Correlatos Diretos de Carry do Real):**
       - `Copom Selic Novembro (#3347918)`: **`81,9¢ Bid / 82,4¢ Ask`** ($\text{US\$ } 126.098$ Vol · $\text{US\$ } 24.118$ Liquidez)
       - `IPCA 2026 Faixa 5,00%–5,49% (#1243901)`: **`48,4¢ Bid / 49,0¢ Ask`** ($\text{US\$ } 198.671$ Vol)
3. **Módulo 3 — Análise Fundamentalista com Dados Oficiais (`Gabriel Torres 05` + `Clara Mendonça 02`):**
   - Tabela de fundamentos em tempo real:
     - **Diferencial de Juros (Carry):** Selic a `14,75% a.a.` vs. Fed Funds `4,50%–4,75%` (`+1.000 bps` de spread a favor do Real).
     - **Câmbio PTAX (BCB SGS 1):** `R$ 5,7640` (`12,7%` de colchão até a barreira de `R$ 6,50`).
     - **Reservas Internacionais do BCB:** $\text{US\$ } 358,4\text{ Bilhões}$ (estoque de swaps $> \text{US\$ } 100\text{B}$).
     - **Balança Comercial 12M:** Superávit de $+\text{US\$ } 76,2\text{ Bilhões}$.
4. **Módulo 4 — Análise Gráfica & Técnica Quantitativa (`Henrique Vasconcelos 01` + `Lucas Bittencourt 03`):**
   - Indicadores técnicos objetivos:
     - **Suporte Técnico Spot:** `R$ 5,6800 / R$ 5,6200`
     - **Resistência Gráfica & Defesa de Swaps:** `R$ 5,8650 / R$ 5,9200` (banda de $+2\sigma$ de Ornstein-Uhlenbeck)
     - **RSI (14 Períodos Diário):** `46,8` (perda de momentum comprador no dólar)
     - **Volatilidade Realizada 30d vs. Implícita:** `14,2%` vs. `17,8%` (prêmio caro favorece venda de cauda / compra de `NO` a `89¢`).
5. **Módulo 5 — Feed de Notícias Exclusivas do Ativo (`Market & Prediction First`):**
   - Exibe apenas as reportagens que movem o `USD/BRL` e os ADRs expostos (`EWZ`, `ITUB`, `PBR`, `VALE`, `NU`).
6. **Módulo 6 — Tribunal Atuarial 5x5 + Boleta em 3 Lotes (*Free-Roll*):**
   - **5 Pessimistas (`88,4%`) vs. 5 Otimistas (`95,8%`) $\rightarrow$ Veredito Juiz Supremo: `92,5%` (`+350 bps` Edge)**.
   - **Lote 1 (`40%`):** Venda Limit a `94¢` ($P(\text{touch}) = 86\%$).
   - **Lote 2 (`40%` — Trava *Free-Roll*):** Venda Limit a `97¢` ($P(\text{touch}) = 74\%$).
   - **Lote 3 (`20%` — *Runner*):** *Hold* até `100¢` · **Stop-Loss:** `78¢`.

*(O mesmo padrão completo é carregado imediatamente quando o usuário troca para **`IPCA Inflação 2026`** ou **`Copom Taxa Selic`**).*

---

## 📊 3. Como Funciona a Página `BRZ.PREDICTION` (Semanal AXIOS + Todos os Predictions)

Na página **`BRZ.PREDICTION`**, o cliente tem a visão consolidada da semana:
1. **Relatório Semanal Oficial do AXIOS sobre o Principal Volume (`axios_weekly_volume_leader_report`):**
   - O **AXIOS** (orquestrador `Axio Vance`) monitora automaticamente qual contrato brasileiro concentrou o **maior volume financeiro da semana** (nesta semana: `Kalshi KXUSDBRLMAX-26DEC31` com **$\text{US\$ } 574.531,52$**, somando **$\text{US\$ } 1,05\text{M}$** junto com IPCA e Selic).
   - Entrega um relatório estruturado em 3 capítulos:
     1. *Radiografia do Volume Principal: O que o Dinheiro Institucional está Colocando*
     2. *Conexão Fundamentalista & Gráfica: Por que o Juro de 14,75% Protege a Barreira Cambial*
     3. *Mapa de Oportunidades da Semana (Resumo das 3 Boletas Líderes)*
2. **Painel Completo dos 23 Predictions do Brasil ($\ge \text{US\$ } 10.000$ de Volume · $\text{US\$ } 2,64\text{M}$):**
   - Todos os mercados qualificados com botão direto **`Abrir no BRZ.DESK →`** para quem quiser operar o dia a dia daquele contrato.
3. **Radar de Arbitragem Cross-Exchange (`Polymarket vs. Kalshi`) & Feed de Notícias de Mercado.**

---

## 📰 4. Nova Diretriz de Notícias & Editorial para Redes Sociais

### 4.1. Fim da Política no Principal $\rightarrow$ Foco 100% `Prediction & Market`
- No arquivo [focus.py](file:///C:/NWX/brz-backend-publish-20261016/src/agents/shared/focus.py) e nas pautas do `Hunter Vance`, removemos `Politics` das prioridades principais das 4 janelas diárias:
  - **`09:00 ET` (`calendar`):** `["Currencies", "Markets", "Macroeconomia", "Investing"]`
  - **`11:00 ET` (`open`):** `["Markets", "Currencies", "Investing", "NASDAQ"]`
  - **`17:00 ET` (`close`):** `["Markets", "Investing", "Currencies", "Small Caps", "NASDAQ"]`
  - **`19:00 ET` (`wrap`):** `["Markets", "Currencies", "Agro", "Tech", "Investing"]`
- Política só entra como variável secundária quando houver **arbitragem financeira direta com alto volume** e impacto mensurável em um ativo listado nos EUA (`PBR`, `EWZ`).

### 4.2. Novo Padrão de Redes Sociais: Hook com Mais Texto + Carrossel Caçador de Oportunidades
Ajustamos a geração de social media ([hunter_prediction_pautas.json](file:///c:/NWX/nwx-Argon/sandbox/runs/brz_news_daily_integration/hunter_prediction_pautas.json)) para:

1. **Hook Analítico Denso (45 a 65 palavras logo na abertura):**
   - Em vez de frases curtas superficiais, o Hook já entrega **o volume financeiro apostado, o preço do contrato no Kalshi/Polymarket, a tese fundamentalista/gráfica e os tickers impactados na corretora**:
   > *"More than \$574,500 is currently locked inside CFTC-regulated Kalshi contracts betting on how high the US dollar can climb against the Brazilian real by December — and the orderbook is flashing a major signal for anyone holding NYSE-listed Brazilian stocks (EWZ, PBR, VALE, ITUB, NU). While retail headlines focus on daily currency noise around R\$ 5.76, institutional order flow is pricing an 88% probability that USD/BRL never touches R\$ 6.50, backed by a 1,000-basis-point interest-rate advantage over the Federal Reserve."*

2. **Carrossel de 6 Slides Focado em Achar Oportunidades e Acompanhar Notícias que Movem o Mercado:**
   - **Slide 1 (Capa com Hook Denso de Oportunidade & Volume):** Título forte + subtítulo analítico completo explicando a oportunidade e o volume real em jogo.
   - **Slide 2 (O que Kalshi & Polymarket estão precificando agora):** Mostra os preços exatos dos contratos (`Bid/Ask`, `Open Interest` e divergências entre bolsas).
   - **Slide 3 (Confluência Fundamentalista + Gráfica):** Combina os dados macro oficiais (`Carry 14,75%`, `Reservas US$ 358B`) com os níveis técnicos do gráfico (`Resistência R$ 5,86–5,92`).
   - **Slide 4 (Notícias Catalisadoras para Acompanhar na Semana):** Lista os 3 eventos/notícias exatos (`Leilão PTAX BCB`, `IPCA-15 IBGE`, `Comunicado Copom`) que vão mexer no preço do contrato.
   - **Slide 5 (Impacto na Conta de Corretora & Assimetria):** Mostra como a oportunidade afeta diretamente `EWZ`, `ITUB`, `BBD`, `PBR`, `VALE` e `NU`.
   - **Slide 6 (CTA para `BRZ.DESK` Diário e `BRZ.PREDICTION` Semanal):** Convida o leitor a acompanhar o terminal diário no `BRZ.DESK` e ler o Relatório Semanal do AXIOS no `BRZ.PREDICTION`.
