import threading
import copy

def crear_tablero():
    tablero = [[' ' for _ in range(8)] for _ in range(8)]
    for fila in range(3):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'n'
    for fila in range(5, 8):
        for col in range(8):
            if (fila + col) % 2 == 1:
                tablero[fila][col] = 'b'
    return tablero

def imprimir_tablero(tablero):
    print("    A B C D E F G H")
    print("   +++++++++++++++++")
    for idx, fila in enumerate(tablero):
        linea = f"{idx} |"
        for col in fila:
            linea += f" {col if col != ' ' else '.'}"
        linea += " |"
        print(linea)
    print("   +++++++++++++++++")

def coronar(tablero, x, y):
    if tablero[x][y] == 'b' and x == 0:
        tablero[x][y] = 'B'
    elif tablero[x][y] == 'n' and x == 7:
        tablero[x][y] = 'N'

def mover_ficha(tablero, origen, destino, jugador):
    ox, oy = origen
    dx, dy = destino
    pieza = tablero[ox][oy]
    if pieza.lower() != jugador:
        return False
    if tablero[dx][dy] != ' ':
        return False
    direccion = -1 if jugador == 'b' else 1
    if abs(dx - ox) == 1 and abs(dy - oy) == 1 and (dx - ox) == direccion:
        tablero[dx][dy] = pieza
        tablero[ox][oy] = ' '
        coronar(tablero, dx, dy)
        return True
    if abs(dx - ox) == 2 and abs(dy - oy) == 2:
        mx, my = (ox + dx) // 2, (oy + dy) // 2
        enemigo = 'n' if jugador == 'b' else 'b'
        if tablero[mx][my].lower() == enemigo:
            tablero[dx][dy] = pieza
            tablero[ox][oy] = ' '
            tablero[mx][my] = ' '
            coronar(tablero, dx, dy)
            return True
    return False

def parsear_movimiento(texto):
    m = texto.replace('-', '').replace(' ', '').upper()
    if len(m) != 4:
        raise ValueError("Formato inválido")
    letras = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
    oy = letras.get(m[0])
    ox = int(m[1])
    dy = letras.get(m[2])
    dx = int(m[3])
    if oy is None or dy is None:
        raise ValueError("Letra inválida")
    if not (0 <= ox < 8 and 0 <= dx < 8):
        raise ValueError("Fila fuera de rango")
    return (ox, oy), (dx, dy)

def calcular_movimientos(tablero, origen):
    ox, oy = origen
    pieza = tablero[ox][oy]
    if pieza == ' ':
        return []
    jugador = pieza.lower()
    dirs = [(-1, -1), (-1, 1)] if jugador == 'b' else [(1, -1), (1, 1)]
    if pieza in ('B', 'N'):
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    movimientos = []
    for dx, dy in dirs:
        nx, ny = ox + dx, oy + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and tablero[nx][ny] == ' ':
            movimientos.append(((ox, oy), (nx, ny)))
        cx, cy = ox + 2*dx, oy + 2*dy
        mx, my = ox + dx, oy + dy
        if (0 <= cx < 8 and 0 <= cy < 8 and tablero[cx][cy] == ' ' and
            tablero[mx][my].lower() in ('b', 'n') and tablero[mx][my].lower() != jugador):
            movimientos.append(((ox, oy), (cx, cy)))
    return movimientos

def movimientos_jugador(tablero, jugador):
    todas = []
    for x in range(8):
        for y in range(8):
            if tablero[x][y].lower() == jugador:
                todas.extend(calcular_movimientos(tablero, (x, y)))
    return todas

def es_riesgo(tablero, origen, destino, jugador):
    copia = [fila.copy() for fila in tablero]
    mover_ficha(copia, origen, destino, jugador)
    enemigo = 'n' if jugador == 'b' else 'b'
    for mov in movimientos_jugador(copia, enemigo):
        (ox, oy), (dx, dy) = mov
        if (dx, dy) == destino and abs(dx - ox) == 2:
            return True
    return False

def format_pos(pos):
    x, y = pos
    return f"{chr(y + 65)}{x}"

def evaluar_movimiento(tablero, origen, destino, jugador):
    ox, oy = origen
    dx, dy = destino
    puntaje = 1
    if abs(dx - ox) == 2:
        puntaje += 100
    if jugador == 'b' and dx == 0:
        puntaje += 50
    if jugador == 'n' and dx == 7:
        puntaje += 50
    if es_riesgo(tablero, origen, destino, jugador):
        puntaje -= 20
    return puntaje

def aplicar_movimiento(tablero, origen, destino):
    nuevo = copy.deepcopy(tablero)
    mover_ficha(nuevo, origen, destino, nuevo[origen[0]][origen[1]].lower())
    return nuevo

def minimax(tablero, jugador, profundidad, maximizando):
    enemigo = 'n' if jugador == 'b' else 'b'
    if profundidad == 0:
        return evaluar_tablero(tablero, jugador), None

    movimientos = movimientos_jugador(tablero, jugador if maximizando else enemigo)
    if not movimientos:
        return evaluar_tablero(tablero, jugador), None

    mejor_mov = None
    if maximizando:
        mejor_valor = float('-inf')
        for mov in movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, mov[0], mov[1])
            valor, _ = minimax(nuevo_tablero, jugador, profundidad-1, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        return mejor_valor, mejor_mov
    else:
        mejor_valor = float('inf')
        for mov in movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, mov[0], mov[1])
            valor, _ = minimax(nuevo_tablero, jugador, profundidad-1, True)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        return mejor_valor, mejor_mov

def evaluar_tablero(tablero, jugador):
    enemigo = 'n' if jugador == 'b' else 'b'
    score = 0
    for fila in tablero:
        for celda in fila:
            if celda.lower() == jugador:
                score += 3 if celda.isupper() else 1
            elif celda.lower() == enemigo:
                score -= 3 if celda.isupper() else 1
    return score

def sugerir_mejor_movimiento(tablero, jugador):
    _, mov = minimax(tablero, jugador, profundidad=3, maximizando=True)
    return mov

def juego():
    tablero = crear_tablero()
    turno = 'b'
    while True:
        print(f"\nTurno de {'blancas' if turno == 'b' else 'negras'}")
        imprimir_tablero(tablero)

        movimientos = movimientos_jugador(tablero, turno)
        if not movimientos:
            print("¡No hay movimientos posibles! Fin del juego.")
            break

        capturas, simples, riesgos = [], [], []
        for origen, destino in movimientos:
            if abs(destino[0] - origen[0]) == 2:
                capturas.append((origen, destino))
            else:
                simples.append((origen, destino))
            if es_riesgo(tablero, origen, destino, turno):
                riesgos.append((origen, destino))

        print("Movimientos con captura:", [f"{format_pos(o)}{format_pos(d)}" for o, d in capturas])
        print("Movimientos sin captura:", [f"{format_pos(o)}{format_pos(d)}" for o, d in simples])
        print("Movimientos en riesgo:", [f"{format_pos(o)}{format_pos(d)}" for o, d in riesgos])

        sugerencia = sugerir_mejor_movimiento(tablero, turno)
        if sugerencia:
            print(f" Sugerencia de IA: {format_pos(sugerencia[0])}{format_pos(sugerencia[1])}")

        try:
            entrada = input("Movimiento (ej. A5B4) o ENTER para usar sugerencia: ").strip()
            if entrada == "" and sugerencia:
                origen, destino = sugerencia
            else:
                origen, destino = parsear_movimiento(entrada)
            if mover_ficha(tablero, origen, destino, turno):
                turno = 'n' if turno == 'b' else 'b'
            else:
                print("Movimiento inválido. Intenta de nuevo.")
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(f"Error inesperado: {e}. Intenta de nuevo.")

if __name__ == "__main__":
    juego()