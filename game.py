import random

# Estados posibles en la matriz
LIBRE = 0
VIRUS = 1
BARRERA = 2

# Variables compartidas (deben inicializarse desde el archivo principal)
infecciones = []
turno_barrera = True

def virusSpread(matriz, num):
    global turno_barrera, infecciones

    posibles_infecciones = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for y in range(num):
        for x in range(num):
            if matriz[y][x] == VIRUS:
                random.shuffle(directions)  # opcional
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < num and 0 <= nx < num:
                        if matriz[ny][nx] == LIBRE:
                            posibles_infecciones.append((ny, nx))
                            break  # solo una opción por virus

    if posibles_infecciones:
        nueva = random.choice(posibles_infecciones)
        y, x = nueva
        matriz[y][x] = VIRUS
        infecciones.append(nueva)
        turno_barrera = True
        return [nueva]  # solo una infección por turno

    turno_barrera = True
    return []  # nada que infectar

def putWall(matriz, y, x, num):
    global turno_barrera
    if turno_barrera and matriz[y][x] == LIBRE:
        matriz[y][x] = BARRERA
        if createIsland(matriz, num):
            matriz[y][x] = LIBRE
            return False
        turno_barrera = False
        return True
    return False

def createIsland(matriz, num):
    global infecciones
    visitado = [[False for _ in range(num)] for _ in range(num)]

    def dfs(y, x):
        if not (0 <= y < num and 0 <= x < num): return
        if visitado[y][x] or matriz[y][x] != LIBRE: return
        visitado[y][x] = True
        for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
            dfs(y+dy, x+dx)

    for y, x in infecciones:
        for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < num and 0 <= nx < num and matriz[ny][nx] == LIBRE:
                dfs(ny, nx)

    for y in range(num):
        for x in range(num):
            if matriz[y][x] == LIBRE and not visitado[y][x]:
                return True
    return False
