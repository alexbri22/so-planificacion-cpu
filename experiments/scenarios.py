from dataclasses import dataclass
from typing import List
from src.cpu_scheduler import Process
import random

@dataclass
class Scenario:
    """
    Modelo de escenario para la simulación de CPU.
    """
    name: str
    description: str
    processes: List[Process]

def scenario_batch_jobs() -> Scenario:
    """
    Todos llegan al tiempo 0, ráfagas muy distintas.
    Sirve para ver cómo SJF reduce el tiempo promedio frente a FCFS, y cómo RR se comporta intermedio.
    """
    procs = [
        Process(pid=1, arrival=0, burst=2),
        Process(pid=2, arrival=0, burst=4),
        Process(pid=3, arrival=0, burst=8),
        Process(pid=4, arrival=0, burst=16),
    ]
    return Scenario(
        name="batch_jobs",
        description="Trabajos tipo batch, todos llegan al tiempo 0 con ráfagas muy distintas.",
        processes=procs,
    )

def scenario_staggered_arrivals() -> Scenario:
    """
    Llegadas escalonadas: sirve para ver el efecto de FCFS vs SJF cuando hay procesos cortos que llegan después.
    """
    procs = [
        Process(pid=1, arrival=0, burst=8),
        Process(pid=2, arrival=2, burst=4),
        Process(pid=3, arrival=4, burst=1),
        Process(pid=4, arrival=6, burst=3),
    ]
    return Scenario(
        name="staggered_arrivals",
        description="Procesos que llegan en distintos tiempos, algunos cortos llegan más tarde.",
        processes=procs,
    )

def scenario_interactive_like() -> Scenario:
    """
    Varios procesos con ráfagas pequeñas y medianas, llegadas cercanas: razonable para ver la ventaja de RR en tiempo de respuesta.
    """
    procs = [
        Process(pid=1, arrival=0, burst=5),
        Process(pid=2, arrival=1, burst=3),
        Process(pid=3, arrival=2, burst=4),
        Process(pid=4, arrival=3, burst=2),
    ]
    return Scenario(
        name="interactive_like",
        description="Carga tipo interactiva: ráfagas pequeñas/medianas y llegadas cercanas.",
        processes=procs,
    )

def _random_scenario(name: str, description: str, n: int, max_arrival: int, min_burst: int, max_burst: int, seed: int) -> Scenario:
    """
    Genera un escenario pseudoaleatorio pero reproducible usando una semilla fija.
    """
    rng = random.Random(seed)
    procs: List[Process] = []

    for pid in range(1, n + 1):
        arrival = rng.randint(0, max_arrival)
        burst = rng.randint(min_burst, max_burst)
        procs.append(Process(pid=pid, arrival=arrival, burst=burst))

    # Ordenamos por tiempo de llegada solo para presentación
    procs.sort(key=lambda p: (p.arrival, p.pid))

    return Scenario(name=name, description=description, processes=procs)

def scenario_random_light_load() -> Scenario:
    """
    Pocos procesos, ráfagas cortas y llegadas en una ventana pequeña.
    """
    return _random_scenario(
        name="random_light_load",
        description="Escenario aleatorio ligero: pocos procesos, ráfagas cortas y llegadas tempranas.",
        n=5,
        max_arrival=5,
        min_burst=1,
        max_burst=6,
        seed=42,
    )

def scenario_random_heavy_load() -> Scenario:
    """
    Más procesos, ráfagas más grandes y llegadas a lo largo de una ventana de tiempo mayor. Simula un sistema más cargado.
    """
    return _random_scenario(
        name="random_heavy_load",
        description="Escenario aleatorio pesado: más procesos, ráfagas medianas/largas y llegadas dispersas.",
        n=10,
        max_arrival=15,
        min_burst=2,
        max_burst=12,
        seed=99,
    )

def all_scenarios() -> List[Scenario]:
    """
    Regresa todos los escenarios definidos.
    """
    return [
        scenario_batch_jobs(),
        scenario_staggered_arrivals(),
        scenario_interactive_like(),
        scenario_random_light_load(),
        scenario_random_heavy_load(),
    ]