import serial
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Datos, db
import os
from dotenv import load_dotenv
load_dotenv()

# Configuración del puerto serie
try:
    ser = serial.Serial('COM3', 115200)  # Asegúrate de usar el puerto correcto
    time.sleep(2)  # Agregar un retraso para asegurarte de que el dispositivo esté listo
except serial.SerialException as e:
    print(f"No se pudo abrir el puerto: {e}")
    exit()

# Configuración de la base de datos
DATABASE_URI = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

try:
    while True:
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            print(linea)
            try:
                datos = json.loads(linea)
                tecla = datos['tecla']
                nota_tecla = datos['nota_tecla']
                frecuencia = datos['frecuencia']
                nota = datos['nota']
                correcta = datos['correcta']

                if nota == "":
                    nota = "---"

                # Guardar los datos en la base de datos
                nuevo_dato = Datos(tecla=tecla, nota_tecla=nota_tecla, frecuencia=frecuencia, nota=nota, correcta=correcta)
                # print(nuevo_dato)
                
                session.add(nuevo_dato)
                session.commit()

            except json.JSONDecodeError:
                pass  # Ignorar líneas que no sean JSON válido

except KeyboardInterrupt:
    ser.close()
    session.close()
    print("Conexión cerrada.")
