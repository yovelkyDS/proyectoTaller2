from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMainWindow
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt

class VtnSecond(QWidget):
    def __init__(self, title, n: int = 5):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 300)
        self.ultimo_click = (None, None)

        self.matrizBotones = []
        grid_layout = QGridLayout()
        for y in range(n):
            filaBtn = []
            for x in range(n):
                boton = QPushButton("🟩")
                boton.setFixedSize(50, 50)
                boton.setStyleSheet("""
                    QPushButton {
                        font-size: 30px;
                        background-color: black;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                """)
                grid_layout.addWidget(boton, y, x)
                filaBtn.append(boton)
            self.matrizBotones.append(filaBtn)

        btnSalir = QPushButton("Salir")
        btnSalir.setFixedSize(80, 30)
        btnSalir.clicked.connect(self.close)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(btnSalir)

        v_layout = QVBoxLayout()
        v_layout.addLayout(grid_layout)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

class VtnMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virus Game")
        self.setGeometry(40, 50, 800, 600)

        self.btnNewGame = QPushButton("Nueva partida")
        self.btnContinueGame = QPushButton("Continuar partida")

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

        for btn in (self.btnNewGame, self.btnContinueGame):
            btn.setFixedSize(250, 70)
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.addWidget(self.btnNewGame)
        layout.addWidget(self.btnContinueGame)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
