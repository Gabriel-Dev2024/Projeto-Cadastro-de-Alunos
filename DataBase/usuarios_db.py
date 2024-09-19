import sqlite3

class DB_Usuarios():
    def conecta_db(self):

        # Conecta ao banco de dados SQLite ou cria um novo se não existir
        self.conn = sqlite3.connect('Usuarios.db')
        self.cursor = self.conn.cursor()
        print('Banco de dados conectado com sucesso!')

    def desconecta_db(self):

        # Fecha a conexão com o banco de dados
        self.conn.close()

    def cria_tabela(self):

        # Cria a tabela Usuarios se ela não existir no banco de dados
        self.conecta_db()


        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                telefone TEXT
            )
        """)
        self.conn.commit()
        print('Tabela criada com sucesso!')
        self.desconecta_db()
