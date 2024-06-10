# Proyecto Musical Arduino-Flask

Este proyecto combina Arduino con Flask para crear una experiencia musical interactiva. (ES NECESARIO UN ARDUINO)

## Componentes:
1. Arduino: Un teclado 4x4 y un sensor de sonido KY-037.
2. Server: Flask + PostgreSQL para almacenar y visualizar datos.

## Configuración:

### Arduino:
1. Conectar el teclado 4x4 a los pines 2-5 (filas) y 6-9 (columnas).
2. Conectar el buzzer al pin 10.
3. Conectar el sensor KY-037 al pin A0.
4. Cargar `proyecto_musical.ino` al Arduino.

### INSTALACION MANUAL:

### Servidor:

1. Instalar Python.
2. Instalar PostgreSQL y crear una base de datos llamada `proyecto_musical`.
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar: `python server/app.py` (LA TABLA DATOS SE DEBERIA GENERAR AUTOMATICAMENTE)
5. En caso de que la tabla Datos no se ejecute, usar el contenido del init.sql
6. Si lo hace de manera local sin el docker, en read_serial cambiar el puerto de 5433 al que este usando localmente (5432 por defecto)

### INSTALACION CON DOCKER:

1. Instalar Docker (Docker Desktop en Windows, sudo apt install docker en Linux)
2. Instalar Python
3. Ejecutar docker-compose up --build (ESPERAR)
4. Conectar el Arduino e identificar cual es el puerto que esta usando (Windows COM1, COM3 ...) (Linux dev01/...)
5. Ejecuta `python server/read_serial.py`
6. Si no se conecta o da error verifica los puertos de la base de datos, en docker sera por defecto 5433

## Uso:
1. Presionar teclas en el teclado 4x4 para reproducir notas.
2. El sensor detecta el nivel de sonido y determina la nota.
3. Los datos se envían al servidor y se muestran en el dashboard.

## Notas:
- Cada tecla representa una nota musical.
- La frecuencia determina la nota detectada.
- El dashboard se actualiza en tiempo real.

## Estructura del Proyecto

```
.
├── arduino/
│   ├── proyecto_musical/
│   │   └── proyecto_musical.ino
│   ├── proyecto_musical_solo_keypad.ino
│   └── README.md
├── server/
│   ├── static/
│   │   └── src/
│   │       ├── chartRespaldo.js
│   │       ├── input.css
│   │       └── script.js
│   ├── templates
│   │   └── index.html
│   ├── app.py
│   ├── models.py
│   └── read_serial.py
├── .env
├── .env.example
├── init.sql
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
└── requirements.txt
```