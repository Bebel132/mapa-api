from flask_restx import Resource, Namespace, fields
from models.estado import EstadoModel

ns = Namespace('estados', description='Ah sei la')

estado_model = ns.model('Estado', {
    'id': fields.Integer(readonly=True),
    'estado': fields.String(readonly=True),
    'porcentagem': fields.String(readonly=True),
    'area': fields.Float(readonly=True),
    'pessoas': fields.Integer(readonly=True),
    'densidade': fields.Integer(readonly=True)
})

@ns.route('/')
class Estados(Resource):    
    def get(self):
        return [
            estado.json() for estado in EstadoModel.query.all()
        ]