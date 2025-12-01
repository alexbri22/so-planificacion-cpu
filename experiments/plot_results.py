import csv
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

RESULTS_CSV = Path("data/results/summary.csv")
OUTPUT_DIR = Path("data/results/plots")

def load_results():
    """Carga el summary.csv generado por run_experiments."""
    rows = []
    with RESULTS_CSV.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "scenario": row["scenario"],
                "algorithm": row["algorithm"],
                "avg_waiting": float(row["avg_waiting"]),
                "avg_turnaround": float(row["avg_turnaround"]),
                "avg_response": float(row["avg_response"]),
            })
    return rows

def group_by_scenario(rows):
    grouped = defaultdict(list)
    for r in rows:
        grouped[r["scenario"]].append(r)
    return grouped

def plot_per_scenario(grouped):
    """
    Para cada escenario genera una figura con tres gráficas de barras: espera, turnaround y respuesta promedio por algoritmo.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    metrics = [
        ("avg_waiting", "Tiempo de espera promedio"),
        ("avg_turnaround", "Turnaround promedio"),
        ("avg_response", "Tiempo de respuesta promedio"),
    ]

    for scenario, rows in grouped.items():
        # Ordenamos por nombre de algoritmo para que salgan siempre igual
        rows = sorted(rows, key=lambda r: r["algorithm"])

        algos = [r["algorithm"] for r in rows]
        x = range(len(algos))

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))

        for ax, (key, title) in zip(axes, metrics):
            values = [r[key] for r in rows]
            ax.bar(x, values)
            ax.set_xticks(list(x))
            ax.set_xticklabels(algos, rotation=45, ha="right")
            ax.set_title(title)
            ax.set_ylabel("Tiempo")

        fig.suptitle(f"Escenario: {scenario}")
        fig.tight_layout()
        outfile = OUTPUT_DIR / f"{scenario}.png"
        fig.savefig(outfile, dpi=200)
        plt.close(fig)
        print(f"Guardada gráfica: {outfile}")

def main():
    rows = load_results()
    grouped = group_by_scenario(rows)
    plot_per_scenario(grouped)

if __name__ == "__main__":
    main()
