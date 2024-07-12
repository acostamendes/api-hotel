from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from sql_alchemy import banco
from resources.hotel import Hoteis, Hotel
from resources.user import User, UserRegister, UserLogin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
jwt = JWTManager(app)

# Solução para criar o banco de dados antes da primeira requisição
@app.before_first_request
def cria_banco():
    banco.create_all()

# Adicionando o recurso à rota
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    banco.init_app(app)
    app.run(debug=True)

print("JWTManager imported successfully")


# http://127.0.0.1:500/hoteis

# ativar ambiente virtual windows '.\ambvir\Scripts\Activate'
# subir a aplicação 'python3 app.py'