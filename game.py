import random
import struct
import os

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