# Analizador URL

Analizador URL es una aplicación de escritorio desarrollada en Python con una interfaz gráfica (GUI) que permite analizar y extraer información relevante de URLs proporcionadas por el usuario.

## Características principales
- Interfaz gráfica intuitiva y fácil de usar.
- Análisis de URLs para extraer información relevante (dominio, parámetros, etc.).
- Soporte para temas claros y oscuros mediante archivos de estilos `.qss`.
- Resultados presentados de forma clara y estructurada.

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/analizador-url.git
   cd analizador-url
   ```
2. **Crea un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/Mac
   ```
3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta la aplicación:
   ```bash
   python gui.py
   ```
2. Ingresa la URL que deseas analizar en el campo correspondiente.
3. Haz clic en el botón de análisis para ver los resultados.

## Estructura del proyecto
- `analizador.py`: Lógica principal para el análisis de URLs.
- `gui.py`: Interfaz gráfica de usuario.
- `requirements.txt`: Dependencias del proyecto.
- `style.qss` y `style_light.qss`: Archivos de estilos para la GUI.
- `favicon.ico`: Icono de la aplicación.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

## Licencia
Este proyecto está bajo la licencia MIT.
