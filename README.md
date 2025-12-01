# Simulador de Planificación de CPU

Proyecto final de la materia de Sistemas Operativos.  
Implementa un simulador de planificación de CPU para comparar distintos algoritmos clásicos bajo cargas de trabajo controladas.

Actualmente el simulador incluye:

- Modelo sencillo de proceso (`pid`, tiempo de llegada, ráfaga de CPU, prioridad).
- Implementación de algoritmos de planificación:
  - **First-Come, First-Served (FCFS)**
  - **Shortest Job First (SJF) no expulsivo**
  - **Shortest Remaining Time First (SRTF)** (versión expulsiva de SJF)
  - **Round Robin (RR)** con quantum configurable
- Conjunto de escenarios de carga:
  - Escenarios diseñados a mano (batch, llegadas escalonadas, carga interactiva).
  - Escenarios pseudoaleatorios con semilla fija para garantizar reproducibilidad.
- Módulo de experimentos que ejecuta todos los algoritmos sobre todos los escenarios
  y genera un resumen de métricas promedio (tabla y archivo CSV).
- Cálculo de métricas:
  - Tiempo de espera promedio
  - Tiempo de retorno (_turnaround_) promedio
  - Tiempo de respuesta promedio
- Pruebas unitarias con `pytest` para validar:
  - El comportamiento de FCFS, SJF, SRTF y RR.
  - La coherencia y reproducibilidad de los escenarios y del módulo de experimentos.
- Un comparador interactivo en el simulador principal que calcula un **ranking de algoritmos**
  (1 = mejor) por cada métrica y un **score global** (suma de rangos).
- Un script de visualización que genera **gráficas de barras** por escenario a partir de `data/results/summary.csv`.

---

## Requisitos

- Python 3.12 (o compatible)
- Entorno virtual (`venv`) recomendado
- `pytest` si se desean ejecutar las pruebas automatizadas
- `matplotlib` solo si se desean generar las gráficas a partir de los resultados

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/alexbri22/so-planificacion-cpu.git
cd so-planificacion-cpu
```

Instalar `pytest` y `matplotlib` si se desean ejecutar pruebas y gráficas:

```bash
python3 -m pip install pytest matplotlib
```

---

## Crear y activar un entorno virtual (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
```

---

## Estructura del proyecto

````text
so-planificacion-cpu/
├─ src/
│  ├─ __init__.py
│  └─ cpu_scheduler.py      # modelo de proceso, algoritmos, métricas y comparador
├─ tests/
│  ├─ test_fcfs.py          # pruebas unitarias para FCFS
│  ├─ test_sjf.py           # pruebas unitarias para SJF no expulsivo
│  ├─ test_rr.py            # pruebas unitarias para Round Robin
│  ├─ test_srtf.py          # pruebas unitarias para SRTF
│  ├─ test_scenarios.py     # pruebas para escenarios (aleatorios y fijos)
│  └─ test_experiments.py   # pruebas para el módulo de experimentos
├─ experiments/
│  ├─ __init__.py
│  ├─ scenarios.py          # definición de escenarios de carga
│  ├─ run_experiments.py    # script que ejecuta y resume los experimentos
│  └─ plot_results.py       # genera gráficas a partir de data/results/summary.csv
├─ data/
│  ├─ inputs/               # (futuro) definiciones de procesos en CSV/JSON
│  └─ results/
│     ├─ summary.csv        # resumen de resultados promedio por escenario/algoritmo
│     └─ plots/             # gráficas generadas por plot_results.py
│        ├─ batch_jobs.png
│        ├─ staggered_arrivals.png
│        ├─ interactive_like.png
│        ├─ random_light_load.png
│        └─ random_heavy_load.png
├─ docs/                    # reporte escrito del proyecto
├─ README.md
└─ .venv/                   # entorno virtual (no se versiona)

---

## Uso

### Ejecutar el simulador con el conjunto de ejemplo

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
python3 src/cpu_scheduler.py
````

El programa ejecuta un conjunto de procesos de ejemplo y muestra los resultados
para:

- **FCFS**

- **SJF no expulsivo**

- **Round Robin** (con un quantum configurado en el código, por ejemplo q = 2)

- **Shortest Remaining Time First (SRTF)** (versión expulsiva de SJF).

Para cada algoritmo se imprimen:

- Métricas por proceso (tiempos de inicio, fin, espera, turnaround y respuesta).

- Promedios de las métricas.

- Una línea de tiempo (timeline) con los intervalos de ejecución de cada proceso.

Al final, el simulador muestra también una tabla comparativa:

- ranking por tiempo de espera promedio,

- ranking por tiempo de turnaround promedio,

- ranking por tiempo de respuesta promedio,

- y un score global (suma de rangos; menor score = mejor algoritmo en ese escenario).

Esto permite ver rápidamente qué algoritmo se comporta mejor en el conjunto de procesos de ejemplo.

Más adelante se podría añadir una interfaz más general para seleccionar algoritmo, quantum y escenarios de entrada.

## Ejecutar experimentos comparativos

Para correr todos los algoritmos en todos los escenarios definidos y obtener
un resumen de métricas promedio:

```bash
python3 -m experiments.run_experiments
```

Este comando:

- Ejecuta FCFS, SJF, SRTF y RR (q = 2) en cada escenario.

- Imprime en la terminal una tabla en formato Markdown con:

  - tiempo de espera promedio,

  - tiempo de turnaround promedio,

  - tiempo de respuesta promedio.

- Guarda los mismos datos en el archivo data/results/summary.csv, listo para ser usado en el reporte o en herramientas externas (Excel, Python, etc.).

Los escenarios pseudoaleatorios se generan con semillas fijas, por lo que los
resultados son reproducibles entre ejecuciones.

---

## Pruebas

Para ejecutar las pruebas unitarias con `pytest`:

```bash
python3 -m pytest
```

Actualmente se incluyen pruebas para:

- Verificar el orden y las métricas de FCFS, SJF, SRTF y Round Robin en escenarios específicos.

- Comprobar que todos los escenarios de carga estén bien formados y que los escenarios aleatorios sean deterministas (misma semilla ⇒ mismos procesos).

- Asegurar que el módulo de experimentos (`run_experiments`) genere una fila coherente por cada combinación escenario–algoritmo.

---

## Trabajo futuro

- Explorar distintos valores de quantum para Round Robin y comparar su impacto.

- Añadir visualizaciones (gráficas) a partir de data/results/summary.csv.

- Extender el análisis a más métricas (por ejemplo, número de cambios de contexto o utilización de la CPU).
