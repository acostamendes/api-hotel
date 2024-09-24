from sql_alchemy import banco

# Criando classe modelo para hotel
class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel') # lista de objetos hoteis
    

    def __init__(self, url):
        self.url = url

    def json(self):  # self é o próprio objeto
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):  # (cls) palavra-chave para a classe
        site= cls.query.filter_by(url=url).first()  # SELECT * FROM site WHERE url= $url LIMIT 1
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()