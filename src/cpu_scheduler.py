from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from collections import deque

@dataclass
class Process:
    """
    Modelo de proceso para la simulación de CPU.
    """
    pid: int # identificador del proceso
    arrival: int # tiempo de llegada
    burst: int # ráfaga total de CPU
    priority: int = 0 # prioridad

    start_time: int = field(default=-1) # momento en que el proceso empieza a ejecutarse por primera vez
    completion_time: int = field(default=-1) # momento en que termina el proceso
    remaining: int = field(init=False) # tiempo de CPU que le falta al proceso

    def __post_init__(self) -> None:
        # Al inicio, todo el burst está pendiente
        self.remaining = self.burst

def compute_metrics(processes: List[Process]) -> Dict[str, Any]:
    """
    Funcion para calcular metricas de los procesos a partir de su start_time y completion_time.
    Calcula waiting, turnaround y response, y también los promedios.
    """
    results = []
    total_wait = total_turn = total_resp = 0

    for p in processes:
        turnaround = p.completion_time - p.arrival # T_i
        waiting = turnaround - p.burst # W_i
        response = p.start_time - p.arrival # R_i

        total_wait += waiting
        total_turn += turnaround
        total_resp += response

        results.append({
            "pid": p.pid,
            "arrival": p.arrival,
            "burst": p.burst,
            "start": p.start_time,
            "completion": p.completion_time,
            "waiting": waiting,
            "turnaround": turnaround,
            "response": response,
        })

    n = len(processes)
    return {
        "processes": results,
        "avg_waiting": total_wait / n,
        "avg_turnaround": total_turn / n,
        "avg_response": total_resp / n,
    }

def simulate_fcfs(original: List[Process]) -> Dict[str, Any]:
    """
    Simula el algoritmo de planificación FIRST-COME, FIRST-SERVED.

    Regresa:
      - algorithm: nombre del algoritmo
      - timeline: lista de segmentos (inicio, fin, pid | None)
      - processes: métricas por proceso
      - avg_waiting, avg_turnaround, avg_response
    """

    # Creamos una copia para no modificar la lista original y ordenamos por tiempo de llegada
    processes = [Process(pid=p.pid, arrival=p.arrival, burst=p.burst, priority=p.priority) for p in original]
    processes = sorted(processes, key=lambda p: (p.arrival, p.pid))

    time = 0
    timeline: List[tuple[int, int, Optional[int]]] = []

    for p in processes:
        # Verificamos si la CPU está libre hasta que llegua el proceso
        if time < p.arrival:
            timeline.append((time, p.arrival, None)) 
            time = p.arrival

        p.start_time = time
        time += p.burst
        p.completion_time = time
        timeline.append((p.start_time, p.completion_time, p.pid))

    metrics = compute_metrics(processes)

    return {
        "algorithm": "FCFS",
        "timeline": timeline,
        **metrics,
    }

def simulate_sjf(original: List[Process]) -> Dict[str, Any]:
    """
    Simula planificación SHORTEST JOB FIRST no expulsiva.

    Regresa:
      - algorithm: nombre del algoritmo
      - timeline: lista de segmentos (inicio, fin, pid | None)
      - processes: métricas por proceso
      - avg_waiting, avg_turnaround, avg_response
    """

    # Copiamos solo los campos de entrada para no modificar los originales
    processes = [Process(pid=p.pid, arrival=p.arrival, burst=p.burst, priority=p.priority) for p in original]

    n = len(processes)
    completed = 0
    time = 0
    timeline: List[tuple[int, int, Optional[int]]] = []

    # Mientras haya procesos sin completar
    while completed < n:
        # Procesos listos
        ready = [p for p in processes if p.arrival <= time and p.completion_time == -1]

        if not ready:
            # No hay procesos listos: CPU libre hasta el siguiente arrival
            next_arrival = min(p.arrival for p in processes if p.completion_time == -1)
            if time < next_arrival:
                timeline.append((time, next_arrival, None))
                time = next_arrival
            continue

        # Elegimos el proceso con ráfaga más corta
        p = min(ready, key=lambda x: (x.burst, x.arrival, x.pid))

        p.start_time = time
        time += p.burst
        p.completion_time = time
        completed += 1

        timeline.append((p.start_time, p.completion_time, p.pid))

    metrics = compute_metrics(processes)

    return {
        "algorithm": "SJF (non-preemptive)",
        "timeline": timeline,
        **metrics,
    }

def simulate_rr(original: List[Process], quantum: int) -> Dict[str, Any]:
    """
    Simula planificación ROUND ROBIN con quantum fijo.

    Regresa:
      - algorithm: nombre del algoritmo
      - timeline: lista de segmentos (inicio, fin, pid | None)
      - processes: métricas por proceso
      - avg_waiting, avg_turnaround, avg_response
    """
    if quantum <= 0:
        raise ValueError("El quantum debe ser un entero positivo")

    # Copiamos procesos para no modificar los originales
    processes = [Process(pid=p.pid, arrival=p.arrival, burst=p.burst, priority=p.priority) for p in original]
    procs_sorted = sorted(processes, key=lambda p: (p.arrival, p.pid))

    n = len(procs_sorted)
    completed = 0
    time = 0
    i = 0  # índice de procesos ordenados por llegada
    ready: deque[Process] = deque()
    timeline: List[tuple[int, int, Optional[int]]] = []

    while completed < n:
        # Agregar a la cola listos todos los procesos que ya llegaron
        while i < n and procs_sorted[i].arrival <= time:
            ready.append(procs_sorted[i])
            i += 1

        if not ready:
            # CPU libre hasta el siguiente arrival
            next_arrival = procs_sorted[i].arrival
            if time < next_arrival:
                timeline.append((time, next_arrival, None))
                time = next_arrival
            continue

        # Tomar el siguiente proceso de la cola circular
        p = ready.popleft()

        # Si es la primera vez que entra a CPU, registramos su start time
        if p.start_time == -1:
            p.start_time = time  

        start = time
        run_time = min(quantum, p.remaining)
        time += run_time
        p.remaining -= run_time

        timeline.append((start, time, p.pid))

        # Durante este quantum pudieron llegar procesos nuevos
        while i < n and procs_sorted[i].arrival <= time:
            ready.append(procs_sorted[i])
            i += 1

        if p.remaining == 0:
            p.completion_time = time
            completed += 1
        else:
            # Todavía le falta burst: va al final de la cola
            ready.append(p)

    metrics = compute_metrics(processes)

    return {
        "algorithm": f"Round Robin (q={quantum})",
        "timeline": timeline,
        **metrics,
    }

def demo_processes() -> List[Process]:
    """Conjunto de procesos de ejemplo para probar el simulador."""
    return [
        Process(pid=1, arrival=0, burst=5),
        Process(pid=2, arrival=2, burst=3),
        Process(pid=3, arrival=4, burst=1),
    ]

def print_results(result: Dict[str, Any]) -> None:
    """Imprime los resultados de forma legible."""
    print(f"=== {result['algorithm']} ===")
    print("\nProcesos:")
    for p in result["processes"]:
        print(
            f"P{p['pid']}: llegada={p['arrival']}, burst={p['burst']}, "
            f"inicio={p['start']}, fin={p['completion']}, "
            f"espera={p['waiting']}, turnaround={p['turnaround']}, "
            f"respuesta={p['response']}"
        )
    print("\nPromedios:")
    print(f"  Espera    : {result['avg_waiting']:.2f}")
    print(f"  Turnaround: {result['avg_turnaround']:.2f}")
    print(f"  Respuesta : {result['avg_response']:.2f}")
    print("\nTimeline:")
    for start, end, pid in result["timeline"]:
        label = f"P{pid}" if pid is not None else "IDLE"
        print(f"  [{start:2d}, {end:2d}) -> {label}")

if __name__ == "__main__":
    procs = demo_processes()

    # FCFS
    result_fcfs = simulate_fcfs(procs)
    print_results(result_fcfs)
    print("\n" + "=" * 60 + "\n")

    # SJF no expulsivo
    result_sjf = simulate_sjf(procs)
    print_results(result_sjf)
    print("\n" + "=" * 60 + "\n")

    # Round Robin con quantum 2
    result_rr = simulate_rr(procs, quantum=2)
    print_results(result_rr)