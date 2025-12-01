import pytest
from src.cpu_scheduler import Process, simulate_fcfs


def make_procs():
    return [
        Process(pid=1, arrival=0, burst=5),
        Process(pid=2, arrival=2, burst=3),
        Process(pid=3, arrival=4, burst=1),
    ]


def test_fcfs_order_and_times():
    procs = make_procs()
    result = simulate_fcfs(procs)

    # Verificar orden en el timeline
    timeline = [seg[2] for seg in result["timeline"]] 
    assert timeline == [1, 2, 3]

    # Buscar cada proceso en los resultados
    p1 = next(p for p in result["processes"] if p["pid"] == 1)
    p2 = next(p for p in result["processes"] if p["pid"] == 2)
    p3 = next(p for p in result["processes"] if p["pid"] == 3)

    # Valores esperados
    assert p1["waiting"] == 0
    assert p1["turnaround"] == 5
    assert p1["response"] == 0

    assert p2["waiting"] == 3
    assert p2["turnaround"] == 6
    assert p2["response"] == 3

    assert p3["waiting"] == 4
    assert p3["turnaround"] == 5
    assert p3["response"] == 4

    # Promedios
    assert pytest.approx(result["avg_waiting"], rel=1e-6) == (0 + 3 + 4) / 3
    assert pytest.approx(result["avg_turnaround"], rel=1e-6) == (5 + 6 + 5) / 3
    assert pytest.approx(result["avg_response"], rel=1e-6) == (0 + 3 + 4) / 3