import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox,
    QButtonGroup,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard
from analizador import SERVICIOS 


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador de URL")
        self.setFixedSize(680, 230)  # Tamaño fijo y no redimensionable
        self.center()  # Centrar la ventana

        # Establecer colores para el tema oscuro moderno
        self.setStyleSheet(
            """
            /* Fondo y texto general */
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: "Segoe UI", sans-serif;
                font-size: 14px;
            }

            /* Botones */
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px 16px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #666666;
            }
            QPushButton:pressed {
                background-color: #222222;
            }

            /* Caja de texto */
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #555555;
                selection-color: #ffffff;
            }

            /* Radio buttons */
            QRadioButton {
                color: #ffffff;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #555555;
                border-radius: 8px;
                background-color: #333333;
            }
            QRadioButton::indicator:checked {
                background-color: #0078d7;
                border: 2px solid #0078d7;
            }

            /* Mensajes de error */
            QMessageBox {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QMessageBox QLabel {
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QMessageBox QPushButton:hover {
                background-color: #444444;
                border: 1px solid #666666;
            }
        """
        )

        # Layout principal
        layout = QVBoxLayout()

        # Cuadro de texto donde se pegará el contenido del portapapeles
        self.texto = QTextEdit()
        self.texto.setPlaceholderText("Pega la URL aquí...")
        self.texto.setMaximumHeight(50)  
        layout.addWidget(self.texto)

        # Frame para los botones de pegar y limpiar
        frame_pegar_limpiar = QHBoxLayout()

        # Botón para pegar el contenido del portapapeles
        boton_pegar = QPushButton("Pegar")
        boton_pegar.clicked.connect(self.pegar_texto)
        boton_pegar.setFixedWidth(100) 
        frame_pegar_limpiar.addWidget(boton_pegar)

        # Botón para limpiar el cuadro de texto
        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.clicked.connect(self.limpiar_texto)
        boton_limpiar.setFixedWidth(100) 
        frame_pegar_limpiar.addWidget(boton_limpiar)

        layout.addLayout(frame_pegar_limpiar)

        # Frame para los radio buttons
        frame_radio_buttons = QHBoxLayout()

        # Grupo de botones de radio
        self.button_group = QButtonGroup()

        for i, (nombre, _) in enumerate(SERVICIOS):
            radio_button = QRadioButton(nombre)
            self.button_group.addButton(radio_button, i)
            frame_radio_buttons.addWidget(radio_button)

        # Establecer un valor predeterminado
        self.button_group.button(0).setChecked(True)

        layout.addLayout(frame_radio_buttons)

        # Contenedor horizontal para centrar el botón "Analizar"
        frame_boton_analizar = QHBoxLayout()
        frame_boton_analizar.addStretch() 
        boton_buscar = QPushButton("Analizar")
        boton_buscar.clicked.connect(self.buscar_en_servicio)
        boton_buscar.setFixedWidth(100)  
        frame_boton_analizar.addWidget(boton_buscar)
        frame_boton_analizar.addStretch() 
        layout.addLayout(frame_boton_analizar)

        # Widget central
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Función para centrar la ventana
    def center(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    # Función para pegar el contenido del portapapeles en el cuadro de texto
    def pegar_texto(self):
        clipboard = QApplication.clipboard()
        self.texto.setPlainText(clipboard.text())

    # Función para limpiar el cuadro de texto
    def limpiar_texto(self):
        self.texto.clear()

    # Función principal para buscar en el servicio seleccionado
    def buscar_en_servicio(self):
        url_a_buscar = self.texto.toPlainText().strip()
        if not url_a_buscar:
            QMessageBox.critical(self, "Error", "No hay URL en el cuadro de texto para analizar.")
            return

        # Obtener el servicio seleccionado
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún servicio.")
            return

        nombre_servicio, funcion_busqueda = SERVICIOS[selected_id]
        funcion_busqueda(url_a_buscar)


# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())