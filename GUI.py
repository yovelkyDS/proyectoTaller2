from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMainWindow
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

class VtnSecond(QWidget):
    def __init__(self, title, n: int = 5):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 300)

        # Crear matriz de botones
        self.matrizBotones = []
        grid_layout = QGridLayout()
        for y in range(n):
            filaBtn = []
            for x in range(n):
                boton = QPushButton("🟩") 
                boton.setFixedSize(50, 50) 
                boton.setStyleSheet("font-size: 40px; border: none; background: transparent;")  
                grid_layout.addWidget(boton, y, x) 
                filaBtn.append(boton)
            self.matrizBotones.append(filaBtn)

        # Crear botón de salir
        btnSalir = QPushButton("Salir")
        btnSalir.setFixedSize(80, 30)
        btnSalir.clicked.connect(self.close)

        # Layout horizontal para alinear el botón a la derecha
        h_layout = QHBoxLayout()
        h_layout.addStretch()  # Empuja el botón hacia la derecha
        h_layout.addWidget(btnSalir)

        # Layout principal vertical
        v_layout = QVBoxLayout()
        v_layout.addLayout(grid_layout)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
    

class VtnMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Virus Game")
        self.setGeometry(40, 50, 800, 600)

        # Crear botones
        self.btnNewGame = QPushButton("Nueva partida")
        self.btnContinueGame = QPushButton("Continuar partida")

        self.button_style = """
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
            btn.setStyleSheet(self.button_style)

        # Crear layout y agregar botones
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.addWidget(self.btnNewGame)
        layout.addWidget(self.btnContinueGame)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


