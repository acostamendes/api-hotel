from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from sql_alchemy import banco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# Solução para criar o banco de dados antes da primeira requisição
@app.before_first_request
def cria_banco():
        banco.create_all()

# Adicionando o recurso à rota /hoteis
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True)


# http://127.0.0.1:500/hoteis