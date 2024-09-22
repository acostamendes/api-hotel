import sqlite3

connection =sqlite3.connect('banco.db')
cursor = connection.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id TEXT PRIMARY KEY, nome TEXT, estrela real, diaria real, cidade TEXT )"

cria_hotel = "INSERT INTO hoteis VALUES ('alpha', 'Alpha Hotel', 4.3, 345.30, 'São Paulo')"


cursor.execute(cria_tabela)
cursor.execute(cria_hotel)


connection.commit()
connection.close()


