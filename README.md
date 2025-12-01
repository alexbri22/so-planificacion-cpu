# Simulador de Planificación de CPU

Proyecto final de la materia de Sistemas Operativos.  
Implementa un simulador de planificación de CPU para comparar distintos algoritmos clásicos bajo cargas de trabajo controladas.

Actualmente el simulador incluye:

- Modelo sencillo de proceso (`pid`, tiempo de llegada, ráfaga de CPU, prioridad).
- Implementación de algoritmos de planificación:
  - **First-Come, First-Served (FCFS)**
  - **Shortest Job First (SJF) no expulsivo**
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
  - El comportamiento de FCFS, SJF y RR.
  - La coherencia y reproducibilidad de los escenarios y del módulo de experimentos.

Más adelante se podría agregar:

- **Shortest Remaining Time First (SRTF)** (versión expulsiva de SJF).
- Más escenarios y visualizaciones (gráficas) sobre los resultados experimentales.

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
│  ├─ test_rr.py            # pruebas unitarias para Round Robin
│  ├─ test_scenarios.py     # pruebas para escenarios (aleatorios y fijos)
│  └─ test_experiments.py   # pruebas para el módulo de experimentos
├─ experiments/
│  ├─ __init__.py
│  ├─ scenarios.py          # definición de escenarios de carga
│  └─ run_experiments.py    # script que ejecuta y resume los experimentos
├─ data/
│  ├─ inputs/               # (futuro) definiciones de procesos en CSV/JSON
│  └─ results/
│     └─ summary.csv        # resumen de resultados promedio por escenario/algoritmo
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

## Ejecutar experimentos comparativos

Para correr todos los algoritmos en todos los escenarios definidos y obtener
un resumen de métricas promedio:

```bash
python3 -m experiments.run_experiments
```

Este comando:

- Ejecuta FCFS, SJF y RR (con q = 2) en cada escenario.

- Imprime en la terminal una tabla en formato Markdown con:

  - tiempo de espera promedio,

  - tiempo de turnaround promedio,

  - tiempo de respuesta promedio.

- Guarda los mismos datos en el archivo data/results/summary.csv, listo para
  ser usado en el reporte o en herramientas externas (Excel, Python, etc.).

Los escenarios pseudoaleatorios se generan con semillas fijas, por lo que los
resultados son reproducibles entre ejecuciones.

---

## Pruebas

Para ejecutar las pruebas unitarias con `pytest`:

```bash
python3 -m pytest
```

Actualmente se incluyen pruebas para:

- Verificar el orden y las métricas de FCFS, SJF y Round Robin en escenarios específicos.

- Comprobar que todos los escenarios de carga estén bien formados y que los escenarios aleatorios sean deterministas (misma semilla ⇒ mismos procesos).

- Asegurar que el módulo de experimentos (`run_experiments`) genere una fila coherente por cada combinación escenario–algoritmo.

---

## Trabajo futuro

- Implementar SRTF (Shortest Remaining Time First) dentro del simulador.

- Explorar distintos valores de quantum para Round Robin y comparar su impacto.

- Añadir visualizaciones (gráficas) a partir de data/results/summary.csv.

- Extender el análisis a más métricas (por ejemplo, número de cambios de contexto).
