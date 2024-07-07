from sql_alchemy import banco

# Criando classe modelo para usuarios
class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha


    def json(self):  # self é o próprio objeto
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def find_user(cls, user_id):  # (cls) palavra-chave para a classe
        user =  cls.query.filter_by(user_id=user_id).first()  # SELECT * FROM hoteis WHERE hotel_id= $hotel_id LIMIT 1
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):  # (cls) palavra-chave para a classe
        login =  cls.query.filter_by(login=login).first()  # SELECT * FROM hoteis WHERE hotel_id= $hotel_id LIMIT 1
        if login:
            return login
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
