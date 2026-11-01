# 🛠️ TOOLS.md — Arsenal Técnico de Axio Vance (Orquestrador)

## 1. Ferramentas de Orquestração e Engenharia
- **Motor Central Argon (`core/argon_engine.py`):**
  - Executa geração de dados sintéticos, simulação controlada em sandbox, análise estatística, modelagem preditiva, avaliação atuarial e geração automatizada de relatórios.
  - Comando padrão:
    ```powershell
    python core/argon_engine.py --config sandbox/configs/default_project.json
    ```
- **Banco de Dados de Referências (`database/references.db`):**
  - Inicialização/Atualização:
    ```powershell
    python database/init_references_db.py
    ```
- **Controle de Estado Multi-Agente:**
  - Leitura e escrita coordenada nos arquivos `PLANNING.md`, `MEMORY.md` e `outputs/` de cada especialista em `agents/`.
