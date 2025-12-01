# Simulador de Planificación de CPU

Proyecto final de la materia de Sistemas Operativos.  
Implementa un simulador de planificación de CPU para comparar distintos algoritmos clásicos bajo cargas de trabajo controladas.

Actualmente el simulador incluye:

- Modelo sencillo de proceso (`pid`, tiempo de llegada, ráfaga de CPU, prioridad).
- Implementación de algoritmos de planificación:
  - **First-Come, First-Served (FCFS)**
  - **Shortest Job First (SJF) no expulsivo**
- Cálculo de métricas:
  - Tiempo de espera promedio
  - Tiempo de retorno (_turnaround_) promedio
  - Tiempo de respuesta promedio
- Pruebas unitarias básicas con `pytest` para validar el comportamiento de FCFS y SJF.

Más adelante se agregarán:

- **Shortest Remaining Time First (SRTF)**
- **Round Robin (RR)** con quantum configurable
- Experimentos comparativos entre algoritmos

---

## Requisitos

- Python 3.12 (o compatible)
- `virtualenv` (opcional pero recomendado)
- `pytest` para ejecutar las pruebas

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/alexbri22/so-planificacion-cpu.git
cd so-planificacion-cpu
```
