import random
import struct
# Constantes
LIBRE = 0
VIRUS = 1
BARRERA = 2

DIRECCIONES = [(-1,0), (1,0), (0,-1), (0,1)]

def inicialize(n, nivel):
    matriz = [[LIBRE for _ in range(n)] for _ in range(n)]
    puntos = min(nivel, n*n)
    posiciones = random.sample([(i, j) for i in range(n) for j in range(n)], puntos)
    for x, y in posiciones:
        matriz[x][y] = VIRUS
    return matriz

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

def canVirusSpread(matriz):
    n = len(matriz)
    for x, y in posVirus(matriz):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and matriz[nx][ny] == 0:
                return True
    return False

def putWall(matriz, x, y):
    if matriz[x][y] != LIBRE:
        return False
    matriz[x][y] = BARRERA
    # Validar islas
    if es_isla(matriz, x, y):
        matriz[x][y] = LIBRE
        return False
    return True

def posVirus(matriz):
    return [(i, j) for i, fila in enumerate(matriz) for j, v in enumerate(fila) if v == VIRUS]

def virusSpread(matriz):
    n = len(matriz)
    infectados = []
    for x, y in posVirus(matriz):
        random.shuffle(DIRECCIONES)
        for dx, dy in DIRECCIONES:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and matriz[nx][ny] == LIBRE:
                infectados.append((nx, ny))
    if infectados:
        x, y = random.choice(infectados)
        matriz[x][y] = VIRUS
        return x, y
    return None

def matriz_a_hex(matriz):
    hex_filas = []
    for fila in matriz:
        num = 0
        for v in fila:
            num = num*3 + v
        # Guardar cada fila como bytes binarios, no como string hexadecimal
        hex_filas.append(num.to_bytes((len(fila)*2+7)//8, 'big'))
    return hex_filas

def savePartida(nombre, matriz, nivel):
    n = len(matriz)
    hex_filas = matriz_a_hex(matriz)
    with open(nombre, 'wb') as f:
        f.write(struct.pack('>H', n))
        f.write(struct.pack('B', nivel))
        for h in hex_filas:
            f.write(h)

def hex_a_matriz(hex_filas, n):
    matriz = []
    for h in hex_filas:
        num = int.from_bytes(h, 'big')
        fila = []
        for _ in range(n):
            fila.append(num % 3)
            num //= 3
        matriz.append(list(reversed(fila)))
    return matriz

def loadGame(nombre):
    with open(nombre, 'rb') as f:
        n = struct.unpack('>H', f.read(2))[0]
        nivel = struct.unpack('B', f.read(1))[0]
        fila_bytes = (n*2+7)//8
        hex_filas = []
        for _ in range(n):
            datos = f.read(fila_bytes)
            hex_filas.append(datos)
        matriz = hex_a_matriz(hex_filas, n)
    return matriz, nivel
