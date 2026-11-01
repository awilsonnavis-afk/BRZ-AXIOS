"""
Inicializador do Banco de Dados de Referências da Equipe Argon (SQLite + Markdown).
Liderado por: Axio (Orquestrador Programador Sênior)
"""
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
JSON_PATH = BASE_DIR / "referencias_comunidades_canais.json"
DB_PATH = BASE_DIR / "references.db"
MD_PATH = BASE_DIR / "CATALOGO_REFERENCIAS.md"


def build_database() -> None:
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    refs = data["references"]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS reference_sources")
    cur.execute(
        """
        CREATE TABLE reference_sources (
            id TEXT PRIMARY KEY,
            agent_owner TEXT NOT NULL,
            domain TEXT NOT NULL,
            type TEXT NOT NULL,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            language TEXT NOT NULL,
            focus TEXT NOT NULL,
            use_case TEXT NOT NULL
        )
        """
    )

    for r in refs:
        cur.execute(
            """
            INSERT INTO reference_sources (
                id, agent_owner, domain, type, name, url, language, focus, use_case
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r["id"],
                r["agent_owner"],
                r["domain"],
                r["type"],
                r["name"],
                r["url"],
                r["language"],
                r["focus"],
                r["use_case"],
            ),
        )

    conn.commit()
    conn.close()

    # Gera também o Catálogo Markdown para leitura imediata por qualquer LLM
    lines = [
        "# 📚 Banco de Dados de Referências — Equipe Argon",
        "",
        f"> **Mantido por:** {data['metadata']['created_by']}  ",
        f"> **Última Atualização:** {data['metadata']['last_updated']}  ",
        "> **Formatos disponíveis:** `references.db` (SQLite), `referencias_comunidades_canais.json` (JSON) e este catálogo Markdown.",
        "",
        "Este banco de dados reúne as principais **comunidades, fóruns técnicos, redes sociais, instituições e canais do YouTube** (nacionais e internacionais) utilizados pelos agentes para pesquisa de dados, validação metodológica e benchmarking.",
        "",
        "---",
        "",
        "## 🔎 Tabela Geral de Referências por Agente",
        "",
        "| ID | Agente Responsável | Tipo | Nome da Fonte | Idioma | Foco Principal | Aplicação na Equipe |",
        "| :--- | :--- | :--- | :--- | :---: | :--- | :--- |",
    ]

    for r in refs:
        lines.append(
            f"| `{r['id']}` | **{r['agent_owner']}** | {r['type']} | [{r['name']}]({r['url']}) | `{r['language']}` | {r['focus']} | {r['use_case']} |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 🛠️ Como Consultar via SQL (para Agentes de IA)",
            "",
            "```sql",
            "-- Exemplo: Buscar fontes de Ciências Atuariais ou Risco Financeiro",
            "SELECT id, name, type, url, use_case",
            "FROM reference_sources",
            "WHERE agent_owner LIKE '%Beatriz Alencar%';",
            "```",
            "",
        ]
    )

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Banco SQLite criado em: {DB_PATH}")
    print(f"[OK] Catálogo Markdown criado em: {MD_PATH}")
    print(f"[OK] Total de referências indexadas: {len(refs)}")


if __name__ == "__main__":
    build_database()
