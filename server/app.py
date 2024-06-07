from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Datos
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datos')
def obtener_datos():
    datos = Datos.query.order_by(Datos.timestamp.desc()).limit(10).all()
    resultados = [
        {
            'tecla': dato.tecla,
            'nota_tecla': dato.nota_tecla,
            'frecuencia': dato.frecuencia,
            'nota': dato.nota,
            'correcta': dato.correcta,
            'timestamp': dato.timestamp.strftime("%H:%M:%S")
        }
        for dato in datos
    ]
    return jsonify(resultados)

@app.route('/estadisticas')
def obtener_estadisticas():
    total_notas = Datos.query.count()
    total_correctas = Datos.query.filter_by(correcta=True).count()
    porcentaje_correctas = (total_correctas / total_notas * 100) if total_notas > 0 else 0

    estadisticas = {
        'total_notas': total_notas,
        'total_correctas': total_correctas,
        'porcentaje_correctas': porcentaje_correctas
    }
    return jsonify(estadisticas)

@app.route('/notas')
def obtener_estadisticas_por_nota():
    notas_distintas = db.session.query(Datos.nota_tecla).distinct().all()
    estadisticas_por_nota = []
    for nota_tecla in notas_distintas:
        nota_tecla = nota_tecla[0]  # La nota es una tupla, por lo que tomamos el primer elemento
        total_notas = Datos.query.filter_by(nota_tecla=nota_tecla).count()
        total_correctas = Datos.query.filter_by(nota_tecla=nota_tecla, correcta=True).count()
        porcentaje_correctas = (total_correctas / total_notas * 100) if total_notas > 0 else 0
        estadisticas_por_nota.append({
            'nota': nota_tecla,
            'total_notas': total_notas,
            'total_correctas': total_correctas,
            'porcentaje_correctas': porcentaje_correctas
        })

        # Quitar indices de la respuesta
        '''
        PASAR DE ESTO:
        "B4": {
            "nota": "B4",
            "porcentaje_correctas": 100,
            "total_correctas": 13,
            "total_notas": 13
        }
        A ESTO:
        [
            {
                "nota": "B4",
                "porcentaje_correctas": 100,
                "total_correctas": 13,
                "total_notas": 13
            }
        ]
        
        '''


    return jsonify(estadisticas_por_nota)

if __name__ == '__main__':
    app.run(debug=True)
