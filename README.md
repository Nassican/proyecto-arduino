# Proyecto Musical Arduino-Flask

Este proyecto combina Arduino con Flask para crear una experiencia musical interactiva.

## Componentes:
1. Arduino: Un teclado 4x4 y un sensor de sonido KY-037.
2. Server: Flask + PostgreSQL para almacenar y visualizar datos.

## Configuración:

### Arduino:
1. Conectar el teclado 4x4 a los pines 2-5 (filas) y 6-9 (columnas).
2. Conectar el buzzer al pin 10.
3. Conectar el sensor KY-037 al pin A0.
4. Cargar `proyecto_musical.ino` al Arduino.

### Servidor:
1. Instalar PostgreSQL y crear una base de datos llamada `proyecto_musical`.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ajustar la configuración en `database.py` y `serial_reader.py`.
4. Ejecutar: `python servidor/app.py`

## Uso:
1. Presionar teclas en el teclado 4x4 para reproducir notas.
2. El sensor detecta el nivel de sonido y determina la nota.
3. Los datos se envían al servidor y se muestran en el dashboard.

## Notas:
- Cada tecla representa una nota musical.
- El nivel de decibelios determina la nota detectada.
- El dashboard se actualiza en tiempo real.