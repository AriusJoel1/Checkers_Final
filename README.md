# Checkers Final – Juego de Damas con IA y Paralelismo

Este proyecto implementa un juego de damas por consola con dos inteligencias artificiales enfrentadas entre sí. El objetivo principal es comparar el rendimiento del algoritmo Minimax en su versión secuencial y en una versión paralelizada, aprovechando técnicas de programación concurrente y paralela.

## Características

- Implementación completa de las reglas tradicionales de damas, incluyendo coronación, movimientos legales y capturas.
- Uso del algoritmo **Minimax** con evaluación de tablero y soporte para memoización (`@lru_cache`) para optimización.
- Evaluación de jugadas usando:
  - **Paralelismo con hilos (ThreadPoolExecutor)** para calcular los movimientos posibles de cada ficha simultáneamente.
  - **Paralelismo real con múltiples procesos (ProcessPoolExecutor)** para evaluar cada rama del Minimax en núcleos distintos, mejorando el rendimiento computacional.
- Clasificación detallada de jugadas:
  - Movimientos con y sin captura
  - Fichas en riesgo de ser capturadas
  - Mejor movimiento (Sugerencia IA)
    
## Comparación de rendimiento

El programa simula varios turnos entre dos IAs (blancas vs negras), y al finalizar muestra un resumen del tiempo total de ejecución tanto para el enfoque secuencial como el paralelo.

#### Ejecución

```bash
# Recomendacion profundidad 4
python checkers_automatico.py
```

### Programación secuencial

- Algoritmo Minimax tradicional recursivo.
- Cálculo de posibles movimientos en serie (uno por uno).
- Utiliza memoización.

### Programación paralela

- Algoritmo Minimax distribuido por procesos (`ProcessPoolExecutor`), permitiendo usar múltiples núcleos.
- Cálculo en paralelo de:
  - Posibles movimientos por ficha (ThreadPoolExecutor), permitiendo calcularlos en paralelo usando múltiples hilos
  - Evaluación de ramas del árbol Minimax (una por proceso)
- Utiliza memoización.
- Mejora significativa del rendimiento para profundidades altas.

### Resultado
Este programa fue probado con una profundidad de 6, lo que significa que la IA calcula hasta 6 movimientos futuros por rama de decisión (considerando tanto jugadas propias como del oponente).

Las pruebas se realizaron en un procesador Intel Core i7-14700, aprovechando casi todos sus núcleos e hilos gracias a la ejecución paralela con ProcessPoolExecutor. Esto permitió observar mejoras notables en rendimiento frente a la versión secuencial, especialmente en turnos con muchas posibilidades de movimiento.





















Iniciamos el juego

![](https://github.com/AriusJoel1/JuegoDeDamas/blob/main/img/1.png)


Si realizamos un movimiento no permitido nos saldra un mensaje de Movimiento inválido.

![](https://github.com/AriusJoel1/JuegoDeDamas/blob/main/img/2.png)


Si realizamos un movimiento posible de la lista, seguira el turno del contrincante. 

![](https://github.com/AriusJoel1/JuegoDeDamas/blob/main/img/3.png)

## Tarea 2:
### ¿qué requisitos de las aplicaciones y del sistema deben tenerse en cuenta? 

Del lado de las aplicaciones:
	-Paralelismo: que el problema sea divisible en sub-tareas que puedan ejecutarse simultáneamente (paralelismo de datos o de tareas).
  -Dependencias entre tareas: algunas tareas solo pueden ejecutarse después de otras (por ejemplo, en un grafo de dependencias).
	-Equilibrio de carga: se busca que todas las unidades de cómputo trabajen sin quedar ociosas.
	-Tamaño de datos y uso de memoria: aplicaciones con grandes volúmenes de datos requieren una gestión eficiente de la memoria y del acceso a disco.
	-Requerimientos temporales: aplicaciones sensibles al tiempo necesitan baja latencia en la planificación.
	-Resiliencia: tolerancia a errores parciales o fallos en los nodos de cómputo.
Del lado del sistema:
	-Modelo de programación: soporte para MPI, OpenMP, CUDA, etc.
	-Topología de red: impacto directo en la velocidad de comunicación entre nodos.
	-Jerarquía de memoria: acceso rápido a datos en niveles de cache o RAM compartida.
	-Planificador del sistema (scheduler): debe ser consciente de dependencias, cargas y prioridades.
	-Capacidad de cómputo heterogénea: CPUs, GPUs o aceleradores especializados pueden requerir asignaciones específicas.
