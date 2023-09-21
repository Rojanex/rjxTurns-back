from app.extensions import db
from datetime import datetime

class FilaMaestra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    start_value = db.Column(db.String(255))
    num_elements = db.Column(db.Integer) 
    f_name = db.Column(db.Text)

    def __repr__(self): 
        return f"FilaMaestra({self.id}, {self.nombre})"


class RegistroFila(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turno = db.Column(db.String(255), nullable=False)
    fila_id = db.Column(db.Integer, db.ForeignKey('fila_maestra.id'), nullable=False)
    modulo = db.Column(db.Integer)
    prioridad = db.Column(db.Integer)
    user = db.Column(db.String(255))
    cedula = db.Column(db.String(255)) 
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_atendido = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime) 

    fila = db.relationship('FilaMaestra', backref='registro_filas')

    def __repr__(self):  
        return f"RegistroFila({self.id}, {self.turno}, {self.fila_id})"
