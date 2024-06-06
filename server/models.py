from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Datos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tecla = db.Column(db.String(1), nullable=False)
    frecuencia = db.Column(db.Float, nullable=False)
    nota = db.Column(db.String(10), nullable=False)
    correcta = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
