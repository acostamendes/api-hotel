from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

argumentos = reqparse.RequestParser()
argumentos.add_argument('login',  type=str, required=True, help="The filed 'login' cannot be left blank.")
argumentos.add_argument('senha', type=str, required=True, help="The find 'senha' cannot be left blank." )

class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user: 
            try:
                user.delete_user()
            except:
                return{'message':'An internal error ocurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}
        return {'message':'User not found.'},404
        

class UserRegister(Resource):
    #/cadastro
    def post(self):
        dados = argumentos.parse_args()

        if UserModel.find_by_login(dados ['login']):
            return {"message": "The login {'login'} already exists.".format(dados['login'])}
        
        user = UserModel(**dados) #(dados['login'], dados['senha']) #instanciando um novo objeto 
        user.save_user()
        return{'message':'User created sucessfully!'},201 #created
    
class UserLogin(Resource):
   
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return  {'access_token': token_de_acesso},200
        return {'message': 'The username or password is incorrect.'},401 #Unathorized 
    