import pytest

from experiments.scenarios import (
    all_scenarios,
    scenario_random_light_load,
    scenario_random_heavy_load,
)
def test_all_scenarios_non_empty():
    """
    Todos los escenarios deben tener al menos un proceso.
    """
    scenarios = all_scenarios()
    assert len(scenarios) >= 5  # sabemos que definimos 5

    for s in scenarios:
        assert s.name  # nombre no vacío
        assert s.processes  # lista no vacía
        # todos los procesos deben tener burst y arrival no negativos
        for p in s.processes:
            assert p.burst > 0
            assert p.arrival >= 0

def _snapshot_processes(procs):
    """
    Representación simplificada de una lista de procesos para poder comparar.
    """
    return [(p.pid, p.arrival, p.burst) for p in procs]

def test_random_scenarios_are_deterministic():
    """
    Los escenarios aleatorios deben ser reproducibles: misma semilla => mismos procesos.
    """
    s1_a = scenario_random_light_load()
    s1_b = scenario_random_light_load()

    s2_a = scenario_random_heavy_load()
    s2_b = scenario_random_heavy_load()

    assert _snapshot_processes(s1_a.processes) == _snapshot_processes(s1_b.processes)
    assert _snapshot_processes(s2_a.processes) == _snapshot_processes(s2_b.processes)