import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_restx import Api, Resource, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

headers = {
    "User-Agent": "Infografico Acesso a Internet no Brasil (https://github.com/Bebel132; contato: emanuel2005batista@gmail.com)"
}

pagina = requests.get('https://pt.wikipedia.org/wiki/Lista_de_unidades_federativas_do_Brasil_por_acesso_%C3%A0_Internet', headers=headers)
dados_pagina = BeautifulSoup(pagina.content, 'html.parser')

tabela = dados_pagina.find("table", class_="wikitable")
linhas = tabela.find_all("tr")[1:]

tabela_dados = []

for linha in linhas:
    td = linha.find_all("td")

    dado = {
        'estado': td[1].get_text(strip=True),
        'porcentagem': td[2].get_text(strip=True)
    }

    tabela_dados.append(dado)

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
# CORS(app, origins=["https://bebel132.github.io"], methods=["GET"])

api = Api(app, doc="/docs")

class EstadoModel(db.Model):
    __tablename__ = 'estados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(50), nullable=False)
    porcentagem = db.Column(db.String(10), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'estado': self.estado,
            'porcentagem': self.porcentagem
        }

ns = Namespace('estados', description='Ah sei la')
estado_model = ns.model('Estado', {
    'id': fields.Integer(readonly=True),
    'estado': fields.String(readonly=True),
    'porcentagem': fields.String(readonly=True)
})

@ns.route('/')
class Estados(Resource):
    def get(self):
        return [
            estado.json() for estado in EstadoModel.query.all()
        ]

api.add_namespace(ns)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not EstadoModel.query.first():
            for dado in tabela_dados:
                estado = EstadoModel(
                    estado=dado['estado'],
                    porcentagem=dado['porcentagem']
                )
                db.session.add(estado)

            db.session.commit()
    app.run(host='0.0.0.0', port=10000, debug=True)