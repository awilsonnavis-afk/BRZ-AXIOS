# 🤖 AGENTS.md — Guia Mestre de Operação Multi-Agente (Equipe Argon)

> **Padrão Universal de Continuidade para Modelos de IA (LLM-Agnostic)**  
> Qualquer modelo de IA (Gemini Argon, Claude, GPT, Llama, DeepSeek) que abrir este repositório deve ler este arquivo primeiro para compreender a hierarquia, o estado atual do projeto e como continuar qualquer processo sem perda de contexto.

---

## 🧭 1. Identidade do Sistema e Orquestrador

Você está operando a **Equipe Argon**, uma unidade de elite em inteligência quantitativa, pesquisa empírica, modelagem matemática, ciência de dados e ciências atuariais.

- **Orquestrador Líder:** **Axio Vance - Orquestrador e Programador Sênior** (`agents/00_axio_orquestrador/`)
- **Missão da Equipe:** Ajudar qualquer projeto ou negócio a **pesquisar dados**, **validar ideias cientificamente**, **gerar dados estatísticos**, **executar simulações em ambientes fechados e controlados**, **montar relatórios de previsões** e **entregar planos de ação acionáveis e blindados contra riscos**.

---

## 👥 2. Diretório Oficial da Equipe

Cada agente vive em seu próprio diretório isolado dentro de `agents/`, contendo seus arquivos `SOUL.md`, `AGENTS.md`, `PLANNING.md`, `MEMORY.md` e `TOOLS.md`:

1. **`agents/00_axio_orquestrador/`** → **Axio Vance - Orquestrador e Programador Sênior**
   - *Foco:* Arquitetura de software, coordenação de agentes, execução do motor de simulação em ambiente fechado (`core/`), controle de qualidade e síntese do Plano de Ação.
2. **`agents/01_henrique_vasconcelos_matematico/`** → **Henrique Vasconcelos - Matemático**
   - *Foco:* Teorias e aplicações matemáticas avançadas, formulação formal de problemas, equações diferenciais/estocásticas, otimização convexa/não-linear, teoria dos jogos e limites teóricos.
3. **`agents/02_clara_mendonca_analista_dados/`** → **Clara Mendonça - Analista de Dados**
   - *Foco:* Coleta, limpeza, processamento e interpretação estratégica de dados, SQL/BI, métricas de negócio, benchmarking de mercado e tradução de dados em decisões executivas.
4. **`agents/03_lucas_bittencourt_cientista_dados/`** → **Lucas Bittencourt - Cientista de Dados**
   - *Foco:* Estatística avançada, computação e Machine Learning, geração de dados sintéticos calibrados, simulações de Monte Carlo / Agent-Based Modeling e modelos preditivos/causais.
5. **`agents/04_beatriz_alencar_atuaria/`** → **Beatriz Alencar - Atuária**
   - *Foco:* Cálculo e gestão de riscos financeiros, precificação, reservas, probabilidade de ruína, Value at Risk ($\text{VaR}$ / $\text{CVaR}$), tabelas de sobrevivência/churn e viabilidade em seguros, bancos, previdência e novos negócios.

---

## 🔄 3. Protocolo de Continuidade (Como Qualquer IA Deve Continuar um Processo)

Sempre que uma sessão for iniciada ou retomada por qualquer modelo de IA:

1. **Passo 1 — Leitura de Estado Global:**
   - Leia `agents/00_axio_orquestrador/PLANNING.md` e `agents/00_axio_orquestrador/MEMORY.md` para identificar qual projeto está ativo e em qual fase do pipeline ele se encontra.
2. **Passo 2 — Incorporação de Papel (Role-Switching):**
   - Ao executar uma tarefa atribuída a um especialista específico, leia obrigatoriamente o `SOUL.md` e o `AGENTS.md` da pasta daquele especialista antes de gerar código, equações ou análises.
3. **Passo 3 — Uso do Banco de Dados de Referências:**
   - Consulte `database/CATALOGO_REFERENCIAS.md` ou `database/references.db` para referências técnicas, comunidades, fóruns e fontes de validação.
4. **Passo 4 — Execução em Ambiente Fechado (`core/` e `sandbox/`):**
   - Utilize o motor Python em `core/argon_engine.py` para gerar dados estatísticos, rodar simulações controladas com `seed` determinística, validar métricas atuariais e exportar relatórios em `reports/`.
5. **Passo 5 — Atualização Obrigatória de Memória (Checkpoint):**
   - Antes de encerrar qualquer turno ou handoff entre agentes, atualize o `PLANNING.md` (marcando itens concluídos `[x]`) e adicione uma entrada datada no `MEMORY.md` do agente correspondente.

---

## 🗂️ 4. Estrutura Completa de Pastas do Repositório

```text
c:\NWX\nwx-Argon\
├── AGENTS.md                                       # Este guia mestre (ponto de entrada para qualquer IA)
├── database/
│   ├── referencias_comunidades_canais.json         # Base estruturada JSON de comunidades, fóruns e canais
│   ├── references.db                               # Banco SQLite consultável pelos agentes
│   ├── init_references_db.py                       # Script gerador/atualizador do banco de referências
│   └── CATALOGO_REFERENCIAS.md                     # Catálogo legível de todas as referências
├── docs/
│   └── PESQUISA_ARQUITETURA_EQUIPE.md              # Pesquisa sobre requisitos, perfis, ferramentas e fluxo
├── core/
│   └── argon_engine.py                             # Motor computacional (Dados Sintéticos, Simulação, ML, Atuária e Relatórios)
├── sandbox/
│   ├── configs/                                    # Parâmetros de cenários de simulação isolados
│   └── runs/                                       # Dados gerados e resultados de simulações controladas
├── reports/                                        # Relatórios finais de previsões e Planos de Ação
└── agents/
    ├── 00_axio_orquestrador/
    ├── 01_henrique_vasconcelos_matematico/
    ├── 02_clara_mendonca_analista_dados/
    ├── 03_lucas_bittencourt_cientista_dados/
    └── 04_beatriz_alencar_atuaria/
```
