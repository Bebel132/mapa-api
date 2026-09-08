from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from models.estado import EstadoModel
from resource.scrap import tabela_dados
from extensions import db
from resource.estados import ns

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# CORS(app)
CORS(app, origins=["https://bebel132.github.io", "http://localhost:5500", "http://127.0.0.1:5500"], methods=["GET"])

api = Api(app, doc="/docs")

api.add_namespace(ns)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not EstadoModel.query.first():
            for dado in tabela_dados:
                estado = EstadoModel(
                    estado=dado['estado'],
                    porcentagem=dado['porcentagem'],
                    area=dado['area'],
                    pessoas=dado['pessoas'],	
                    densidade=int(dado['pessoas']/dado['area'])
                )
                db.session.add(estado)

            db.session.commit()
    app.run(host='0.0.0.0', port=5003, debug=True)
