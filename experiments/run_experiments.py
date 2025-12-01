from typing import Callable, List, Dict, Any
import csv
from pathlib import Path
from src.cpu_scheduler import Process, simulate_fcfs, simulate_sjf, simulate_rr, simulate_srtf
from experiments.scenarios import all_scenarios, Scenario

AlgorithmFn = Callable[[List[Process]], Dict[str, Any]]

def get_algorithms() -> List[tuple[str, AlgorithmFn]]:
    """
    Lista de algoritmos a comparar.
    """
    return [
        ("FCFS", simulate_fcfs),
        ("SJF", simulate_sjf),
        ("SRTF", simulate_srtf),
        ("RR_q2", lambda procs: simulate_rr(procs, quantum=2)),
    ]

def run_all_experiments() -> List[Dict[str, Any]]:
    """
    Ejecuta todos los algoritmos en todos los escenarios y regresa una lista de filas con métricas promedio.
    """
    rows: List[Dict[str, Any]] = []

    for scenario in all_scenarios():
        for name, fn in get_algorithms():
            result = fn(scenario.processes)
            rows.append(
                {
                    "scenario": scenario.name,
                    "algorithm": name,
                    "avg_waiting": result["avg_waiting"],
                    "avg_turnaround": result["avg_turnaround"],
                    "avg_response": result["avg_response"],
                }
            )

    return rows

def print_markdown_table(rows: List[Dict[str, Any]]) -> None:
    """
    Utilidad para imprimir una tabla de resultados en formato Markdown
    """
    print("| Escenario | Algoritmo | Espera prom. | Turnaround prom. | Respuesta prom. |")
    print("|-----------|-----------|--------------|-------------------|-----------------|")
    for r in rows:
        print(
            f"| {r['scenario']} | {r['algorithm']} | "
            f"{r['avg_waiting']:.2f} | {r['avg_turnaround']:.2f} | {r['avg_response']:.2f} |"
        )

def save_csv(rows: List[Dict[str, Any]], path: str = "data/results/summary.csv") -> None:
    """
    Guarda los resultados en un CSV para análisis posterior.
    """
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["scenario", "algorithm", "avg_waiting", "avg_turnaround", "avg_response"]
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Resultados guardados en {out_path}")

if __name__ == "__main__":
    rows = run_all_experiments()
    print_markdown_table(rows)
    save_csv(rows)