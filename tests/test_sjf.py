import pytest
from src.cpu_scheduler import Process, simulate_fcfs, simulate_sjf

def make_procs():
    return [
        Process(pid=1, arrival=0, burst=5),
        Process(pid=2, arrival=2, burst=3),
        Process(pid=3, arrival=4, burst=1),
    ]

def test_sjf_order_and_times():
    procs = make_procs()
    result = simulate_sjf(procs)

    # Orden en el timeline: primero P1, luego P3 (más corto), luego P2
    timeline_pids = [seg[2] for seg in result["timeline"]]
    assert timeline_pids == [1, 3, 2]

    p1 = next(p for p in result["processes"] if p["pid"] == 1)
    p2 = next(p for p in result["processes"] if p["pid"] == 2)
    p3 = next(p for p in result["processes"] if p["pid"] == 3)

    # Valores esperados
    assert p1["waiting"] == 0
    assert p1["turnaround"] == 5
    assert p1["response"] == 0

    assert p2["waiting"] == 4
    assert p2["turnaround"] == 7
    assert p2["response"] == 4

    assert p3["waiting"] == 1
    assert p3["turnaround"] == 2
    assert p3["response"] == 1

    # Promedios
    assert pytest.approx(result["avg_waiting"], rel=1e-6) == (0 + 4 + 1) / 3
    assert pytest.approx(result["avg_turnaround"], rel=1e-6) == (5 + 7 + 2) / 3
    assert pytest.approx(result["avg_response"], rel=1e-6) == (0 + 4 + 1) / 3

def test_sjf_better_avg_wait_than_fcfs():
    """
    SJF debería dar menor tiempo de espera promedio que FCFS
    para el conjunto de procesos de ejemplo.
    """
    procs = make_procs()
    result_fcfs = simulate_fcfs(procs)
    result_sjf = simulate_sjf(procs)

    assert result_sjf["avg_waiting"] < result_fcfs["avg_waiting"]
