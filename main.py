from GUI import VtnMain, VtnSecond
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox
from game import virusSpread, putWall, inicialize, posVirus, canVirusSpread, savePartida, loadGame, checkEndGame
import sys
import os

MATRIZ = []

def handle_click(vtn, y_click, x_click, nivel):
    """Maneja lo que sucede cuando se da click en un boton de la matriz 

    Args:
        vtn (_type_): ventana principal
        y_click (_type_): coordenada y del boton
        x_click (_type_): coordenada x del boton
        nivel (_type_): nivel de la partida
    """
    global MATRIZ
    if not canVirusSpread(MATRIZ):
        reply = QMessageBox.question(
            vtn.vtnNewGame,
            "¡Ganaste!",
            "¡Felicidades, has ganado! ¿Quieres continuar al siguiente nivel?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            openNewGame(vtn, nivel+1)
        else:
            vtn.vtnNewGame.close()
        return
    
    if putWall(MATRIZ, y_click, x_click):
        vtn.vtnNewGame.matrizBotones[y_click][x_click].setText("🧱")
        result = virusSpread(MATRIZ)
        if result is not None and isinstance(result, tuple) and len(result) == 2:
            pX, pY = result
            if 0 <= pX < len(MATRIZ) and 0 <= pY < len(MATRIZ[0]):
                vtn.vtnNewGame.matrizBotones[pX][pY].setText("🦠")
            else:
                QMessageBox.warning(vtn.vtnNewGame, "Error", "El virus se propagó fuera de los límites de la matriz.")
            if not checkEndGame(MATRIZ):
                QMessageBox.information(vtn.vtnNewGame, "¡Perdiste!", "El virus ha infectado todas las celdas libres. ¡Has perdido!")
                reply = QMessageBox.question(
                    vtn.vtnNewGame,
                    "¡Perdiste!",
                    "¿Quieres reiniciar el juego?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.Yes:
                    openNewGame(vtn, nivel)
        else:
            reply = QMessageBox.question(
                vtn.vtnNewGame,
                "¡Ganaste!",
                "¡Felicidades, has ganado! ¿Quieres continuar al siguiente nivel?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                openNewGame(vtn, nivel+1)  # Llama a la función para iniciar un nuevo juego/nivel
            if reply == QMessageBox.StandardButton.No:
                print("Guardando partida...")
                reply_save = QMessageBox.question(
                    vtn.vtnNewGame,
                    "Guardar Partida",
                    "¿Quieres guardar tu partida antes de salir?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply_save == QMessageBox.StandardButton.Yes:
                    saveGame(vtn, nivel)
                vtn.vtnNewGame.close()
    else:
        QMessageBox.warning(vtn.vtnNewGame, "Movimiento incorrecto", "La celda ya está ocupada o no se puede colocar una barrera ahí.")

def setNumber(parent):
    """Solicita al usuario el tamaño de la matriz

    Args:
        parent (_type_): ventana principal 

    Returns:
        _type_: devuelve el numero ingresado por el usuario para crear la matriz
    """
    while True:
        num, ok = QInputDialog.getText(parent, "Matriz", "Escriba el número de filas y columnas (NxN):")
        if not ok:
            return None
        if num.strip().isdigit():
            return int(num.strip())
        else:
            QMessageBox.warning(parent, "Número inválido", "Solo se permiten números enteros.")

def saveGame(vtnM, level):
    """Guarda la partida que se esta jugando en un archivo .bin

    Args:
        vtnM (_type_): ventana principal 
        level (_type_): nivel de la partida
    """
    global MATRIZ
    if MATRIZ:
        file_name, ok = QInputDialog.getText(vtnM.vtnNewGame, "Guardar Partida", "Nombre del archivo:")
        if ok and file_name.strip():
            print(MATRIZ)
            savePartida(file_name.strip(), MATRIZ, level)
            QMessageBox.information(vtnM.vtnNewGame, "Partida guardada", f"Partida guardada como {file_name.strip()}")
        else:
            QMessageBox.warning(vtnM.vtnNewGame, "Error", "Nombre de archivo inválido.")
    else:
        QMessageBox.warning(vtnM.vtnNewGame, "Error", "No hay partida para guardar.")
    vtnM.vtnNewGame.close()

def openNewGame(vtnM, level):
    """Inicia una nueva partida 

    Args:
        vtnM (_type_): ventana principal
        level (_type_): nivel de la partida
    """
    global MATRIZ
    nume = setNumber(vtnM)
    if nume is None:
        return
    vtnM.vtnNewGame = VtnSecond("Nueva Partida", nume)
    MATRIZ = inicialize(nume, level)
    vtnM.vtnNewGame.setWindowTitle(f"Nivel {level}")
    vtnM.vtnNewGame.show()

    for i, j in posVirus(MATRIZ):
        vtnM.vtnNewGame.matrizBotones[i][j].setText("🦠")
        
    for i in range(nume):
        for j in range(nume):
            btn = vtnM.vtnNewGame.matrizBotones[i][j]
            btn.clicked.connect(lambda _, y=i, x=j: handle_click(vtnM, y, x, level))
    vtnM.vtnNewGame.btnSalir.clicked.connect(lambda : saveGame(vtnM, level))

def continueGame(vtnM):
    """Carga una partida guardada para continuar jugando 

    Args:
        vtnM (_type_): ventana principal 
    """
    global MATRIZ
    folder = "partidas"
    if not os.path.exists(folder):
        os.makedirs(folder)
    archivos = [f for f in os.listdir(folder) if f.endswith(".bin")]
    if not archivos:
        QMessageBox.warning(vtnM, "Sin partidas", "No hay archivos de partida guardados.")
        return
    archivos_str = "\n".join(archivos)
    QMessageBox.information(vtnM, "Partidas guardadas", f"Archivos disponibles:\n{archivos_str}")
    file_name, ok = QInputDialog.getText(vtnM, "Cargar Partida", "Nombre del archivo:")
    if ok and file_name.strip():
        try:
            MATRIZ, level = loadGame(file_name.strip())
            vtnM.vtnNewGame = VtnSecond("Continuar Partida", len(MATRIZ))
            vtnM.vtnNewGame.setWindowTitle(f"Nivel {level}")
            vtnM.vtnNewGame.show()
            # Mostrar virus y barreras según la matriz cargada
            for i in range(len(MATRIZ)):
                for j in range(len(MATRIZ)):
                    btn = vtnM.vtnNewGame.matrizBotones[i][j]
                    if MATRIZ[i][j] == 1:  # Suponiendo 1 es virus
                        btn.setText("🦠")
                    elif MATRIZ[i][j] == 2:  # Suponiendo 2 es barrera
                        btn.setText("🧱")
                    elif MATRIZ[i][j] == 0:  # Suponiendo 0 es libre
                        btn.setText("🟩")
                    else:
                        btn.setText("")
                    btn.clicked.connect(lambda _, y=i, x=j: handle_click(vtnM, y, x, level))
            vtnM.vtnNewGame.btnSalir.clicked.connect(lambda : saveGame(vtnM, level))
        except Exception as e:
            QMessageBox.warning(vtnM, "Error", f"No se pudo cargar la partida: {e}")
    else:
        QMessageBox.warning(vtnM, "Error", "Nombre de archivo inválido.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VtnMain()
    window.show()
    window.btnNewGame.clicked.connect(lambda: openNewGame(window, 1))
    window.btnContinueGame.clicked.connect(lambda: continueGame(window))
    sys.exit(app.exec())
