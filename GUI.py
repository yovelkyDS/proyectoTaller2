from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
import sys

app = QApplication(sys.argv)
vtnMain = QWidget()
vtnMain.setWindowTitle("Virus Game")
vtnMain.setGeometry(40, 50, 800, 600)

# Crear botones
btnNewGame = QPushButton("Nueva partida")
btnContinueGame = QPushButton("Opciones")

button_style = """
    QPushButton {
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 24px;
        padding: 15px;
    }
    QPushButton:hover {
        background-color: #218838;
    }
    QPushButton:pressed {
        background-color: #1e7e34;
    }
"""

for btn in (btnNewGame, btnContinueGame):
    btn.setFixedSize(250, 70)
    btn.setStyleSheet(button_style)

# Crear layout y agregar botones
layout = QVBoxLayout()
layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
layout.setSpacing(20)

layout.addWidget(btnNewGame)
layout.addWidget(btnContinueGame)

# Aplicar layout a la ventana
vtnMain.setLayout(layout)

vtnMain.show()
sys.exit(app.exec())
