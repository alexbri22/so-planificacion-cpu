import pytest

from src.cpu_scheduler import Process, simulate_rr


def make_procs_rr():
    """
    Escenario para probar Round Robin con quantum = 2.
    """
    return [
        Process(pid=1, arrival=0, burst=5),
        Process(pid=2, arrival=1, burst=5),
        Process(pid=3, arrival=2, burst=1),
    ]


def test_rr_timeline_and_metrics():
    procs = make_procs_rr()
    result = simulate_rr(procs, quantum=2)

    timeline_pids = [seg[2] for seg in result["timeline"]]

    # Esperamos la alternancia: P1, P2, P3, P1, P2, P1, P2
    assert timeline_pids == [1, 2, 3, 1, 2, 1, 2]

    p1 = next(p for p in result["processes"] if p["pid"] == 1)
    p2 = next(p for p in result["processes"] if p["pid"] == 2)
    p3 = next(p for p in result["processes"] if p["pid"] == 3)

    # Valores esperados
    # P1: llega 0, termina 10, burst 5
    assert p1["waiting"] == 5
    assert p1["turnaround"] == 10
    assert p1["response"] == 0

    # P2: llega 1, termina 11, burst 5
    assert p2["waiting"] == 5
    assert p2["turnaround"] == 10
    assert p2["response"] == 1

    # P3: llega 2, termina 5, burst 1
    assert p3["waiting"] == 2
    assert p3["turnaround"] == 3
    assert p3["response"] == 2

    # Promedios
    assert pytest.approx(result["avg_waiting"], rel=1e-6) == (5 + 5 + 2) / 3
    assert pytest.approx(result["avg_turnaround"], rel=1e-6) == (10 + 10 + 3) / 3
    assert pytest.approx(result["avg_response"], rel=1e-6) == (0 + 1 + 2) / 3