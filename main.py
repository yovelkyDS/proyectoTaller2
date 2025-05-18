from GUI import VtnMain, VtnSecond
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox
from game import virusSpread, putWall, inicialize, posVirus, canVirusSpread
import sys
TURNO = 0
MATRIZ = []

def handle_click(vtn, num, y_click, x_click, nivel):
    global MATRIZ
    if not canVirusSpread(MATRIZ):
        reply = QMessageBox.question(
            vtn.vtnNewGame,
            "¡Ganaste!",
            "¡Felicidades, has ganado! ¿Quieres continuar al siguiente nivel?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            openNewGame(vtn, nivel+1, num)
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
        else:
            reply = QMessageBox.question(
                vtn.vtnNewGame,
                "¡Ganaste!",
                "¡Felicidades, has ganado! ¿Quieres continuar al siguiente nivel?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                openNewGame(vtn, nivel+1, num)  # Llama a la función para iniciar un nuevo juego/nivel
            else:
                vtn.vtnNewGame.close()
    else:
        QMessageBox.warning(vtn.vtnNewGame, "Movimiento incorrecto", "La celda ya está ocupada o no se puede colocar una barrera ahí.")

def setNumber(parent):
    while True:
        num, ok = QInputDialog.getText(parent, "Matriz", "Escriba el número de filas y columnas (NxN):")
        if not ok:
            return None
        if num.strip().isdigit():
            return int(num.strip())
        else:
            QMessageBox.warning(parent, "Número inválido", "Solo se permiten números enteros.")

def openNewGame(vtnM, level, nume=6):
    global MATRIZ, TURNO
    if level == 1:
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
            btn.clicked.connect(lambda _, y=i, x=j: handle_click(vtnM, nume, y, x, level))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VtnMain()
    window.show()
    window.btnNewGame.clicked.connect(lambda: openNewGame(window, 1))
    sys.exit(app.exec())
