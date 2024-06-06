from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psycopg2
import pandas as pd
import serial
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = process.env.SECRET_KEY
socketio = SocketIO(app)

# Configuración de la conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host=process.env.DB_HOST,
    database=process.env.DB_NAME,
    user=process.env.DB_USER,
    password=process.env.DB_PASSWORD,
)

# Configuración del puerto serie
# try:
#     ser = serial.Serial('COM3', 115200)
# except serial.SerialException as e:
#     print(f"No se pudo abrir el puerto: {e}")
#     exit()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('obtener_datos')
def obtener_datos():
    cur = conn.cursor()
    cur.execute("SELECT * FROM notas ORDER BY id DESC LIMIT 10")
    notas = cur.fetchall()
    cur.close()

    # Convertir los datos a un DataFrame de Pandas
    df = pd.DataFrame(notas, columns=['id', 'tecla', 'frecuencia', 'nota', 'correcta'])

    # Convertir el DataFrame a un diccionario
    data = df.to_dict('records')

    socketio.emit('actualizar_datos', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)