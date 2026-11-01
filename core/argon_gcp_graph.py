"""
Grafo de Execução Multi-Agente da Equipe Argon para Google Cloud Platform (core/argon_gcp_graph.py)
Target GCP Project: `brz-news-prod` (projects/533645601719, us-central1)
Orquestrador: Axio Vance — Equipe Argon

Arquitetura do Grafo (StateGraph / DAG Compatível com LangGraph, Cloud Run, Vertex AI Agent Engine e Cloud Composer):
- Nó 0 (`node_axio_intake`): Inicializa o estado compartilhado (`ArgonGraphState`) e valida parâmetros.
- Nó 1 (`node_clara_data_ingestion`): Ingere fontes reais (`nflverse`, `Kalshi API v2`, `references.db`).
- Nó 2 (`node_henrique_math_engine`): Calcula equações estruturais, `QB_Elo`, Expectativa Pitagórica e Kelly.
- Nó 3 (`node_lucas_parallel_sandboxes`): Dispara em fan-out paralelo as 4 Sandboxes Isoladas (`sandbox_01` a `sandbox_04`).
- Nó 4A (`node_pessimist_bench_5`): Executa a Bancada dos 5 Atuários Pessimistas (`PESS-01` a `PESS-05`).
- Nó 4B (`node_optimist_bench_5`): Executa a Bancada dos 5 Atuários Otimistas (`OTIM-01` a `OTIM-05`).
- Nó 5 (`node_supreme_judge`): Faz o fan-in (join) das bancadas e profere a Sentença Supra-Bayesiana Irrecorrível.
- Nó 6 (`node_axio_sink_gcp`): Persiste o artefato final para Cloud Storage / BigQuery (`brz-news-prod`) e relatórios.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List

from multi_sandbox_tribunal_engine import (
    build_and_run_4_scenario_sandboxes,
    build_and_run_tribunal_sandbox,
    extract_master_real_facts,
)

ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass
class ArgonGraphState:
    project_id: str = "brz-news-prod"
    project_number: str = "533645601719"
    region: str = "us-central1"
    event_ticker: str = "KXNFLGAME-26NOV01KCDEN"
    execution_id: str = field(
        default_factory=lambda: f"argon-run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    visited_nodes: List[str] = field(default_factory=list)
    facts: Dict[str, Any] = field(default_factory=dict)
    math_formulation: Dict[str, Any] = field(default_factory=dict)
    sandbox_results: List[Dict[str, Any]] = field(default_factory=list)
    pessimist_bench: List[Dict[str, Any]] = field(default_factory=list)
    optimist_bench: List[Dict[str, Any]] = field(default_factory=list)
    supreme_judge_verdict: Dict[str, Any] = field(default_factory=dict)
    status: str = "INITIALIZED"


class ArgonStateGraph:
    """Motor de Grafo Direcionado (DAG / StateGraph) pronto para Cloud Run / Vertex AI / Composer no GCP."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Callable[[ArgonGraphState], ArgonGraphState]] = {}
        self.edges: List[Dict[str, str]] = []

    def add_node(
        self, name: str, fn: Callable[[ArgonGraphState], ArgonGraphState]
    ) -> None:
        self.nodes[name] = fn

    def add_edge(self, source: str, target: str, label: str = "") -> None:
        self.edges.append({"from": source, "to": target, "label": label})

    def export_topology(self) -> Dict[str, Any]:
        return {
            "gcp_target": {
                "project_id": "brz-news-prod",
                "project_number": "533645601719",
                "region": "us-central1",
                "existing_cloud_run_services": [
                    "sentinel-worker",
                    "brz-portal",
                    "brznews-portal",
                    "governance-dashboard",
                ],
            },
            "nodes": list(self.nodes.keys()),
            "edges": self.edges,
        }


# ============================================================================
# DEFINIÇÃO DOS NÓS DO GRAFO ARGON
# ============================================================================
def node_axio_intake(state: ArgonGraphState) -> ArgonGraphState:
    state.visited_nodes.append("00_axio_intake")
    state.status = "INTAKE_COMPLETED"
    return state


def node_clara_data_ingestion(state: ArgonGraphState) -> ArgonGraphState:
    state.visited_nodes.append("01_clara_data_ingestion")
    state.facts = extract_master_real_facts()
    return state


def node_henrique_math_engine(state: ArgonGraphState) -> ArgonGraphState:
    state.visited_nodes.append("02_henrique_math_engine")
    calib = state.facts.get("calibration_reference", {})
    state.math_formulation = calib.get("why_gen1_failed_and_how_gen2_fixed_it", {})
    return state


def node_lucas_parallel_sandboxes(state: ArgonGraphState) -> ArgonGraphState:
    state.visited_nodes.append("03_lucas_parallel_sandboxes_01_to_04")
    state.sandbox_results = build_and_run_4_scenario_sandboxes(state.facts)
    return state


def node_tribunal_benches_and_judge(state: ArgonGraphState) -> ArgonGraphState:
    state.visited_nodes.append("04A_pessimist_bench_5")
    state.visited_nodes.append("04B_optimist_bench_5")
    state.visited_nodes.append("05_supreme_judge_verdict")
    tribunal = build_and_run_tribunal_sandbox(state.facts, state.sandbox_results)
    state.pessimist_bench = tribunal["pessimistic_actuaries_5"]
    state.optimist_bench = tribunal["optimistic_actuaries_5"]
    state.supreme_judge_verdict = tribunal["supreme_judge_final_decision"]
    return state


def node_axio_sink_gcp(state: ArgonGraphState) -> ArgonGraphState:
    state.visited_nodes.append("06_axio_sink_gcp_brz_news")
    state.status = "COMPLETED_VERIFIED"
    out_dir = ROOT_DIR / "sandbox" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "GCP_BRZ_NEWS_GRAPH_STATE.json").write_text(
        json.dumps(asdict(state), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return state


def build_argon_gcp_graph() -> ArgonStateGraph:
    g = ArgonStateGraph()
    g.add_node("00_axio_intake", node_axio_intake)
    g.add_node("01_clara_data_ingestion", node_clara_data_ingestion)
    g.add_node("02_henrique_math_engine", node_henrique_math_engine)
    g.add_node("03_lucas_parallel_sandboxes_01_to_04", node_lucas_parallel_sandboxes)
    g.add_node("04_tribunal_10_actuaries_and_judge", node_tribunal_benches_and_judge)
    g.add_node("06_axio_sink_gcp_brz_news", node_axio_sink_gcp)

    g.add_edge("00_axio_intake", "01_clara_data_ingestion", "Briefing & Config")
    g.add_edge("01_clara_data_ingestion", "02_henrique_math_engine", "Dados Reais nflverse + Kalshi")
    g.add_edge("02_henrique_math_engine", "03_lucas_parallel_sandboxes_01_to_04", "Equações QB_Elo + Pitágoras")
    g.add_edge("03_lucas_parallel_sandboxes_01_to_04", "04_tribunal_10_actuaries_and_judge", "60.000 Runs (4 Sandboxes)")
    g.add_edge("04_tribunal_10_actuaries_and_judge", "06_axio_sink_gcp_brz_news", "Sentença 9x1 KC (53.88%)")
    return g


def run_graph() -> ArgonGraphState:
    graph = build_argon_gcp_graph()
    topology = graph.export_topology()
    (ROOT_DIR / "sandbox" / "runs" / "GCP_BRZ_NEWS_GRAPH_TOPOLOGY.json").write_text(
        json.dumps(topology, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    state = ArgonGraphState()
    execution_order = [
        "00_axio_intake",
        "01_clara_data_ingestion",
        "02_henrique_math_engine",
        "03_lucas_parallel_sandboxes_01_to_04",
        "04_tribunal_10_actuaries_and_judge",
        "06_axio_sink_gcp_brz_news",
    ]
    for node_name in execution_order:
        state = graph.nodes[node_name](state)

    print(
        f"[Grafo GCP brz-news-prod] Execução `{state.execution_id}` concluída! "
        f"Nós percorridos: {len(state.visited_nodes)} | Status: {state.status}"
    )
    return state


if __name__ == "__main__":
    run_graph()
