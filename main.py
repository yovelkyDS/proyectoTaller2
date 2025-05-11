from GUI import VtnMain, VtnSecond
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox
import re
import sys, random

def setName(parent):
    while True:
        texto, ok = QInputDialog.getText(parent, "Nombre del jugador", "Escribe tu nombre:")
        if not ok:
            return None
        if re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]{1,20}", texto.strip()):
            return texto.strip()
        else:
            QMessageBox.warning(parent, "Nombre inválido", "Solo letras y espacios. Inténtalo de nuevo.")

def setNumber(parent):
    while True:
        num, ok = QInputDialog.getText(parent, "Matriz", "Escriba el numero de filas y columnas de la matriz del juego (formato NxN):")
        if not ok:
            return None
        if num.strip().isdigit():
            return int(num.strip())
        else:
            QMessageBox.warning(parent, "Número inválido", "Solo se permiten números enteros. Inténtalo de nuevo.")

def openNewGame(vtnM):
    nume = setNumber(vtnM)
    if nume is None:
        return
    vtnM.vtnNewGame = VtnSecond("Nueva Partida", nume)
    vtnM.vtnNewGame.show()
    QApplication.processEvents()

    pX, pY = vtnM.vtnNewGame.ultimo_click
    if pX is None or pY is None:
        x = random.randint(0, nume-1)
        y = random.randint(0, nume-1)
        vtnM.vtnNewGame.matrizBotones[x][y].setText("🦠")
        vtnM.vtnNewGame.ultimo_click = (x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VtnMain()
    window.show()
    name = setName(window)
    if name == None:
        window.destroy()
    window.btnNewGame.clicked.connect(lambda: openNewGame(window))
    sys.exit(app.exec())