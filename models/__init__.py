from flask_login import UserMixin
from storage.database import obter_conexao
from werkzeug.security import generate_password_hash

class User(UserMixin):
    def __init__(self, id, email, senha_hash, is_admin = False, nome=None, cpf=None):
        self.id = id
        self.email = email
        self.senha_hash = senha_hash
        self.is_admin = is_admin
        self.nome = nome
        self.cpf = cpf

    @classmethod
    def get(cls, user_id):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_usuarios WHERE id = ?"
        resultado = conexao.execute(sql, (user_id,)).fetchone()
        if resultado:
            return User(id=resultado['id'],email=resultado['email'], senha_hash=resultado['senha'], is_admin=bool(resultado['is_admin']))
        conexao.close()
        return None

    @classmethod
    def all(cls):
        conexao = obter_conexao()
        sql = "SELECT * FROM tb_usuarios"
        resultados = conexao.execute(sql, ).fetchall()
        usuarios = {}
        usuarios = []
        for i in resultados:
            usuario = User( id=i['id'],email=i['email'],is_admin=i['is_admin']  )
            usuarios.append(usuario)
        
        conexao.close()
        return usuarios

    def save(self):
        conexao = obter_conexao()

        # Verifica se usuário já existe
        sql = "SELECT * FROM tb_usuarios WHERE email = ?"
        resultado = conexao.execute(sql, (self.email,)).fetchone()
        if resultado:
            conexao.close()
            return None
        else:
            # Insere novo usuário
            sql_insert = "INSERT INTO tb_usuarios (email, senha, is_admin) VALUES (?, ?, ?)"
            conexao.execute(sql_insert, (self.email, self.senha_hash, int(self.is_admin)))
            conexao.commit()
            conexao.close()
            return True

    @classmethod
    def delete(cls, email):
        conexao = obter_conexao()

        sql = "DELETE FROM tb_usuarios WHERE nome = ?"
        conexao.execute(sql, (email,))
        conexao.commit()
        conexao.close()
    
    def update(self, email, senha, nome, cpf): #nao chequei tudo dessa função
        conexao = obter_conexao()
        senha_hash = generate_password_hash(senha) #hash para a senha nova
        sql = "UPDATE tb_usuarios SET email = ?, senha = ?, nome = ?, cpf = ? WHERE id = ?"
        conexao.execute(sql, (email, senha_hash, nome, cpf, self.id))
        conexao.commit()
        conexao.close()
        #atualiza os atributos do objeto pra ficar de igual com os dados novos
        self.email = email
        self.senha_hash = senha_hash
        self.nome = nome
        self.cpf = cpf