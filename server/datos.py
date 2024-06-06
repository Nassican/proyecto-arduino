import serial
import json
import time
from collections import defaultdict

# Configuración del puerto serie
try:
    ser = serial.Serial('COM3', 115200)  # Asegúrate de usar el puerto correcto
    time.sleep(2)  # Agregar un retraso para asegurarte de que el dispositivo esté listo
except serial.SerialException as e:
    print(f"No se pudo abrir el puerto: {e}")
    exit()

# Estructuras de datos para almacenar estadísticas
notas_totales = 0
notas_correctas = 0
frecuencias = defaultdict(list)
notas_por_tecla = defaultdict(lambda: defaultdict(int))
ultimo_tiempo = time.time()

try:
    while True:
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            print(linea)
            try:
                datos = json.loads(linea)
                tecla = datos['tecla']
                frecuencia = datos['frecuencia']
                nota = datos['nota']
                correcta = datos['correcta']

                #print(f"Tecla: {tecla}, Frecuencia: {frecuencia}, Nota: {nota}, Correcta: {correcta}")

                # Actualizar estadísticas
                notas_totales += 1
                if correcta:
                    notas_correctas += 1

                if nota != "Nota no encontrada":
                    frecuencias[nota].append(frecuencia)
                    notas_por_tecla[tecla][nota] += 1

                # Calcular notas por minuto
                tiempo_actual = time.time()
                if tiempo_actual - ultimo_tiempo > 60:
                    print(f"Notas por minuto: {notas_totales}")
                    notas_totales = 0
                    ultimo_tiempo = tiempo_actual

            except json.JSONDecodeError:
                pass  # Ignorar líneas que no sean JSON válido

except KeyboardInterrupt:
    ser.close()
    print("Conexión cerrada.")