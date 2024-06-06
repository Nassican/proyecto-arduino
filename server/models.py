from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Datos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tecla = db.Column(db.String(10), nullable=False)
    frecuencia = db.Column(db.Float, nullable=False)
    nota = db.Column(db.String(10), nullable=False)
    correcta = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Datos {self.tecla} - {self.nota}>'
