from src.cpu_scheduler import Process, simulate_srtf

def test_srtf_preempts_long_job():
    """
    Escenario donde SRTF mejora claramente a SJF:
    - P1 largo llega primero
    - P2 y P3 más cortos llegan después y deben preemptar
    """
    processes = [
        Process(pid="P1", arrival=0, burst=8),
        Process(pid="P2", arrival=1, burst=4),
        Process(pid="P3", arrival=2, burst=1),
    ]

    result = simulate_srtf(processes)
    procs = {p["pid"]: p for p in result["processes"]}

    # Tiempos esperados:
    # P1: C=13, W=5
    # P2: C=6,  W=1
    # P3: C=3,  W=0

    p1 = procs["P1"]
    p2 = procs["P2"]
    p3 = procs["P3"]

    # Comprobamos tiempos de finalización
    assert p1["completion"] == 13
    assert p2["completion"] == 6
    assert p3["completion"] == 3

    assert p1["waiting"] == 5
    assert p2["waiting"] == 1
    assert p3["waiting"] == 0

    # Checamos que nadie se quede sin start_time
    assert p1["start"] == 0
    assert p2["start"] == 1
    assert p3["start"] == 2

    # Timeline debería reflejar expulsiones (P1 -> P2 -> P3 -> P2 -> P1)
    timeline_pids = [pid for _, _, pid in result["timeline"]]
    assert timeline_pids[0] == "P1"
    assert "P2" in timeline_pids
    assert "P3" in timeline_pids