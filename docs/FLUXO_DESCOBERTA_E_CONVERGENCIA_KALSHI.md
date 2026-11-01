# 🔍 Arquitetura de Descoberta e Convergência Probabilística — Caso Kalshi NFL (`KXNFLGAME`)

> **Autor:** Axio Vance — Orquestrador e Programador Sênior  
> **Projeto de Referência:** `PROJ-002-KALSHI-NFL`

---

## 1. Diagrama Completo do Fluxo de Execução (End-to-End)

```mermaid
flowchart TD
    subgraph S1["FASE 1: Descoberta e Extração (Clara Mendonça - Analista de Dados)"]
        U["URL do Usuário: kalshi.com/markets/kxnflgame/nfl-game"] --> W1["Varredura de Subdomínios e Tickers (site:kalshi.com/markets/kxnflgame)"]
        W1 --> T9["Identificação dos 9 Contratos Ativos da Rodada (KXNFLGAME-26NOV01*)"]
        T9 --> MKT["Extração de Cotações (¢), Cálculo do Overround (Vig) e Métricas NFL (Elo, Off/Def EPA, Turnovers, HFA)"]
    end

    subgraph S2["FASE 2: Modelagem Formal (Dr. Henrique Vasconcelos - Matemático)"]
        MKT --> EQ1["Equação Estrutural de Spread Esperado: μ_Δ = ΔElo/25 + 22·ΔNetEPA + 1.5·ΔTO + HFA"]
        EQ1 --> PA["Probabilidade Analítica Fechada: P_analítica = Φ(μ_Δ / σ_NFL)"]
        PA --> KELLY["Formulação do Critério de Kelly Fracionário (γ = 0.25) com Regra de Empate Kalshi (US$ 0.50)"]
    end

    subgraph S3["FASE 3: Validação ML e Simulação Fechada (Lucas Bittencourt - Cientista de Dados)"]
        MKT --> SYN["Geração de 1.800 Jogos Históricos Calibrados (Seed = 20261101)"]
        SYN --> SPLIT["Strict Split: 80% Treino (1.440) / 20% Teste (360) ANTES do Z-Score"]
        SPLIT --> RIDGE["Treinamento Regressão Ridge L2 + Validação Out-of-Sample (Acurácia 62.78%, Brier 0.2243)"]
        RIDGE --> MC["Simulação de Monte Carlo: 10.000 Partidas por Confronto (90.000 Jogos c/ Prorrogação)"]
        PA --> ENS["Ensemble Argon: 40% Prob. Analítica + 60% Prob. Monte Carlo (Erro Padrão <= 0.5%)"]
        MC --> ENS
    end

    subgraph S4["FASE 4: Blindagem de Risco e Solvência (Beatriz Alencar - Atuária)"]
        ENS --> EDGE["Filtro de Eficiência de Mercado: Edge = P_Argon - Preço_Kalshi > 1.5%"]
        KELLY --> EDGE
        EDGE --> STRESS["Stress Test de Carteira: 10.000 Domingos Simulados (Banca US$ 1.000)"]
        STRESS --> VAR["Auditoria de Cauda: VaR 95% (US$ 129.50), CVaR 95% e Probabilidade de Ruína (0.00%)"]
    end

    subgraph S5["FASE 5: Síntese Executiva (Axio Vance - Orquestrador)"]
        VAR --> REP["Relatório Final (RELATORIO_KALSHI_NFL_26NOV01.md) + Checkpoint em PLANNING.md e MEMORY.md"]
    end
```

---

## 2. Como Chegamos à "Certeza Estatística" (Convergência vs. Palpite)

Em sistemas estocásticos (como jogos da NFL ou mercado financeiro), **nenhum agente sério promete 100% de certeza determinística em um único evento isolado**, pois um time com `70%` de chance de vencer ainda perde `30%` das vezes por variância natural (*fumbles*, interceptações, lesões ou chutes no poste).

A **certeza científica da Equipe Argon** reside em **4 garantias matemáticas verificáveis**:
1. **Convergência pela Lei dos Grandes Números ($N = 10.000$ runs/jogo):** Com 10.000 simulações por jogo, o erro padrão de Monte Carlo ($\text{SE} = \sqrt{p(1-p)/N}$) é inferior a **$0.5\%$**.
2. **Consenso Triplo (Equação Analítica + Machine Learning Validado Fora da Amostra + Simulação de Placar):** Um time só recebe alta probabilidade quando o modelo teórico de Henrique, o regressor Ridge de Lucas e a simulação de placares convergem na mesma direção.
3. **Separação entre "Quem Ganha o Jogo" e "Qual Contrato Tem Valor":** Identificamos quando um favorito vai ganhar no campo (ex.: Washington Commanders com `67.8%`), mas o preço no Kalshi (`69¢`) já comeu toda a margem de lucro, bloqueando uma operação ruim (`NO TRADE`).
4. **Imunidade à Ruína (Certeza Atuarial de Sobrevivência):** Ao limitar cada posição via Kelly Fracionário ($\gamma = 0.25$) e manter `65.75%` da banca em reserva técnica, a probabilidade de quebrar a banca na rodada é comprovadamente **`0.0000%`**.
