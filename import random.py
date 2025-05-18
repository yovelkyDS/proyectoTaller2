import random
import struct
import os

# Constantes
LIBRE = 0
VIRUS = 1
BARRERA = 2

DIRECCIONES = [(-1,0), (1,0), (0,-1), (0,1)]  # Arriba, Abajo, Izquierda, Derecha

def crear_matriz(n, nivel):
    matriz = [[LIBRE for _ in range(n)] for _ in range(n)]
    puntos = min(nivel, n*n)
    posiciones = random.sample([(i, j) for i in range(n) for j in range(n)], puntos)
    for x, y in posiciones:
        matriz[x][y] = VIRUS
    return matriz

def mostrar_matriz(matriz):
    simbolos = {LIBRE: '.', VIRUS: 'V', BARRERA: '#'}
    for fila in matriz:
        print(' '.join(simbolos[c] for c in fila))
    print()

def posiciones_virus(matriz):
    return [(i, j) for i, fila in enumerate(matriz) for j, v in enumerate(fila) if v == VIRUS]

def celdas_libres(matriz):
    print("Celdas libres:")
    return [(i, j) for i, fila in enumerate(matriz) for j, v in enumerate(fila) if v == LIBRE]

def puede_propagarse(matriz):
    n = len(matriz)
    for x, y in posiciones_virus(matriz):
        for dx, dy in DIRECCIONES:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and matriz[nx][ny] == LIBRE:
                return True
    return False

def propagar_virus(matriz):
    n = len(matriz)
    infectados = []
    for x, y in posiciones_virus(matriz):
        random.shuffle(DIRECCIONES)
        for dx, dy in DIRECCIONES:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and matriz[nx][ny] == LIBRE:
                infectados.append((nx, ny))
    if infectados:
        x, y = random.choice(infectados)
        matriz[x][y] = VIRUS

def es_isla(matriz, x, y):
    # BFS desde (x, y) para ver si puede llegar a un virus
    n = len(matriz)
    visitado = [[False]*n for _ in range(n)]
    cola = [(x, y)]
    visitado[x][y] = True
    while cola:
        cx, cy = cola.pop(0)
        if matriz[cx][cy] == VIRUS:
            return False
        for dx, dy in DIRECCIONES:
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < n and 0 <= ny < n and not visitado[nx][ny]:
                if matriz[nx][ny] != BARRERA:
                    visitado[nx][ny] = True
                    cola.append((nx, ny))
    return True

def colocar_barrera(matriz, x, y):
    if matriz[x][y] != LIBRE:
        return False
    matriz[x][y] = BARRERA
    # Validar islas
    if es_isla(matriz, x, y):
        print(f"Colocando barrera en ({i}, {j})")
        matriz[x][y] = LIBRE
        return False
    return True

def matriz_a_hex(matriz):
    hex_filas = []
    for fila in matriz:
        num = 0
        for v in fila:
            num = num*3 + v
        hex_filas.append(num.to_bytes((len(fila)*2+7)//8, 'big').hex())
    return hex_filas

def hex_a_matriz(hex_filas, n):
    matriz = []
    for h in hex_filas:
        num = int(h, 16)
        fila = []
        for _ in range(n):
            fila.append(num % 3)
            num //= 3
        matriz.append(list(reversed(fila)))
    return matriz

def guardar_partida(nombre, matriz, nivel):
    n = len(matriz)
    hex_filas = matriz_a_hex(matriz)
    with open(nombre, 'wb') as f:
        f.write(struct.pack('>H', n))
        f.write(struct.pack('B', nivel))
        for h in hex_filas:
            f.write(bytes.fromhex(h))

def cargar_partida(nombre):
    with open(nombre, 'rb') as f:
        n = struct.unpack('>H', f.read(2))[0]
        nivel = struct.unpack('B', f.read(1))[0]
        fila_bytes = (n*2+7)//8
        hex_filas = []
        for _ in range(n):
            datos = f.read(fila_bytes)
            hex_filas.append(datos.hex())
        matriz = hex_a_matriz(hex_filas, n)
    return matriz, nivel

def juego():
    print("Bienvenido a Virus Spread Challenge")
    while True:
        op = input("1. Nueva partida\n2. Cargar partida\n3. Salir\n> ")
        if op == '1':
            n = int(input("Tamaño de la matriz (N): "))
            nivel = int(input("Nivel de dificultad: "))
            matriz = crear_matriz(n, nivel)
            break
        elif op == '2':
            nombre = input("Nombre del archivo a cargar: ")
            if not os.path.exists(nombre):
                print("Archivo no encontrado.")
                continue
            matriz, nivel = cargar_partida(nombre)
            n = len(matriz)
            break
        elif op == '3':
            return
        else:
            print("Opción inválida.")
    turno = 1
    while True:
        print(f"\nTurno {turno} - Nivel {nivel}")
        mostrar_matriz(matriz)
        if not puede_propagarse(matriz):
            print("¡Ganaste! El virus no puede expandirse más.")
            break
        if not celdas_libres(matriz):
            print("¡Perdiste! El virus ocupó todas las celdas libres.")
            break
        # Colocar barrera
        while True:
            s = input("Coloca barrera (formato: x y) o 'guardar nombre': ")
            if s.startswith('guardar'):
                _, nombre = s.split()
                guardar_partida(nombre, matriz, nivel)
                print("Partida guardada.")
                continue
            try:
                x, y = map(int, s.strip().split())
                if 0 <= x < n and 0 <= y < n:
                    if colocar_barrera(matriz, x, y):
                        break
                    else:
                        print("Movimiento inválido (celda ocupada o crearía isla).")
                else:
                    print("Coordenadas fuera de rango.")
            except:
                print("Entrada inválida.")
        propagar_virus(matriz)
        turno += 1

if __name__ == "__main__":
    juego()