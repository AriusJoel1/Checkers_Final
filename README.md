# Checkers Final – Juego de Damas con IA y Paralelismo

Este proyecto implementa un juego de damas por consola con dos inteligencias artificiales enfrentadas entre sí. El objetivo principal es comparar el rendimiento del algoritmo Minimax en su versión secuencial y en una versión paralelizada, aprovechando técnicas de programación concurrente y paralela.

## Características

- Implementación completa de las reglas tradicionales de damas, incluyendo coronación, movimientos legales y capturas.
- Uso del algoritmo **Minimax** con evaluación de tablero y soporte para memoización `@lru_cache` para optimización.
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

![i7-14700](https://github.com/AriusJoel1/Checkers_Final/blob/main/img/im1.jpg)

#### Para una entrada de 25 jugadas con profundidad 6 tenemos:

![](https://github.com/AriusJoel1/Checkers_Final/blob/main/img/im3.jpg)

#### Resultado de tiempo:

![](https://github.com/AriusJoel1/Checkers_Final/blob/main/img/im2.jpg)

#### Funcionalidades implementadas:
  - Movimientos con captura 
  - Movimientos sin captura
  - Fichas en riesgo de ser capturadas
  - Mejor movimiento (Sugerencia IA)


