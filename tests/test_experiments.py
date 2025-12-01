import pytest

from experiments.scenarios import all_scenarios
from experiments.run_experiments import run_all_experiments, get_algorithms

def test_run_all_experiments_shape():
    """
    run_all_experiments debe generar una fila por (escenario, algoritmo) con las claves esperadas.
    """
    scenarios = all_scenarios()
    algos = get_algorithms()

    rows = run_all_experiments()

    # número de filas = escenarios * algoritmos
    assert len(rows) == len(scenarios) * len(algos)

    for r in rows:
        # claves mínimas que esperamos en cada fila
        assert "scenario" in r
        assert "algorithm" in r
        assert "avg_waiting" in r
        assert "avg_turnaround" in r
        assert "avg_response" in r

        # tipos razonables
        assert isinstance(r["scenario"], str)
        assert isinstance(r["algorithm"], str)
        assert isinstance(r["avg_waiting"], (int, float))
        assert isinstance(r["avg_turnaround"], (int, float))
        assert isinstance(r["avg_response"], (int, float))
