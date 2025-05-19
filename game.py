import random
import struct, os
# Constantes
LIBRE = 0
VIRUS = 1
BARRERA = 2

DIRECCIONES = [(-1,0), (1,0), (0,-1), (0,1)]

def inicialize(n, nivel):
    """inicializa la matriz del juego 

    Args:
        n (_type_): tamaño de la matriz
        nivel (_type_): nivel de dificultad de la partida

    Returns:
        _type_: matriz inicializada
    """
    matriz = [[LIBRE for _ in range(n)] for _ in range(n)]
    puntos = min(nivel, n*n)
    posiciones = random.sample([(i, j) for i in range(n) for j in range(n)], puntos)
    for x, y in posiciones:
        matriz[x][y] = VIRUS
    return matriz

def checkEndGame(matriz):
    """
    Verifica si el juego terminó porque el virus ya no puede propagarse.
    Retorna False si el usuario perdió (el virus no puede expandirse y no quedan casillas libres).
    Retorna True si el juego puede continuar.

    Args:
        matriz (_type_): matriz del juego

    Returns:
        bool: False si el usuario perdió, True si el juego sigue
    """
    # Si no hay casillas libres y el virus no puede expandirse, el usuario perdió
    libres = any(LIBRE in fila for fila in matriz)
    if not libres and not canVirusSpread(matriz):
        return False
    return True
    

def es_isla(matriz, x, y):
    """Verifica si poner una barrera en cierta posicion crearia una isla 

    Args:
        matriz (_type_): matriz del juego 
        x (_type_): coordenada x del click del usuario
        y (_type_): coordenada y del click del usuario

    Returns:
        _type_: Devuelve True si se crea una isla, False si no
    """
    n = len(matriz)
    temp = [fila[:] for fila in matriz]
    temp[x][y] = BARRERA

    # Buscar todas las posiciones LIBRE
    libres = set((i, j) for i in range(n) for j in range(n) if temp[i][j] == LIBRE)
    if not libres:
        return False

    # Buscar todas las posiciones VIRUS
    virus = set((i, j) for i in range(n) for j in range(n) if temp[i][j] == VIRUS)
    if not virus:
        return False  # No hay virus, no puede haber isla

    # BFS desde todas las posiciones de virus para marcar las LIBRE alcanzables
    visitado = [[False]*n for _ in range(n)]
    from collections import deque
    cola = deque()
    for vx, vy in virus:
        cola.append((vx, vy))
        visitado[vx][vy] = True

    while cola:
        cx, cy = cola.popleft()
        for dx, dy in DIRECCIONES:
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < n and 0 <= ny < n and not visitado[nx][ny]:
                if temp[nx][ny] == LIBRE:
                    visitado[nx][ny] = True
                    cola.append((nx, ny))
                elif temp[nx][ny] == VIRUS:
                    visitado[nx][ny] = True  # Marcar virus también

    # Si existe alguna celda LIBRE no visitada, es una isla
    for i, j in libres:
        if not visitado[i][j]:
            return True
    return False

def canVirusSpread(matriz):
    """Verifica si el virus puede propagarse 

    Args:
        matriz (_type_): matriz del juego

    Returns:
        _type_: Devuelve True si el virus puede propagarse, False si no
    """
    n = len(matriz)
    for x, y in posVirus(matriz):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and matriz[nx][ny] == 0:
                return True
    return False

def putWall(matriz, x, y):
    """Coloca una barrera si la celda esta libre y no crea una isla 

    Args:
        matriz (_type_): matriz del juego
        x (_type_): coordenada x del click del usuario
        y (_type_): coordenada y del click del usuario

    Returns:
        _type_: Devuelve True si se coloca la barrera, False si no se pudo colocar 
    """
    if matriz[x][y] != LIBRE:
        return False
    matriz[x][y] = BARRERA
    # Validar islas
    if es_isla(matriz, x, y):
        matriz[x][y] = LIBRE
        return False
    return True

def posVirus(matriz):
    """Devuelve las posiciones de los virus dentro de la matriz

    Args:
        matriz (_type_): matriz del juego

    Returns:
        _type_: lista de posiciones del virus
    """
    return [(i, j) for i, fila in enumerate(matriz) for j, v in enumerate(fila) if v == VIRUS]

def virusSpread(matriz):
    """Propaga el virus a una celda libre adyacente
    Elige aleatoriamente una dirección y propaga el virus a una celda libre adyacente.

    Args:
        matriz (_type_): matriz del juego

    Returns:
        _type_: coordenadas de la celda infectada o None si no hay celdas libres
    """
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
    """Convierte una matriz a una lista de bytes hexadecimales
    Cada fila de la matriz se convierte a un número entero en base 3, y luego se convierte a bytes.

    Args:
        matriz (_type_): matriz que se va a convertir 

    Returns:
        _type_: lista de bytes hexadecimales
    """
    hex_filas = []
    for fila in matriz:
        num = 0
        for v in fila:
            num = num*3 + v
        # Guardar cada fila como bytes binarios, no como string hexadecimal
        hex_filas.append(num.to_bytes((len(fila)*2+7)//8, 'big'))
    return hex_filas

def savePartida(nombre, matriz, nivel):
    """Guarda la partida en un archivo binario
    El archivo se guarda en la carpeta "partidas" y se le asigna el nombre proporcionado.

    Args:
        nombre (_type_): nombre del archivo
        matriz (_type_): mariz de la partida
        nivel (_type_): nivel de la partida
    """
    n = len(matriz)
    hex_filas = matriz_a_hex(matriz)
    carpeta = "partidas"
    os.makedirs(carpeta, exist_ok=True)
    if not nombre.endswith('.bin'):
        nombre += '.bin'
    ruta = os.path.join(carpeta, nombre)
    with open(ruta, 'wb') as f:
        f.write(struct.pack('>H', n))
        f.write(struct.pack('B', nivel))
        for h in hex_filas:
            f.write(h)

def hex_a_matriz(hex_filas, n):
    """Convierte una lista de bytes hexadecimales a una matriz

    Args:
        hex_filas (_type_): lista de bytes hexadecimales
        n (_type_): tamaño de la matriz

    Returns:
        _type_: matriz convertida
    """
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
    """Carga una partida desde un archivo binario

    Args:
        nombre (_type_): nombre del archivo de la partida a cargar

    Raises:
        FileNotFoundError: si el archivo no existe

    Returns:
        _type_: matriz de la partida y nivel de la partida
    """
    if not nombre.endswith('.bin'):
        nombre += '.bin'
    carpeta = "partidas"
    ruta = os.path.join(carpeta, nombre)
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo {ruta} no existe.")
    with open(ruta, 'rb') as f:
        n = struct.unpack('>H', f.read(2))[0]
        nivel = struct.unpack('B', f.read(1))[0]
        fila_bytes = (n*2+7)//8
        hex_filas = []
        for _ in range(n):
            datos = f.read(fila_bytes)
            hex_filas.append(datos)
        matriz = hex_a_matriz(hex_filas, n)
    return matriz, nivel
