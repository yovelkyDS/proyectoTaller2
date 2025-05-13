from GUI import VtnMain, VtnSecond
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox
from game import virusSpread, putWall, createIsland, infecciones
import sys, random

matrizPosiciones = []

def handle_click(vtn, num, y_click, x_click):
    global matrizPosiciones

    if putWall(matrizPosiciones, y_click, x_click, num):
        vtn.vtnNewGame.matrizBotones[y_click][x_click].setText("🧱")
        nuevas = virusSpread(matrizPosiciones, num)
        for yv, xv in nuevas:
            vtn.vtnNewGame.matrizBotones[yv][xv].setText("🦠")
            QApplication.processEvents()
    else:
        QMessageBox.warning(vtn.vtnNewGame, "Movimiento inválido", "No puedes crear islas inaccesibles o colocar una barrera ahí.")

def setNumber(parent):
    while True:
        num, ok = QInputDialog.getText(parent, "Matriz", "Escriba el número de filas y columnas (NxN):")
        if not ok:
            return None
        if num.strip().isdigit():
            return int(num.strip())
        else:
            QMessageBox.warning(parent, "Número inválido", "Solo se permiten números enteros.")

def openNewGame(vtnM):
    global matrizPosiciones
    nume = setNumber(vtnM)
    if nume is None:
        return

    vtnM.vtnNewGame = VtnSecond("Nueva Partida", nume)
    vtnM.vtnNewGame.show()

    matrizPosiciones.clear()
    infecciones.clear()
    for _ in range(nume):
        matrizPosiciones.append([0] * nume)

    x = random.randint(0, nume - 1)
    y = random.randint(0, nume - 1)
    vtnM.vtnNewGame.matrizBotones[y][x].setText("🦠")
    vtnM.vtnNewGame.ultimo_click = (x, y)
    matrizPosiciones[y][x] = 1
    infecciones.append((y, x))

    for i in range(nume):
        for j in range(nume):
            btn = vtnM.vtnNewGame.matrizBotones[i][j]
            btn.clicked.connect(lambda _, y=i, x=j: handle_click(vtnM, nume, y, x))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VtnMain()
    window.show()
    window.btnNewGame.clicked.connect(lambda: openNewGame(window))
    sys.exit(app.exec())
