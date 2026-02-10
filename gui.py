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
    QLabel,
    QMessageBox,
    QButtonGroup,
    QComboBox,
    QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from analizador import SERVICIOS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador de URL")
        self.setWindowIcon(QIcon("favicon.ico"))
        self.setFixedSize(800, 780)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        self.center()
        try:
            with open("style.qss", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"No se pudo cargar el archivo de estilos: {e}")

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(15)

        self.idiomas = {"Español": "es", "English": "en"}
        self.idioma_actual = "es"

        # Section 1: URL Input
        self.label_url = QLabel("URL para analizar")
        self.label_url.setObjectName("titulo")
        layout.addWidget(self.label_url)
        
        self.texto = QTextEdit()
        self.texto.setMaximumHeight(80)
        self.texto.setAcceptDrops(True)
        layout.addWidget(self.texto)

        # Section 2: Action Buttons
        fila_botones = QHBoxLayout()
        
        boton_pegar = QPushButton("Pegar")
        boton_pegar.clicked.connect(self.pegar_texto)
        boton_pegar.setFixedSize(130, 42)
        boton_pegar.setCursor(Qt.CursorShape.PointingHandCursor)
        
        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.clicked.connect(self.limpiar_texto)
        boton_limpiar.setFixedSize(130, 42)
        boton_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        
        boton_analizar = QPushButton("Analizar")
        boton_analizar.clicked.connect(self.buscar_en_servicio)
        boton_analizar.setFixedSize(130, 42)
        boton_analizar.setCursor(Qt.CursorShape.PointingHandCursor)
        
        boton_exportar = QPushButton("Exportar historial")
        boton_exportar.clicked.connect(self.exportar_historial)
        boton_exportar.setFixedSize(160, 42)
        boton_exportar.setCursor(Qt.CursorShape.PointingHandCursor)

        fila_botones.addWidget(boton_pegar)
        fila_botones.addWidget(boton_limpiar)
        fila_botones.addWidget(boton_analizar)
        fila_botones.addWidget(boton_exportar)
        fila_botones.setSpacing(15)
        fila_botones.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(fila_botones)
        layout.addSpacing(10)

        # Section 3: Service Selection
        from PyQt6.QtWidgets import QGridLayout
        self.label_servicios = QLabel("Seleccione un servicio de análisis:")
        layout.addWidget(self.label_servicios)
        
        grid_servicios = QGridLayout()
        grid_servicios.setSpacing(10)
        self.button_group = QButtonGroup()
        
        cols = 3
        for i, (nombre, _) in enumerate(SERVICIOS):
            radio_button = QRadioButton(nombre)
            radio_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.button_group.addButton(radio_button, i)
            row = i // cols
            col = i % cols
            grid_servicios.addWidget(radio_button, row, col)
        
        if self.button_group.buttons():
            self.button_group.button(0).setChecked(True)
        layout.addLayout(grid_servicios)
        layout.addSpacing(10)

        # Section 4: Reputation Result (Box style)
        self.label_reputacion = QLabel("Reputación: Desconocida")
        self.label_reputacion.setMinimumHeight(90) 
        self.label_reputacion.setWordWrap(True)
        self.label_reputacion.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.label_reputacion.setObjectName("reputacion")
        layout.addWidget(self.label_reputacion)
        layout.addSpacing(10)

        # Section 5: History
        self.label_historial = QLabel("Historial de URLs")
        layout.addWidget(self.label_historial)
        
        self.historial_text = QTextEdit()
        self.historial_text.setReadOnly(True)
        self.historial_text.setMinimumHeight(120)
        self.historial_text.setMaximumHeight(180) # Prevent it from eating all space
        self.historial_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        layout.addWidget(self.historial_text)

        # FORCE EVERYTHING UP AND SETTINGS DOWN
        layout.addStretch(1)
        layout.addSpacing(20)

        # Section 6: Settings (Now guaranteed to be below everything)
        fila_ajustes = QHBoxLayout()
        
        self.combo_idioma = QComboBox()
        self.combo_idioma.addItems(list(self.idiomas.keys()))
        self.combo_idioma.currentTextChanged.connect(self.cambiar_idioma)
        self.combo_idioma.setFixedWidth(160)
        self.combo_idioma.setFixedHeight(36)
        
        self.combo_tema = QComboBox()
        self.combo_tema.addItems(["Oscuro", "Claro"])
        self.combo_tema.currentTextChanged.connect(self.cambiar_tema)
        self.combo_tema.setFixedWidth(160)
        self.combo_tema.setFixedHeight(36)
        
        fila_ajustes.addWidget(self.combo_idioma)
        fila_ajustes.addSpacing(20)
        fila_ajustes.addWidget(self.combo_tema)
        fila_ajustes.addStretch()
        
        layout.addLayout(fila_ajustes)

        self.historial = []
        self.setCentralWidget(main_widget)

    def center(self):
        # Get the geometry of the main window
        qr = self.frameGeometry()
        # Get the center point of the available screen space (handles taskbars)
        cp = self.screen().availableGeometry().center()
        # Move the rectangle's center to the screen's center
        qr.moveCenter(cp)
        # Move the top-left point of the window to the top-left of the rectangle
        self.move(qr.topLeft())

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.texto.setPlainText(event.mimeData().text())

    def pegar_texto(self):
        clipboard = QApplication.clipboard()
        self.texto.setPlainText(clipboard.text())

    def limpiar_texto(self):
        self.texto.clear()

    def buscar_en_servicio(self):
        url_a_buscar = self.texto.toPlainText().strip()
        if not url_a_buscar:
            QMessageBox.critical(self, "Error", "No hay URL en el cuadro de texto para analizar.")
            return
        import re
        patron_url = re.compile(r"^(https?://)?([\w.-]+)\.([a-z]{2,})(/.*)?$", re.IGNORECASE)
        if not patron_url.match(url_a_buscar):
            QMessageBox.critical(self, "Error", "La URL ingresada no tiene un formato válido.")
            return
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún servicio.")
            return
        nombre_servicio, funcion_busqueda = SERVICIOS[selected_id]
        try:
            reputacion = funcion_busqueda(url_a_buscar)
            # Actualizar reputación en el label
            if reputacion:
                if reputacion == "Alta":
                    explicacion = "Sitio seguro y confiable. No se han detectado amenazas ni actividades sospechosas."
                elif reputacion == "Media":
                    explicacion = "Sitio con reputación intermedia. Puede tener advertencias o historial dudoso."
                elif reputacion == "Baja":
                    explicacion = "Sitio potencialmente peligroso o sospechoso. Evita ingresar información personal."
                else:
                    explicacion = "Sin información adicional."
                self.label_reputacion.setText(f"Reputación: {reputacion}\n{explicacion}")
            else:
                self.label_reputacion.setText("Reputación: Desconocida")
            self.notificar(f"Análisis de {url_a_buscar} finalizado.")
            self.historial.append(url_a_buscar)
            self.actualizar_historial()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al analizar la URL: {e}")

    def actualizar_historial(self):
        self.historial_text.setPlainText("\n".join(self.historial))

    def exportar_historial(self):
        try:
            import openpyxl
        except ImportError:
            QMessageBox.critical(self, "Error", "Falta el paquete openpyxl. Instálalo con 'pip install openpyxl'.")
            return
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar historial", "historial.xlsx", "Archivos Excel (*.xlsx)")
        if archivo:
            try:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Historial"
                ws.append(["URL"])
                for url in self.historial:
                    ws.append([url])
                wb.save(archivo)
                QMessageBox.information(self, "Éxito", "Historial exportado correctamente en Excel.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar el historial: {e}")

    def cambiar_tema(self, texto):
        if texto == "Claro":
            try:
                with open("style_light.qss", "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"No se pudo cargar el archivo de estilos claro: {e}")
        else:
            try:
                with open("style.qss", "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"No se pudo cargar el archivo de estilos oscuro: {e}")

    def cambiar_idioma(self, texto):
        self.idioma_actual = self.idiomas.get(texto, "es")
        if self.idioma_actual == "en":
            self.setWindowTitle("URL Analyzer")
            self.combo_idioma.setToolTip("Change language")
            self.label_url.setText("URL to analyze")
            self.label_servicios.setText("Select an analysis service:")
            self.label_historial.setText("History of URLs")
            self.label_reputacion.setText("Reputation: Unknown")
        else:
            self.setWindowTitle("Analizador de URL")
            self.combo_idioma.setToolTip("Cambiar idioma")
            self.label_url.setText("URL para analizar")
            self.label_servicios.setText("Seleccione un servicio de análisis:")
            self.label_historial.setText("Historial de URLs")
            self.label_reputacion.setText("Reputación: Desconocida")

    def notificar(self, mensaje):
        print(f"NOTIFICACIÓN: {mensaje}")

# Iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())