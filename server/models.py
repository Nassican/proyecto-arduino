from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Datos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tecla = db.Column(db.String(10), nullable=False)
    nota_tecla = db.Column(db.String(10), nullable=False)
    frecuencia = db.Column(db.Float, nullable=False)
    nota = db.Column(db.String(10), nullable=False)
    correcta = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Datos(tecla={self.tecla}, nota_tecla={self.nota_tecla}, frecuencia={self.frecuencia}, nota={self.nota}, correcta={self.correcta}, timestamp={self.timestamp})>"
