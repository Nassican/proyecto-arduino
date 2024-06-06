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
            'frecuencia': dato.frecuencia,
            'nota': dato.nota,
            'correcta': dato.correcta,
            'timestamp': dato.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for dato in datos
    ]
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
