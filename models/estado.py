from extensions import db

class EstadoModel(db.Model):
    __tablename__ = 'estados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(50), nullable=False)
    porcentagem = db.Column(db.String(10), nullable=False)
    area = db.Column(db.Float, nullable=False)
    pessoas = db.Column(db.Integer, nullable=False)
    densidade=db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'estado': self.estado,
            'porcentagem': self.porcentagem,
            'area': self.area,
            'pessoas': self.pessoas,
            'densidade': self.densidade
        }
