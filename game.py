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

def bfs(t, visit, i, j, largo):
    cola = [(i, j)]
    visit[i][j] = True
    toca_borde = False
    puede_virus = False
    while cola:
        cx, cy = cola.pop(0)
        if cx == 0 or cx == largo-1 or cy == 0 or cy == largo-1:
            toca_borde = True
        for dx, dy in DIRECCIONES:
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < largo and 0 <= ny < largo:
                if t[nx][ny] == VIRUS:
                    puede_virus = True
                if not visit[nx][ny] and t[nx][ny] == LIBRE:
                    visit[nx][ny] = True
                    cola.append((nx, ny))
    # Es isla si NO toca borde y NO puede ser alcanzada por el virus
    return not toca_borde and not puede_virus

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

    visitado = [[False]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if not visitado[i][j] and temp[i][j] == LIBRE:
                if bfs(temp, visitado, i, j, n):
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
