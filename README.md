# Simulador de Planificación de CPU

Proyecto final de la materia de Sistemas Operativos.  
Implementa un simulador de planificación de CPU para comparar distintos algoritmos clásicos bajo cargas de trabajo controladas.

Actualmente el simulador incluye:

- Modelo sencillo de proceso (`pid`, tiempo de llegada, ráfaga de CPU, prioridad).
- Implementación de algoritmos de planificación:
  - **First-Come, First-Served (FCFS)**
  - **Shortest Job First (SJF) no expulsivo**
  - **Round Robin (RR)** con quantum configurable
- Cálculo de métricas:
  - Tiempo de espera promedio
  - Tiempo de retorno (_turnaround_) promedio
  - Tiempo de respuesta promedio
- Pruebas unitarias con `pytest` para validar el comportamiento de FCFS, SJF y RR.

Más adelante se agregará:

- **Shortest Remaining Time First (SRTF)** (versión expulsiva de SJF).
- Experimentos comparativos entre algoritmos con distintos escenarios de carga.

---

## Requisitos

- Python 3.12 (o compatible)
- Entorno virtual (`venv`) recomendado
- `pytest` solo si se desea ejecutar las pruebas automatizadas

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/alexbri22/so-planificacion-cpu.git
cd so-planificacion-cpu
```

---

## Crear y activar un entorno virtual (recomendado):

```bash
python3 -m pip install pytest
```

---

## Estructura del proyecto

```text
so-planificacion-cpu/
├─ src/
│  ├─ __init__.py
│  └─ cpu_scheduler.py      # modelo de proceso, algoritmos y utilidades
├─ tests/
│  ├─ test_fcfs.py          # pruebas unitarias para FCFS
│  ├─ test_sjf.py           # pruebas unitarias para SJF no expulsivo
│  └─ test_rr.py            # pruebas unitarias para Round Robin
├─ experiments/             # (futuro) escenarios y scripts de experimentos
├─ data/
│  ├─ inputs/               # (futuro) definiciones de procesos en CSV/JSON
│  └─ results/              # (futuro) resultados de corridas y métricas
├─ docs/                    # reporte escrito del proyecto
├─ README.md
└─ .venv/                   # entorno virtual (no se versiona)
```

---

## Uso

### Ejecutar el simulador con el conjunto de ejemplo

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
python3 src/cpu_scheduler.py
```

El programa ejecuta un conjunto de procesos de ejemplo y muestra los resultados
para:

- **FCFS**

- **SJF no expulsivo**

- **Round Robin** (con un quantum configurado en el código, por ejemplo q = 2)

Para cada algoritmo se imprimen:

- Métricas por proceso (tiempos de inicio, fin, espera, turnaround y respuesta).

- Promedios de las métricas.

- Una línea de tiempo (timeline) con los intervalos de ejecución de cada proceso.

Más adelante se añadirá una interfaz más general para seleccionar algoritmo,
quantum y escenarios de entrada.

---

## Pruebas

Para ejecutar las pruebas unitarias con `pytest`:

```bash
python3 -m pytest
```

Actualmente se incluyen pruebas para:

- Verificar el orden y las métricas de FCFS en un escenario de ejemplo.

- Verificar el comportamiento de SJF (orden de ejecución y métricas).

- Verificar la alternancia y las métricas de Round Robin para un caso con preempción.

---

## Trabajo futuro

- Implementar SRTF (Shortest Remaining Time First) dentro del simulador.

- Definir varios escenarios de carga (procesos cortos/largos, llegadas escalonadas, diferentes quantums).

- Generar tablas y gráficas comparando tiempos de espera, retorno y respuesta entre algoritmos.

- Documentar resultados y conclusiones en el reporte final (docs/).
